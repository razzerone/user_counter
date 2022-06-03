_browsers = [
    ('Opera', 'Opera'),
    ('OPR', 'Opera'),
    ('Edg', 'Edge'),
    ('YaBrowser', 'YaBrowser'),
    ('Chrome', 'Chrome'),
    ('Safari', 'Safari'),
    ('Firefox', 'Firefox'),
]

BROWSERS = [
    'Opera',
    'Edge',
    'YaBrowser',
    'Chrome',
    'Safari',
    'Firefox',
]

OS = [
    'Linux',
    'Windows',
    'Android',
]


def identify_browser(user_agent: str) -> str:
    for i, res in _browsers:
        if i in user_agent:
            return res

    return 'unknown'


def identify_os(user_agent: str) -> str:
    for i in OS:
        if i in user_agent:
            return i

    return 'unknown'
