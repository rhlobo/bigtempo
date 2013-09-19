# -*- coding: utf-8 -*-


import os
import copy
import pandas

import unittest
from mockito import mock, unstub

import bigtempo.utils as utils


def generate_multiple(engine, references, symbol, start, end, test_data_filepath_fn, module=None):
    results = []
    for reference in references:
        result = generate(engine, reference, symbol, start, end, test_data_filepath_fn, module)
        results.append(result)
    if module is None:
        return results


def generate(engine, reference, symbol, start, end, test_data_filepath_fn, module=None):
    if not os.path.isfile(test_data_filepath_fn(reference, symbol)):
        return

    class CustomDatasourceTestCase(_create_datasource_test_case_for(engine)):

        def test_datasource_using_test_data(self):
            _assert_datasource_correctness_using_datafiles(engine, reference, symbol, start, end, test_data_filepath_fn)

    CustomDatasourceTestCase.__name__ = '%s{%s}[%s:%s]' % (reference, symbol, start, end)

    if module is None:
        return CustomDatasourceTestCase

    setattr(module,
            'TestDatasourceCorrectness(%s){%s}[%s:%s]' % (reference, symbol, start, end),
            CustomDatasourceTestCase)


def _create_datasource_test_case_for(engine):
    class DatasourceTestCase(unittest.TestCase):

        @classmethod
        def setUpClass(cls):
            testing_datasource_factory_mock = mock()

            def testing_datasource_factory(cls):
                mock_result = testing_datasource_factory_mock.build(cls)
                if mock_result:
                    return mock_result
                return cls()

            cls.testing_datasource_factory_mock = testing_datasource_factory_mock
            cls.original_datasource_factory = engine._datasource_factory
            engine._datasource_factory = testing_datasource_factory

        @classmethod
        def tearDownClass(cls):
            engine._datasource_factory = cls.original_datasource_factory
            engine._instances = {}

        def setUp(self):
            engine._instances = {}

        def tearDown(self):
            unstub()

    return DatasourceTestCase


def _assert_datasource_correctness_using_datafiles(engine, reference, symbol, start, end, test_data_filepath_fn):
    logger = utils.DatasourceLogger()

    original_registrations = {}

    for dependency_reference in engine._registrations[reference]['dependencies']:
        mock_data_file = test_data_filepath_fn(dependency_reference, symbol)

        if not os.path.isfile(mock_data_file):
            continue

        datasource_mock_cls = _create_mock_datasource(dependency_reference, mock_data_file, logger)

        if not engine._registrations.get(dependency_reference):
            engine._registrations[dependency_reference] = {}

        original_registrations[dependency_reference] = engine._registrations[dependency_reference]
        registration_mock = copy.deepcopy(engine._registrations[dependency_reference])
        registration_mock['class'] = datasource_mock_cls
        registration_mock['dependencies'] = set()
        engine._registrations[dependency_reference] = registration_mock

    expected_data_file = test_data_filepath_fn(reference, symbol)

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
        for dependency_reference, original_registration in original_registrations.items():
            engine._registrations[dependency_reference] = original_registration


def _create_mock_datasource(mock_reference, mock_data_file, logger):
    class DatasourceMock(object):

        def evaluate(self, context, symbol, start=None, end=None):
            data = pandas.DataFrame.from_csv(mock_data_file)
            sliced_data = utils.slice(data, start, end)
            logger.log(os.path.basename(mock_data_file), sliced_data)
            return sliced_data

    return DatasourceMock


def _assert_dataframe_almost_equal(expected, actual, margin=0.0000000001):
    tmp = ((expected.dropna() - actual.dropna()).abs() < margin)
    assert tmp.all().all()
