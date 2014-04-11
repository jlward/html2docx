from html2docx import HTML2Docx


test_cases = [
    (
        'Test blank.',
        '',
    ),
    (
        'Test super simple.',
        '<p>AAA</p>',
    ),
]


def test():
    for test_name, html in test_cases:
        def run():
            HTML2Docx(html, 'test.docx')
            html == html
        run.description = test_name
        yield run
