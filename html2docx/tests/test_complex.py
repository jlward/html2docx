from html2docx.tests import build_run


test_cases = [
    (
        'Test paragraph, table, paragraph.',
        '<p>AAA</p><table><tr><td>BBB</td></tr></table><p>CCC</p>',
    ),
    (
        'Test table, table, paragraph',
        '<table><tr><td>AAA</td></tr></table><table><tr><td>BBB</td></tr></table><p>CCC</p>',  # noqa
    ),
    # Nesting doesn't really work yet.
    # (
    #     'Test Nested Table',
    #     '<table><tr><td>AAA</td><td><table><tr><td>BBB</td></tr></table></td></tr></table>',  # noqa
    # ),
]


def test():
    for test_name, html in test_cases:
        run = build_run(test_name, html)
        yield run
