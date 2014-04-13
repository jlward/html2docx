from html2docx.tests import build_run


test_cases = [
    (
        'Test simple table.',
        '<table><tr><td>AAA</td></tr></table>',
    ),
]


def test():
    for test_name, html in test_cases:
        run = build_run(test_name, html)
        yield run
