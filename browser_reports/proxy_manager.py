import os
# from undetected_chromedriver import Chrome
# from selenium.webdriver import ChromeOptions
import shutil
import random
import fake_useragent
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service as ChromeService


class FileManager:
    def __init__(self, file_name):
        with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
            self.lines = f.readlines()

    def get_line(self):
        line = random.choice(self.lines).strip()
        return line


def split_proxy(proxy_line):
    part1, part2 = proxy_line.split('@')
    login, password = part1.split(':')
    host, port = part2.split(':')
    return host, port, login, password


def generate_random_zip():
    return ''.join(random.choices('1234567890asdfghhjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM', k=16))


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
"""


def get_chromedriver(host, port, login, password):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = ChromeOptions()
    plugin_file = generate_random_zip()
    os.mkdir(os.path.join(path, plugin_file))
    with open(os.path.join(path, plugin_file, 'manifest.json'), 'w') as f:
        f.write(manifest_json)
    with open(os.path.join(path, plugin_file, 'background.js'), 'w') as f:
        f.write(background_js % (host, port, login, password))

    ua = fake_useragent.UserAgent().random
    chrome_options.add_argument(f'--load-extension={os.path.join(path, plugin_file)}')
    chrome_options.add_argument('--user-agent=%s' % ua)
    chrome_options.headless = True
    driver = Chrome(driver_executable_path=ChromeService(ChromeDriverManager().install()).path,
                    options=chrome_options,
                    headless=False)
    shutil.rmtree(os.path.join(path, plugin_file))
    return driver, ua
