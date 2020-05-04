from utils.logger import logger
from robot.libraries.BuiltIn import BuiltIn
import os
import time, datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import traceback

class WebUiBase(object):
    def __init__(self):
        print('uibase init')
        self.selib = BuiltIn().get_library_instance('SeleniumLibrary')
        self.download_path = BuiltIn().get_variable_value("${EXECDIR}")
   
    def get_page_screenshot(self):
        # 截图
        try:
            self.selib.capture_page_screenshot()
            #self.selib.save_screenshot("test2.png")
            print('Screen shot saved')
        except:
            print('Screen shot failed')
            logger.error('Screen shot failed')
    #从一堆里面点击第几个
    def click_index_from_webelements(self, locator, index):
        """点击第几个在获取的webelemnts中间
        :param  locator 参考robotframework规定
        """
        try:
            print('click_index_from_webelements', locator, index)
            items = self.get_elements(locator)
            if items:
                items[int(index)].click()
            else:
                print('no items found ' + locator)
        except:
            self.get_page_screenshot()
            print('exception happens')

 
   

    def create_chrome_webdriver(self, url, wait_timeout=10,implicit_wait=3, headless=False, download_path="",speed=0.3):
        '''
        创建chrome浏览器的webdriver
        :param url: 需要打开的网页地址
        :param wait_timeout:  selenium的wait时间
        :param implicit_wait: 元素的not found的等待时间
        :param headless: 是否无界面运行
        :param download_path: 下载目录,默认为运行目录
        :param speed: selenium运行速度,默认设为0.3秒
        :return:
        '''
        try:
            from selenium import webdriver
            from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
            if not download_path:
                download_path = self.download_path
            options = webdriver.ChromeOptions()

            opts = ['--no-sandbox', '--disable-dev-shm-usage', 'start-maximized', '--disable-infobars', '--disable-gpu',
                '--test-type', '--disable-extensions', '--ignore-certificate-errors', '--disable-user-media-security']
            if headless:
                opts.append('--headless')
            else:
                if os.getenv("USE_HEADLESS") == 'True':
                    opts.append('--headless')
            for opt in opts:
                options.add_argument(opt)

            prefs = {'download.default_directory': download_path,
                'download.prompt_for_download': 'false'}
            options.add_experimental_option("prefs", prefs)
            capabilities = DesiredCapabilities.CHROME
            capabilities['goog:loggingPrefs'] =  {"driver": "INFO", "server": "OFF", "browser": "ALL"}
            self.selib.create_webdriver('Chrome', desired_capabilities=capabilities, chrome_options=options)
            self.selib.go_to(url)
            self.selib.set_selenium_speed(speed)
            self.selib.set_selenium_implicit_wait(implicit_wait)
            self.selib.set_selenium_timeout(wait_timeout)
        except AssertionError:
            print("Error happens")
            logger.error('Error happens when create driver')

    def close_chrome_browser(self):
        '''
        关闭浏览器,内容加入了判断失败的内容,所以需要在teardown里面调用
        :return:
        '''
        result = 'FAIL'
        case_id = 'None'
        try:
            pass
            #result = BuiltIn().get_variable_value("${TEST STATUS}")
            #case_id = BuiltIn().get_variable_value("${TEST NAME}")
            #if 'FAIL' in result:
                #BuiltIn().log(self.get_selenium_browser_log())
        finally:
            pass
        try:
            selib = BuiltIn().get_library_instance('SeleniumLibrary')
            selib.close_all_browsers()
        except Exception as ex:
            print(ex)

