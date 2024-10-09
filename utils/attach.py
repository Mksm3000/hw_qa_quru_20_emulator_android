import os

import allure
import requests


def png_attachment(browser):
    allure.attach(browser.driver.get_screenshot_as_png(), 'screenshot',
                  allure.attachment_type.PNG)


def xml_attachment(browser):
    allure.attach(browser.driver.page_source, 'screen xml dump',
                  allure.attachment_type.XML, '.xml')


def log_attachment(browser):
    log = "".join(f'{text}\n' for text in browser.driver.get_log(log_type='browser'))
    allure.attach(log, 'browser_logs', allure.attachment_type.TEXT, '.log')


def html_attachment(browser):
    html = browser.driver.page_source
    allure.attach(html, 'page_source', allure.attachment_type.HTML, '.html')


def web_video_attachment(browser):
    video_url = "https://selenoid.autotests.cloud/video/" + browser.driver.session_id + ".mp4"
    html = "<html><body><video width='100%' height='100%' controls autoplay><source src='" \
           + video_url \
           + "' type='video/mp4'></video></body></html>"
    allure.attach(html, 'video_' + browser.driver.session_id,
                  allure.attachment_type.HTML, '.html')


def video_attachment(session_id):
    bs_session = requests.get(url=f'https://api.browserstack.com/app-automate/sessions/'
                                  f'{session_id}.json',
                              auth=((os.getenv('BS_NAME'), os.getenv('BS_KEY')))).json()
    video_url = bs_session["automation_session"]["video_url"]

    allure.attach('<html><body>'
                  '<video width="100%" height="100%" controls autoplay>'
                  f'<source src="{video_url}" type="video/mp4">'
                  '</video></body></html>',
                  'video recording', allure.attachment_type.HTML)
