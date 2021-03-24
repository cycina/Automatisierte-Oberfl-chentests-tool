# Usage
# python screenshotsReference.py -u link -l CSS class
import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
import argparse
import time
from urllib.parse import urlparse
import os


# This little function make screen size to maximum for better screenshot result
def save_screenshot(driver, path, url, my_element):
    original_size = driver.get_window_size()
    time.sleep(2)
    required_width = driver.execute_script(
        'return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script(
        'return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    u = urlparse(url)
    try:
        driver.find_element_by_class_name(my_element).screenshot(
            path + "cons-body_" + os.path.basename(os.path.normpath((u.fragment)))+".png")  # Avoids scrollbar
    except Exception as e:
        print(e)


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help='delimited url input')
parser.add_argument('-l', '--element',
                    help='delimited element input', type=str)

args = parser.parse_args()
my_url = [url for url in args.url.split(',')]
my_elements = [element for element in args.element.split(',')]

out_path = "C:/Users/cyrin/OneDrive/Bureau/IC2/py/Screenshot/ref_img/"
for i in range(len(my_url)):
    url = my_url[i].replace("'", "")
    my_elements =my_elements[i].replace("'", "")
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
    save_screenshot(driver, out_path, url, my_elements)
    driver.close()

