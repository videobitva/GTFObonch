from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import NoSuchElementException
from time import sleep, time
from datetime import datetime

BONCH_USERNAME = ""
BONCH_PASSWORD = ""

GOOGLE_USERNAME = ""
GOOGLE_PASSWORD = ""

login_success = "https://lk.sut.ru/cabinet/?login=yes"
magic_link = "https://lk.sut.ru/cabinet/project/cabinet/forms/raspisanie.php"
oh_no = "У Вас нет прав доступа. Или необходимо перезагрузить приложение.."

driver_path = "/Users/beatrice.raw/Downloads/geckodriver"


# Strategy: normal -- full, eager -- no css, none -- only html


class GTFObonch:
    def __init__(self, bonch_username, bonch_password, google_username, google_password, driver, firefox=False, chrome=False,
                 strategy="normal"):
        self.bonch_username = bonch_username
        self.bonch_password = bonch_password
        self.google_username = google_username,
        self.google_password = google_password,
        self.timetable = []

        self.lk_ready = False
        self.google_ready = False

        self.browser = None

        self.lk_handle = None
        self.google_handle = None

        if firefox:
            options = FirefoxOptions()
            options.page_load_strategy = strategy
            options.add_argument("--incognito")
            # options.add_argument("--use-fake-device-for-media-stream")
            # options.add_argument("--use-fake-ui-for-media-stream")
            self.browser = webdriver.Firefox(executable_path=driver, options=options)
        elif chrome:
            options = ChromeOptions()
            options.page_load_strategy = strategy
            options.add_argument("--incognito")
            # options.add_argument("--use-fake-device-for-media-stream")
            # options.add_argument("--use-fake-ui-for-media-stream")
            self.browser = webdriver.Chrome(executable_path=driver, options=options)
        else:
            raise ValueError("No browser type specified!")

    def login(self):
        if self.lk_handle is None:
            self.lk_handle = self.browser.current_window_handle

        self.browser.get("https://lk.sut.ru/")
        self.browser.find_element_by_id("users").send_keys(self.bonch_username)
        self.browser.find_element_by_id("parole").send_keys(self.bonch_password)
        self.browser.find_element_by_id("logButton").click()

    def login_google(self, link):
        return
        self.browser.get("https://meet.google.com/ytc-igti-scn")

        login_button = self.browser.find_element_by_xpath("Войти")
        print(f"login google button{login_button.text}")
        # self.browser.find_element_by_id("password").send_keys(self.google_password)
        # self.browser.find_element_by_id("loginbtn").click()
        # self.check_session_state()

    def commit_classes(self):
        self.browser.switch_to.window(self.lk_handle)
        self.browser.get("https://lk.sut.ru/cabinet")

        study = self.browser.find_element_by_id("heading1")
        study.click()

        timetable = self.browser.find_element_by_id("menu_li_6118")
        timetable.click()

        sleep(0.5)

        for i in range(5):
            try:
                table = self.browser.find_element_by_class_name("simple-little-table").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
                break
            except Exception:
                sleep(0.5)
        else:
            raise ValueError("Can not locate class start button!")

        for i, el in enumerate(table, 1):
            columns = el.find_elements_by_tag_name("td")
            if len(columns) > 1:
                start_stop = columns[0].text.split()[-1][1:-1].split("-")
                distant = True if columns[2].text == "Дистанционно" else False

                start = datetime.strptime(start_stop[0], '%H:%M').time()
                stop = datetime.strptime(start_stop[1], '%H:%M').time()
                now = datetime.now().time()

                if start <= now <= stop:
                    try:
                        if distant:
                            self.login_google(columns[4].find_element_by_tag_name("a").get_property("href"))
                    except NoSuchElementException:
                        pass

                    try:
                        columns[4].find_element_by_tag_name("span").find_element_by_tag_name("a").click()
                    except NoSuchElementException:
                        pass

    def check_session_state(self):
        self.browser.get("https://lk.sut.ru/cabinet/project/cabinet/forms/raspisanie.php")
        if self.browser.find_element_by_tag_name("body").text == oh_no:
            self.lk_ready = False
        else:
            self.lk_ready = True

    def close(self):
        self.browser.quit()


if __name__ == "__main__":
    ara_ara = GTFObonch(BONCH_USERNAME, BONCH_PASSWORD, GOOGLE_USERNAME, GOOGLE_PASSWORD, driver_path, firefox=True, strategy="normal")
    ara_ara.login()
    ara_ara.commit_classes()
    ara_ara.close()
