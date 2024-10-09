import pytest
from selene import browser
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.attach import png_attachment, log_attachment, html_attachment, web_video_attachment


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def browser_management():
    browser.config.base_url = os.getenv('base_url', 'https://www.wikipedia.org')

    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = 30

    selenoid_login = os.getenv('SELENOID_LOGIN')
    selenoid_pass = os.getenv('SELENOID_PASS')
    selenoid_url = os.getenv('SELENOID_URL')

    options = Options()
    selenoid_capabilities = {
        'browserName': 'chrome',
        'browserVersion': '126.0',
        'selenoid:options': {
            'enableVNC': True,
            'enableVideo': True,
        }
    }
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=f'https://{selenoid_login}:{selenoid_pass}@{selenoid_url}',
        options=options
    )

    browser.config.driver = driver

    yield browser

    png_attachment(browser)
    log_attachment(browser)
    html_attachment(browser)
    web_video_attachment(browser)

    browser.quit()
