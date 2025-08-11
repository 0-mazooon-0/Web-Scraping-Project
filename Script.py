from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import selenium.common.exceptions as exceptions
import urllib
import os
import time as t


class Scraping_Images:

    def __init__(self, topic: str, *, download_path: str = None):

        if len(topic) < 1 or type(topic) != str:
            raise ValueError(
                "Your topic is too short or invalid please try another one.\n")
        else:
            self.topic = topic

        if download_path != None:
            if os.path.isdir(os.path.dirname(os.path.abspath(download_path))):
                path = download_path + f'\{topic}'
                os.makedirs(path, exist_ok=True)
                self.download_path = path
            else:
                raise ValueError(
                    "Your driver address is invalid or typed incorrectly please try again.\n"
                )

        else:
            path = os.path.dirname(os.path.abspath(__file__))
            path += f'\{topic}'
            os.makedirs(path, exist_ok=True)
            self.download_path = path

    def scrape(self):

        def download_image(url, filename):
            resource = urllib.request.urlopen(url)
            output = open(filename, "wb")
            output.write(resource.read())
            output.close()

        self.__window = webdriver.Chrome()
        self.__window.get(
            f"https://www.google.com/search?sxsrf=AE3TifOzKmAS32r4SRbjNst0HfZz4wyVsw:1754136543040&udm=2&q={self.topic}"
        )

        self.__main_code = self.__window.find_element(By.XPATH,
                                                      '//*[@id="rso"]/div')

        last_height = 0
        while 1:
            new_height = self.__window.execute_script(
                "return document.body.scrollHeight")
            self.__window.execute_script(
                f"window.scrollTo({last_height}, document.body.scrollHeight);")
            t.sleep(2)

            if last_height == new_height:
                break
            else:
                last_height = new_height

        self.__photo_tags = self.__main_code.find_elements(
            By.XPATH,
            '//*[@id="rso"]/div/div/div[1]/div/div/div/div[2]/h3/a/div/div/div/g-img/img'
        )
        self.__photo_src = []

        for x in self.__photo_tags:
            self.__photo_src.append(x.get_attribute('src'))

        self.__photos = 1
        for x in self.__photo_src:
            if len(x) < 90:
                continue
            path = self.download_path + f'\{self.__photos}.jpg'
            download_image(x, path)
            self.__photos += 1

        else:
            print(
                f"\nYour images are downloaded successfully.\nYou can find your photos at {self.download_path}\nThanks for your time <3 <3 !!\n"
            )

    def photo_count(self):
        try:
            print(f"There are {self.__photos} photos")
            print(f"There were {len(self.__photo_src)} photos")

        except Exception as exc:
            print(exc)


# You can try this
# myscrape1 = Scraping_Images('roberto carlos')

# myscrape1.scrape()
# myscrape1.photo_count()

# You can try this
# # myscrape2 = Scraping_Images('Messi',download_path = r"C:\Users\mazen ashraf\Desktop")

# myscrape2.scrape()
# myscrape2.photo_count()


