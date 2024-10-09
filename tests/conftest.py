import allure
import allure_commons
import pytest
from appium import webdriver
from dotenv import load_dotenv
from selene import browser, support

import config
from utils.attach import png_attachment, xml_attachment, video_attachment


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        default="bstack",
        help="Specify the test context"
    )


def pytest_configure(config):
    context = config.getoption("--context")
    env_file_path = f".env.{context}"

    load_dotenv(dotenv_path=env_file_path)


@pytest.fixture
def context(request):
    return request.config.getoption("--context")


@pytest.fixture(autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def mobile_management(context):
    options = config.to_driver_options(context=context)

    browser.config.driver = webdriver.Remote(command_executor=options.get_capability('remote_url'),
                                             options=options)
    browser.config.timeout = 30.0

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext)

    yield browser

    png_attachment(browser)
    xml_attachment(browser)

    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

    if context == 'bstack':
        video_attachment(session_id)
