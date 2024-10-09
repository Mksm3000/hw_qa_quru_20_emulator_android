import os

# context = os.getenv('context', 'bstack')
# run_on_bstack = os.getenv('run_on_bstack', 'false').lower() == 'true'
# 'app': 'bs://77e1f3856082cb9f61564781fdb95d123840f38c'

remote_url = os.getenv('remote_url', 'http://127.0.0.1:4723/wd/hub')
deviceName = os.getenv('deviceName')
deviceUdid = os.getenv('deviceUdid', 'emulator-5554')
platformVersion = os.getenv('platformVersion', '9.0')
appWaitActivity = os.getenv('appWaitActivity', 'org.wikipedia.*')
app = os.getenv('app', './resources/org.wikipedia--50479.apk')
runs_on_bstack = app.startswith('bs://')
if runs_on_bstack:
    remote_url = 'http://hub.browserstack.com/wd/hub'
