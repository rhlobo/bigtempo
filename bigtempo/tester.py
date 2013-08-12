# -*- coding: utf-8 -*-


import os
import pandas

import unittest
from mockito import mock, unstub

import bigtempo.utils as utils


def generate_for_references(engine, references, symbol, start, end, test_data_dir, module=None):
    for reference in references:
        generate_for_reference(engine, reference, symbol, start, end, test_data_dir, module)


def generate_for_reference(engine, reference, symbol, start, end, test_data_dir, module=None):
    if not os.path.isfile(_get_datafile_path(reference, symbol, test_data_dir)):
        return

    class CustomDatasourceTestCase(_create_datasource_test_case_for(engine)):

        def test_datasource_using_test_data(self):
            _assert_datasource_correctness_using_datafiles(engine, reference, symbol, start, end, test_data_dir)

    CustomDatasourceTestCase.__name__ = '%s{%s}[%s:%s]' % (reference, symbol, start, end)

    if module:
        setattr(module,
                'assert_datasource_correctness_using_datafiles(%s){%s}[%s:%s]' % (reference, symbol, start, end),
                CustomDatasourceTestCase)


def _create_datasource_test_case_for(engine):
    class DatasourceTestCase(unittest.TestCase):

        @classmethod
        def setUpClass(cls):
            testing_builder_mock = mock()

            def testing_builder(cls):
                mock_result = testing_builder_mock.build(cls)
                if mock_result:
                    return mock_result
                return cls()

            cls.testing_builder_mock = testing_builder_mock
            cls.original_builder = engine._builder
            engine._builder = testing_builder

        @classmethod
        def tearDownClass(cls):
            engine._builder = cls.original_builder
            engine._instances = {}

        def setUp(self):
            engine._instances = {}

        def tearDown(self):
            unstub()

    return DatasourceTestCase


def _get_datafile_path(reference, symbol, test_data_dir):
    filename = '%s{%s}.csv' % (reference, symbol)
    return os.path.join(test_data_dir, filename)


def _assert_datasource_correctness_using_datafiles(engine, reference, symbol, start, end, test_data_dir):
    logger = utils.DatasourceLogger()
    mocked_registrations = {}

    for dependency_reference in engine._registrations[reference]['dependencies']:
        mock_data_file = _get_datafile_path(dependency_reference, symbol, test_data_dir)

        if not os.path.isfile(mock_data_file):
            continue

        datasource_mock_cls = _create_mock_datasource(dependency_reference, mock_data_file, logger)

        if not engine._registrations.get(dependency_reference):
            engine._registrations[dependency_reference] = {}

        mocked_registrations[dependency_reference] = engine._registrations[dependency_reference]
        engine._registrations[dependency_reference] = {
            'class': datasource_mock_cls,
            'lookback': 0,
            'dependencies': set()
        }

    expected_data_file = _get_datafile_path(reference, symbol, test_data_dir)

    actual = engine.get(reference).process(symbol, start, end)
    expected = utils.slice(pandas.DataFrame.from_csv(expected_data_file), start, end)

    logger.log('actual', actual)
    logger.log('expected', expected)

    try:
        _assert_dataframe_almost_equal(expected, actual)
    except Exception, e:
        logger.print_summary()
        raise e
    finally:
        for dependency_reference, original_registration in mocked_registrations.items():
            engine._registrations[dependency_reference] = original_registration


def _create_mock_datasource(mock_reference, mock_data_file, logger):
    class DatasourceMock(object):

        def evaluate(self, context, symbol, start=None, end=None):
            data = pandas.DataFrame.from_csv(mock_data_file)
            logger.log(os.path.basename(mock_data_file), data)
            return data

    return DatasourceMock


def _assert_dataframe_almost_equal(expected, actual, margin=0.0000000001):
    tmp = ((expected.dropna() - actual.dropna()).abs() < margin)
    assert tmp.all().all()
