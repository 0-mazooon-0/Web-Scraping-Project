from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.service import Service
import urllib
from os import getcwd, makedirs
import time as t

def download_image(url, filename):
    resource = urllib.request.urlopen(url)
    output = open(filename,"wb")
    output.write(resource.read())
    output.close()

window = webdriver.Chrome()
topic = 'manchester united'
window.get(f"https://www.google.com/search?sxsrf=AE3TifOzKmAS32r4SRbjNst0HfZz4wyVsw:1754136543040&udm=2&q={topic}")
t.sleep(3)

main_code = window.find_element(By.ID, 'main').find_element(By.ID, 'cnt').find_element(By.CLASS_NAME, 'MjjYud').find_element(By.XPATH, '//*[@id="rso"]/div/div/div[1]/div/div')

last_height = 0

while 1:
    new_height = window.execute_script("return document.body.scrollHeight")
    window.execute_script(f"window.scrollTo({last_height}, document.body.scrollHeight);")
    t.sleep(3)

    if last_height == new_height:
        break
    else:
        last_height = new_height

photo_tags = main_code.find_elements(By.XPATH, '//*[@id="rso"]/div/div/div[1]/div/div/div/div[2]/h3/a/div/div/div/g-img/img')
photo_src = []

for x in photo_tags:
    photo_src.append( x.get_attribute('src') )

print(len(photo_src))

for i,src in enumerate(photo_src):
    if len(src) <= 90:
        photo_src.pop(i)
    if src == "data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==":
        photo_src.pop(i)

print(len(photo_src))

file_dir = r"C:\Users\mazen ashraf\Desktop" + f"\{topic}"
makedirs(file_dir, exist_ok = True)

txt_dir = r"C:\Users\mazen ashraf\Desktop" + f"\{topic}.txt"
text = open(txt_dir, 'w')
text.close()

for i, x in enumerate(photo_src):
    path = file_dir + f'\{i+1}.jpg'
    download_image(x, path)
    
    text = open(txt_dir, 'a')
    text.write(f"{i}. {x}\n============================================================\n")
    text.close()

