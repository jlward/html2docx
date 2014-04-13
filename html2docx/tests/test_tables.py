from html2docx.tests import build_run


test_cases = [
    (
        'Test simple table.',
        '<table><tr><td>AAA</td></tr></table>',
    ),
    (
        'Test multiple rows.',
        '<table><tr><td>AAA</td></tr><tr><td>BBB</td></tr></table>',
    ),
    (
        'Test multiple cells.',
        '<table><tr><td>AAA</td><td>BBB</td></tr></table>',
    ),
    (
        'Test multiple rows and cells.',
        '<table><tr><td>AAA</td><td>BBB</td></tr><tr><td>CCC</td><td>DDD</td></tr></table>',  # noqa
    ),
]


def test():
    for test_name, html in test_cases:
        run = build_run(test_name, html)
        yield run
