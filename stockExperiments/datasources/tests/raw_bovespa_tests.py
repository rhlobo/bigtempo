from datetime import datetime as dt

import util.testutils as testutils

import instances
import datasources.raw_bovespa as raw_bovespa


class TestRawBovespaDatasource(testutils.DatasourceTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestRawBovespaDatasource, cls).setUpClass()
        cls.importer = raw_bovespa.cotahist.CotahistImporter
        raw_bovespa.cotahist.CotahistImporter = _CotahistImporterMock

    @classmethod
    def tearDownClass(cls):
        super(TestRawBovespaDatasource, cls).tearDownClass()
        raw_bovespa.cotahist.CotahistImporter = cls.importer

    def test_should_return_empty_dataFrame_when_period_not_available(self):
        processor = instances.data_engine.get('RAW_BOVESPA')
        data = processor.process('PETR4', dt(2114, 3, 10), dt(2114, 4, 26))
        assert len(data) == 0

    def test_should_return_dataFrame_subset_when_period_is_contained_in_available_data(self):
        processor = instances.data_engine.get('RAW_BOVESPA')
        data = processor.process('PETR4', dt(2013, 3, 8), dt(2013, 3, 12))
        assert len(data) == 3
        assert data.ix[0].name == dt(2013, 3, 8)
        assert data.ix[1].name == dt(2013, 3, 11)
        assert data.ix[2].name == dt(2013, 3, 12)

    def test_should_return_whole_dataFrame_when_no_startdt_and_enddt_is_given(self):
        processor = instances.data_engine.get('RAW_BOVESPA')
        data = processor.process('PETR4')
        assert len(data) == 18
        assert data.ix[0].name == dt(2013, 3, 1)
        assert data.ix[17].name == dt(2013, 3, 26)

    def test_should_return_dataFrame_begining_on_1st_record_when_no_startdt_is_given(self):
        processor = instances.data_engine.get('RAW_BOVESPA')
        data = processor.process('PETR4', end=dt(2013, 3, 12))
        assert len(data) == 8
        assert data.ix[0].name == dt(2013, 3, 1)
        assert data.ix[7].name == dt(2013, 3, 12)

    def test_should_return_dataFrame_records_until_last_when_no_enddt_is_given(self):
        processor = instances.data_engine.get('RAW_BOVESPA')
        data = processor.process('PETR4', start=dt(2013, 3, 23))
        assert len(data) == 2
        assert data.ix[0].name == dt(2013, 3, 25)
        assert data.ix[1].name == dt(2013, 3, 26)


class _CotahistImporterMock(object):

    def __init__(self, s_data_dir):
        self.d_dataFrame = {}
        self.d_dataFrame['PETR4'] = testutils.get_dataframe_from_csv(__file__, 'petr4.csv')

    def getDataFrameMap(self):
        return self.d_dataFrame
