import time
from threading import Thread

import fake_useragent

# from selenium.webdriver.common.by import By
from .proxy_manager import get_chromedriver, split_proxy
import requests


class Browser(Thread):
    def __init__(self, number, text, email, proxy, who_report, uuid_order):
        super().__init__()
        self.number = number
        self.text = text
        self.email = email
        self.proxy = proxy.strip()
        self.who_report = who_report
        self.uuid_order = uuid_order

    def run(self) -> None:
        tries = 5
        # proxies = {'http': self.proxy, 'https': self.proxy}
        while tries:
            # driver = None
            try:
                # driver, ua = get_chromedriver(*split_proxy(self.proxy))
                ua = fake_useragent.UserAgent().random
                # driver.get('https://telegram.org/support?setln=ru')
                # self.text += f'\n{self.who_report}'
                # driver.find_element(By.ID, 'support_problem').send_keys(self.text)
                # driver.find_element(By.ID, 'support_email').send_keys(self.email)
                # driver.find_element(By.ID, 'support_phone').send_keys(self.number)
                # driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-lg').click()
                # time.sleep(10)
                data = {'message': self.text, 'email': self.email, 'phone': self.number, 'setln': 'ru'}
                r = requests.post(
                    'https://telegram.org/support',
                    proxies={'http': self.proxy, 'https': self.proxy},
                    data=data,
                    headers={'user-agent': ua}
                )
                print(r.text)
                if 'Мы постараемся отреагировать как можно быстрее.' in r.text:
                    requests.post('http://127.0.0.1:8000/site_reports/save_report/', data={
                        'phone_number': self.number,
                        'user_agent': ua,
                        'mail': self.email,
                        'report_text': self.text,
                        'uuid': self.uuid_order
                    })

                # driver.quit()
                break
            except Exception as e:
                print(f'Что-то пошло не так с {self.number}\n{str(e)}\n')
                tries -= 1
                # if driver:
                #     driver.quit()
