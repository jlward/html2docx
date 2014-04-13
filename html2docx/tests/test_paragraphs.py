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
    (
        'Test bold.',
        '<p><strong>AAA</strong></p>',
    ),
    (
        'Test partial bold.',
        '<p>A<strong>A</strong>A</p>',
    ),
    (
        'Test em.',
        '<p><em>AAA</em></p>',
    ),
    (
        'Test partial em.',
        '<p>A<em>A</em>A</p>',
    ),
    (
        'Test mixed styles.',
        '<p><strong><em>AAA</em></strong></p>',
    ),
]


def test():
    for test_name, html in test_cases:
        run = build_run(test_name, html)
        yield run
