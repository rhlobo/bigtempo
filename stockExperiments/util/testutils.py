import os


def should_skip_provider_deep_tests():
    return os.environ.get('TESTTYPE') == 'FAST'


def get_providers_deep_tests_skip_reason():
    if os.environ.get('TESTTYPE') == 'FAST':
        return 'Fast test execution requested through environment variable.'
    return 'Providers deep tests are disabled.'
