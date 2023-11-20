import time
import os
from .browser import Browser
from .proxy_manager import FileManager
import random


class ReportBrowser:
    def __init__(self, thread_count, count_numbers, who_report, uuid_order, proxy):
        self.thread_count = thread_count
        self.count_numbers = count_numbers
        self.who_report = who_report
        self.proxy = proxy

        pm = FileManager('proxies.txt')
        em = FileManager('emails.txt')

        numbers = self.generate_random_numbers(self.count_numbers)
        while numbers:
            current_numbers = numbers[:self.thread_count]
            threads = []
            for number in current_numbers:
                email = em.get_line()
                t = Browser(number, self.get_text_report_random(), email, self.proxy, self.who_report, uuid_order)
                t.start()
                threads.append(t)
            self.wait_threads(threads)
            numbers = numbers[self.thread_count:]

    @staticmethod
    def get_text_report_random():
        return random.choice(open(os.path.join(os.path.dirname(__file__), 'text.txt'), 'rb').readlines()).decode('utf-8')

    @staticmethod
    def wait_threads(ths):
        while True:
            flag = False
            for th in ths:
                flag = max(flag, th.is_alive())

            if not flag:
                return
            time.sleep(1)

    @staticmethod
    def generate_random_numbers(count_numbers):
        arr = []
        while count_numbers != len(arr):
            start_text = str(random.randint(900, 999))
            end_text = random.randint(1_000_000, 9_999_999)
            number = f'+7{start_text}{end_text}'

            if number not in arr:
                arr.append(number)

        return arr
