from html2docx.tests import build_run


test_cases = [
    (
        'Test blank.',
        '',
    ),
    (
        'Test super simple.',
        '<p>AAA</p>',
    ),
    (
        'Test multiple.',
        '<p>AAA</p><p>BBB</p>',
    ),
]


def test():
    for test_name, html in test_cases:
        run = build_run(test_name, html)
        yield run
