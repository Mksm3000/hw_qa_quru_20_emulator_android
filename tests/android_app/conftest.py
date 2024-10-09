import os

import allure
import allure_commons
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv
from selene import browser, support

import config
import utils.file
from utils.attach import png_attachment, xml_attachment, video_attachment


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    options = UiAutomator2Options()

    if config.deviceName:
        options.set_capability('deviceName', config.deviceName)

    if config.appWaitActivity:
        options.set_capability('appWaitActivity', config.appWaitActivity)

    options.set_capability('app',
                           config.app if
                           (config.app.startswith(
                               '/') or config.runs_on_bstack) else
                           utils.file.abs_path_from_project(config.app))

    if config.runs_on_bstack:
        options.load_capabilities({
            'bstack:options': {
                'projectName': 'First Python project',
                'buildName': 'browserstack-build-1',
                'sessionName': 'BStack first_test',
                'platformVersion': os.getenv('platformVersion'),
                'userName': os.getenv('BS_NAME'),
                'accessKey': os.getenv('BS_KEY')
            }
        })

    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(config.remote_url,
                                                 options=options)

    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext)

    yield

    png_attachment(browser)

    xml_attachment(browser)

    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

    if config.runs_on_bstack:
        video_attachment(session_id)
