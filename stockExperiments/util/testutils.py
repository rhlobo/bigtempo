import os


def should_skip_provider_deep_tests():
    return os.environ.get('TESTTYPE') == 'FAST'


def get_providers_deep_tests_skip_reason():
    if os.environ.get('TESTTYPE') == 'FAST':
        return 'Fast test execution requested through environment variable.'
    return 'Providers deep tests are disabled.'


def assert_data_index_is_ordered(data):
    lastDate = data.ix[0].name
    for row in data.iterrows():
        currDate = row[0]
        assert currDate >= lastDate
        lastDate = currDate


def assert_dataframe_almost_equal(expected, actual, margin=0.0000000001):
    tmp = (expected - actual).abs() < margin
    assert tmp.all().all() == True
