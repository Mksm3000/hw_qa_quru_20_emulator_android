from selene import have, browser
from allure import step


def test_search():
    browser.open('/')

    with step('Type search'):
        browser.element('#search-input').element('#searchInput').type('Apple')

    with step('Verify content found'):
        results = browser.all('.suggestion-link')
        assert results.should(have.size_greater_than(0))
        assert results.first.should(have.text('Apple'))

