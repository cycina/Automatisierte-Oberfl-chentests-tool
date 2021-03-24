# Usage
#  python screenshotLayoutElements.py -u link
import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
import argparse
import time
from urllib.parse import urlparse
import os


# This little function make screen size to maximum for better screenshot result
def save_screenshot(driver, path, url, classname):
    original_size = driver.get_window_size()
    time.sleep(2)
    time.sleep(3)
    required_width = driver.execute_script(
        'return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script(
        'return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    u = urlparse(url)
    try:
        driver.find_element_by_class_name(classname).screenshot(
            path + "cons-"+classname.split('-')[1]+".png")  # Avoids scrollbar
    except Exception as e:
        print(e)
    driver.set_window_size(original_size['width'], original_size['height'])


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help='delimited url input')

args = parser.parse_args()
my_url = [url for url in args.url.split(',')]


out_path = "C:/Users/cyrin/OneDrive/Bureau/IC2/py/Screenshot/test_img/"
for url in my_url:
    url = url.replace("'", "")
    capabilities = webdriver.DesiredCapabilities().FIREFOX
    # This is for accepting self signed SSl certificates.
    capabilities['acceptSslCerts'] = True
    opts = Options()
    opts.headless = True
    driver = webdriver.Firefox(
        firefox_options=opts, executable_path="C:/Users/cyrin/OneDrive/Bureau/IC2/py/geckodriver/geckodriver.exe")
    driver.capabilities = capabilities
    driver.get(url)
    # Saving the screenshot
    save_screenshot(driver, out_path, url, 'c-sidebar')
    save_screenshot(driver, out_path, url, 'c-header')  # Saving the screenshot
    save_screenshot(driver, out_path, url, 'c-footer')  # Saving the screenshot

    driver.close()
