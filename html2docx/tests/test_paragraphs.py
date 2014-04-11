test_cases = [
    (
        'Test super simple.',
        '<p>AAA</p>',
    ),
]


def test():
    for test_name, html in test_cases:
        def run():
            html == html
        run.description = test_name
        yield run
