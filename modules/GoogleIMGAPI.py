# -*- coding: UTF-8 -*-

'''
Created on Apr 28, 2020

@author: shijingsheng
'''

from base.WebUiBase import WebUiBase
from time import sleep
from utils.logger import logger
from utils.util import *
import requests
import re, os
from requests_toolbelt.multipart.encoder import MultipartEncoder
from collections import OrderedDict
from urllib3 import encode_multipart_formdata
import time, json
import datetime

class GoogleIMGAPI(WebUiBase):
    def __init__(self):
        WebUiBase.__init__(self)


    def Step1(self,url,text,result):
        #create chrome
        self.create_chrome_webdriver(url)
        sleep(0.5)
        #click images to search images
        self.selib.click_element("//*[@id='gbw']/div/div/div[1]/div[2]/a")

        #input the string to search
        self.selib.input_text("//*[@id='sbtc']/div/div[2]/input", text)

        #click serach button
        self.selib.click_element("//*/input")
        sleep(2)
        #parameter of the number
        strings="//*[@id='islrg']/div[1]/div[" + result + "]"
        self.selib.click_element(strings)
        sleep(0.5)

        sleep(0.5)
        self.get_page_screenshot()
        sleep(0.5)
if __name__ == "__main__":
    t = GoogleIMGAPI()
    t.Step1()

'''
  resulten = self.wait_element_present("//span[contains(text(),'Images')]", 20)
        resultcn = self.wait_element_present("//span[contains(text(),'图片')]", 20)
        if not (resulten or resultcn):
            print('not found images')
        return False
class CmsModule(WebUiBase):




    def open_item(self, item, folder):
        print('打开{}下的{}'.format(folder, item))
        folder_xpath = "//li[@class='treeview'][contains(., '{}')]".format(folder)
        item_xpath = "//li[@class='treeview active'][contains(., '{}')]//ul//li/a[contains(.,'{}')]".format(folder, item)
        if not self.wait_element_visible(item_xpath, timeout=3):
            self.click_locator(folder_xpath)
            sleep(0.4)
        self.click_by_js(item_xpath)

    def add_media_info(self, title, author,category, keyword="", video='', picture="", audio="", readsec=10, season=1):
        self.selib.select_frame("mainFrame")
        try:
            self.selib.click_link("//a[@href='/news/add']")
            self.selib.input_text('id:title', title)
            self.selib.input_text("id:author", author)
            if keyword:
                self.selib.input_text("id:keyword", keyword)
            self.selib.input_text("id:time_span", readsec)
            self.selib.click_element("id:departmentID")
            self.click_locator("//li[contains(@id, 'col_departmentID')]/span[text()='{}']".format(category))

            self.selib.input_text("id:describe", season)

            if video:
                video_file = os.path.join(config.root_dir, 'data', video)
                self.selib.choose_file("id:videourl", video_file)

            if audio:
                audio_file = os.path.join(config.root_dir, 'data', audio)
                self.selib.choose_file("id:audiourl", audio_file)
            if picture:
                pic = os.path.join(config.root_dir, 'data', picture)
                self.selib.choose_file("id:img_url", pic)
            self.selib.click_element("name:submit")
            result = self.wait_element_present("//*[contains(text(),'添加成功')]", timeout=6)
            print('添加内容状态', result)
            self.selib.unselect_frame()
            return result
        finally:
            self.selib.unselect_frame()

    def search_title(self, title):
        self.wait_element_present("mainFrame", timeout=5)
        self.selib.select_frame("mainFrame")
        try:
            self.selib.input_text("id:search_title", title)
            self.selib.click_element("id:search_btn")
            row_xpath = "//a[text()='{}']/../..".format(title)
            return self.wait_element_present(row_xpath, timeout=3)
        except Exception as ex:
            print(ex)
            return False
        finally:
            self.selib.unselect_frame()

    def get_media_result(self, title):
        self.wait_element_present("mainFrame", timeout=5)
        self.selib.select_frame("mainFrame")
        try:
            row_xpath = "//a[text()='{}']/../..".format(title)
            audio_result = "{}/td[5]".format(row_xpath)
            video_result = "{}/td[4]".format(row_xpath)
            if not self.wait_element_present(row_xpath, timeout=3):
                print('不存在这个'+title)
                return False
            audio = self.selib.get_text(audio_result)
            video_url = self.selib.get_text(video_result)
            print(video_url, audio)
            return video_url, audio

        finally:
            self.selib.unselect_frame()

    def media_content_operation(self, title, action='audit'):
        self.wait_element_present("mainFrame", timeout=5)
        self.selib.select_frame("mainFrame")
        try:
            row_xpath = "//a[text()='{}']/../..".format(title)
            audit_btn = "{}/td[7]".format(row_xpath)
            audiot_btn_status = "{}/td[7]/a".format(row_xpath)
            sync_status = "{}/td[8]".format(row_xpath)
            edit = "{}/td[10]/a[1]".format(row_xpath)
            delete = "{}/td[10]/a[2]".format(row_xpath)
            audio_result = "{}/td[5]".format(row_xpath)
            video_result = "{}/td[4]".format(row_xpath)
            if not self.wait_element_present(row_xpath, timeout=3):
                print('不存在这个'+title)
                return False
            if action == 'audit':
                if self.selib.get_element_attribute(audiot_btn_status, 'data-status') == 'yes':
                    print('已经audit')
                    return True
                self.selib.click_element(audit_btn)
                self.selib.handle_alert()
                sleep(10)
                return self.selib.get_text(sync_status) == '成功'

            if action == 'delete':
                self.selib.click_element(delete)
                self.selib.handle_alert()
                result = self.wait_element_present("//*[contains(text(),'删除成功')]", timeout=6)
                self.selib.unselect_frame()
                return result
        except Exception as ex:
            print(ex)
            return False
        finally:
            self.selib.unselect_frame()

    def create_faq_category(self, cate_name, sort):
        self.selib.select_frame("mainFrame")
        try:
            self.selib.click_link("//a[@href='/fqacate/add']")
            self.selib.input_text('id:cate_name', cate_name)
            self.selib.click_element("id:parent_id")
            # 选择第一个category
            self.click_locator("//ul[@class='dropmenu menuH']/li[1]")
            self.selib.input_text("id:sort",sort)
            self.selib.click_element("name:addbtn")
            result_exist = self.wait_element_present("//*[contains(text(),'分类名称已存在')]", timeout=6)
            if result_exist:
                print('分类名称已存在')
                return '分类名称已存在'
            result = self.wait_element_present("//*[contains(text(),'添加成功')]", timeout=6)
            print('添加内容状态', result)
            self.selib.unselect_frame()
            return result
        finally:
            self.selib.unselect_frame()

    def search_faq(self,title):
        self.wait_element_present("mainFrame", timeout=5)
        self.selib.select_frame("mainFrame")
        try:
            self.selib.input_text("id:search_title", title)
            self.selib.click_element("id:search_btn")
            self.selib.unselect_frame()
            return self.wait_page_contains(title,timeout=3)
        except Exception as ex:
            print(ex)
            return False
        finally:
            self.selib.unselect_frame()

    def add_faq(self, title, question, answer):
        self.selib.select_frame("mainFrame")
        try:
            self.selib.click_link("//a[@href='/fqaitem/add']")
            self.selib.input_text('id:title', title)
            self.selib.click_element("id:parent_id")
            self.click_locator("//ul[contains(@class,'dropmenu menuH')]/li[1]")
            self.selib.input_text("name:qs", question)
            self.selib.input_text("name:as", answer)
            self.selib.click_element("id:fqaemoji")
            self.click_locator("//option[2]")
            self.selib.click_element("name:submit")
            result = self.wait_element_present("//*[contains(text(),'添加成功')]", timeout=6)
            print('添加内容状态', result)
            self.selib.unselect_frame()
            return result
        finally:
            self.selib.unselect_frame()

    def del_faq(self,title):
        self.wait_element_present("mainFrame", timeout=5)
        self.selib.select_frame("mainFrame")
        try:
            row_xpath = "//a[text()='{}']/../..".format(title)
            delete = "{}/td[7]/a[2]".format(row_xpath)
            if not self.wait_element_present(row_xpath, timeout=3):
                print('不存在这个' + title)
                return False
            self.selib.click_element(delete)
            self.selib.handle_alert()
            result = self.wait_element_present("//*[contains(text(),'删除成功')]", timeout=6)
            self.selib.unselect_frame()
            return result
        except Exception as ex:
            print(ex)
            return False
        finally:
            self.selib.unselect_frame()

    def get_faq_synch_status(self, title):
        self.wait_element_present("mainFrame", timeout=5)
        self.selib.select_frame("mainFrame")
        try:
            row_xpath = "//a[text()='{}']/../..".format(title)
            audit_status = "{}/td[5]".format(row_xpath)
            if not self.wait_element_present(row_xpath, timeout=3):
                print('不存在这个'+title)
                return False
            status = self.selib.get_text(audit_status)
            print(status)
            return status
        finally:
            self.selib.unselect_frame()

    def faq_audit(self,title):
        self.wait_element_present("mainFrame", timeout=5)
        self.selib.select_frame("mainFrame")
        try:
            row_xpath = "//a[text()='{}']/../..".format(title)
            audit = "{}/td[4]".format(row_xpath)
            if not self.wait_element_present(row_xpath, timeout=3):
                print('不存在这个' + title)
                return False
            self.selib.click_element(audit)
            self.selib.handle_alert()
            self.selib.unselect_frame()
            return True
        except Exception as ex:
            print(ex)
            return False
        finally:
            self.selib.unselect_frame()

    def chitchat_search(self, question='',answer=''):
        """
        闲聊搜索,
        :param question:
        :param answer:
        :return:
        """
        print('chitchat_search', question, answer)
        self.common_switch_frame()
        try:
            if not (question or answer):
                logger.error('question,answer至少一个不为空')
                self.common_switch_frame(False)
                return False
            if question:
                self.selib.input_text('id:req', question)
            if answer:
                self.selib.input_text('id:res', answer)
            self.selib.click_element('id:go')
            ret = self.wait_element_present('id:story_id')
            self.common_switch_frame(False)
            return ret
        except Exception as ex:
            print(ex)
            self.common_switch_frame(False)
            return False

    def chitchat_delete(self, question='', answer='', delete_all=False):
        print('chitchat_delete', question,answer)
        if not self.chitchat_search(question, answer):
            logger.info('没有发现这个question')
            print('没有发现这个question')
            return True
        self.common_switch_frame()
        # 删除第一个
        try:
            if delete_all:
                for element in self.selib.get_webelements('class:tab_del'):
                    self.selib.click_element(element)
                    self.selib.handle_alert()
                    self.wait_element_present("//*[contains(text(),'删除成功')]", timeout=6)
                    if self.chitchat_search(question, answer):
                        self.common_switch_frame()
                        continue
                    else:
                        self.common_switch_frame()
                        break
                ret = self.chitchat_search(question, answer)
                return not ret
            else:
                self.selib.click_element('class:tab_del')
                self.selib.handle_alert()
                result = self.wait_element_present("//*[contains(text(),'删除成功')]", timeout=6)
                self.common_switch_frame(False)
                return result
        except Exception as ex:
            print(ex)
            self.common_switch_frame(False)
            return False
        finally:
            self.selib.unselect_frame()

    def chitchat_sync_status(self):
        """
        同步状态,多个是指第一个,必须先搜索
        :return:
        """
        self.common_switch_frame()
        try:
            actual = self.selib.get_text("xpath://td[@class='td_center'][2]")
            self.common_switch_frame(False)
            if '成功' in actual:
                return True
            elif '失败' in actual:
                return False
            else:
                assert False, '状态不可知'
        except Exception as ex:
            print(ex)
            self.common_switch_frame(False)
            return False

    def chitchat_audit(self, status=True):
        """
        审核, 必须先搜索到,取第一个
        :param status:
        :return:
        """
        print('chitchat_audit', status)
        self.common_switch_frame()
        try:
            if not self.wait_element_present('xpath://a[@data-status]'):
                print('没有发现审核按钮')
                logger.error('没有发现审核按钮')
                self.common_switch_frame(False)
                return False
            audit_btn = 'xpath://a[@data-status]'
            pre_status = self.selib.get_element_attribute(audit_btn, 'data-status')
            if 'yes' in pre_status:
                if status:
                    self.click_locator(audit_btn)
                    self.selib.handle_alert()
                    sleep(0.3)
                    self.click_locator(audit_btn)
                else:
                    self.click_locator(audit_btn)
            else:
                if status:
                    self.click_locator(audit_btn)
                else:
                    self.click_locator(audit_btn)
                    self.selib.handle_alert()
                    sleep(0.3)
                    self.click_locator(audit_btn)
            self.selib.handle_alert()
            sleep(1)
            self.common_switch_frame(False)
            return self.chitchat_sync_status()
        except Exception as ex:
            print(ex)
            self.common_switch_frame(False)
            return False

    def chitchat_add(self, question, answer):
        print('chitchat_add', question, answer)
        try:
            self.common_switch_frame()
            self.selib.click_link('/thirdchat/add')
            self.selib.input_text('id:request', question)
            self.selib.input_text("id:response", answer)
            sleep(0.5)
            self.selib.click_element('name:submit')
            result = self.wait_element_present("//*[contains(text(),'添加成功')]", timeout=6)
            print('添加内容状态', result)
            self.common_switch_frame(False)
            return result
        except Exception as ex:
            print(ex)
            self.common_switch_frame(False)
            return False

    def common_switch_frame(self, status=True):
        try:
            if status:
                self.wait_element_present("mainFrame", timeout=5)
                self.selib.select_frame("mainFrame")
            else:
                self.selib.unselect_frame()
        except Exception as ex:
            print(ex)

    def story_search(self, title="", content=""):
        print("story_search", title, content)
        self.common_switch_frame()
        try:
            if not title+content:
                print('title and content should be not empty')
            if title:
                self.selib.input_text("id:title", title)
            if content:
                self.selib.input_text("name:content", content)
            self.selib.click_element("id:go")
            if not self.wait_element_present("//td[@class='td_cont']/p", timeout=2):
                print('无内容查到')
                self.common_switch_frame(False)
                return False
            actual_content = self.selib.get_text("//td[@class='td_cont']/p")
            actual_title = self.selib.get_text("//td[@class='td_title']/a")
            print(actual_title, actual_content)
            if title and content:
                self.common_switch_frame(False)
                return title in actual_title and content in actual_content
            elif title:
                self.common_switch_frame(False)
                return title in actual_title
            elif content:
                self.common_switch_frame(False)
                return content in actual_content
            else:
                self.common_switch_frame(False)
                return False
        except Exception as ex:
            print(ex)
            self.common_switch_frame(False)
            return False

    def story_action(self, title, action='audit', status=True):
        """
        story action操作, 需要查询后操作
        :param action: audit, audit_log, sync_log, edit, delete, 目前支持audit和delete两种
        :param status
        :return:
        """
        row_rest = "//td[@class='td_title']/a[text()='{}']/../..".format(title)
        audit_btn = "{}/td[6]/a".format(row_rest)
        sync_status = "{}/td[7]".format(row_rest)
        audit_log = "{}/td[8]/a[1]".format(row_rest)
        sync_log = "{}/td[8]/a[1]".format(row_rest)
        edit_btn = "{}/td[9]/a[1]".format(row_rest)
        delete_btn = "{}/td[9]/a[2]".format(row_rest)
        self.common_switch_frame()
        if not self.wait_element_present(row_rest, timeout=3):
            print('没有搜到', title)
            logger.error("没有搜到{}".format(title))
            return False
        try:
            if action == "audit": #审核
                pre_status = self.selib.get_element_attribute(audit_btn, 'data-status')
                if 'no' in pre_status:
                    if status:
                        self.click_locator(audit_btn)
                        self.selib.handle_alert()
                    else:
                        self.click_locator(audit_btn)
                        self.selib.handle_alert()
                        self.click_locator(audit_btn)
                        self.selib.handle_alert()
                else:
                    if status:
                        self.click_locator(audit_btn)
                        self.selib.handle_alert()
                        self.click_locator(audit_btn)
                        self.selib.handle_alert()
                    else:
                        self.click_locator(audit_btn)
                        self.selib.handle_alert()
                sleep(5)
                sync = self.selib.get_text(sync_status)
                self.common_switch_frame(False)
                return "成功" in sync

            elif action == 'delete': #删除
                self.click_locator(delete_btn)
                self.selib.handle_alert()
                result = self.wait_element_present("//*[contains(text(),'删除成功')]", timeout=6)
                print('删除状态', result)
                self.common_switch_frame(False)
                return result
        except Exception as ex:
            print(ex)
            self.common_switch_frame(False)
            return False

    def story_add(self, title, story_type, content):
        try:
            self.common_switch_frame()
            self.selib.click_link("/story/add")
            self.selib.input_text("id:title", title)
            self.selib.input_text("name:content", content)
            self.selib.execute_javascript('document.querySelector("#form>fieldset>p:nth-child(3)>select").value="{}"'.format(story_type))
            sleep(0.3)
            print('选择其他故事')
            self.click_locator("class:review_wrap")
            self.click_locator("name:submit")
            print('提交')
            result = self.wait_element_present("//*[contains(text(),'添加成功')]", timeout=6)
            print('添加内容状态', result)
            assert result, "添加内容状态shibai"
            row_rest = "//td[@class='td_title']/a[text()='{}']/../..".format(title)
            sync_status = "{}/td[7]".format(row_rest)
            assert self.wait_element_present(row_rest),"添加内容后未出现在首页"
            assert "成功" in self.selib.get_text(sync_status), "新建故事同步失败"
        except Exception as ex:
            print(ex)
            self.common_switch_frame(False)
            return False

    #技能管理-笑话-添加
    def add_joke_info(self, category, content):
        self.selib.select_frame("mainFrame")
        try:
            self.selib.click_link("//a[@href='/joke/add']")
            self.click_locator("//select[@id='tag']//option[@value='{}']".format(category))
            self.selib.input_text("name:content", content)
            self.selib.click_element("name:submit")
            result = self.wait_element_present("//*[contains(text(),'添加成功')]", timeout=6)
            print('添加内容状态', result)
            self.selib.unselect_frame()
            return result
        finally:
            self.selib.unselect_frame()

    # 技能管理-笑话-搜索
    def joke_search_content(self, content):
        self.wait_element_present("mainFrame", timeout=5)
        self.selib.select_frame("mainFrame")
        try:
            self.selib.input_text("id:title", content)
            self.selib.click_element("id:go")
            row_xpath = "//p[contains(text(),'{}')]/../..".format(content)
            return self.wait_element_present(row_xpath, timeout=3)
        except Exception as ex:
            print(ex)
            return False
        finally:
            self.selib.unselect_frame()

    # 技能管理-笑话-内容获取
    def get_joke_result(self, content):
        self.wait_element_present("mainFrame", timeout=5)
        self.selib.select_frame("mainFrame")
        try:
            row_xpath = "//p[contains(text(),'{}')]/../..".format(content)
            joke_content = "{}/td[3]".format(row_xpath)
            joke_id = "{}/td[2]".format(row_xpath)
            if not self.wait_element_present(row_xpath, timeout=3):
                print('不存在这个'+content)
                return False
            joke_content_result = self.selib.get_text(joke_content)
            joke_id_result = self.selib.get_element_attribute(joke_id,"title")
            print(joke_id_result.split(":",1)[0],joke_content_result)
            return joke_id_result.split(":",1)[1],joke_content_result

        finally:
            self.selib.unselect_frame()

    # 技能管理-笑话-操作处理：审核，删除
    def joke_content_operation(self, content, action='audit'):
        self.wait_element_present("mainFrame", timeout=5)
        self.selib.select_frame("mainFrame")
        try:
            row_xpath = "//p[contains(text(),'{}')]/../..".format(content)
            audit_btn = "{}/td[5]".format(row_xpath)
            audiot_btn_status = "{}/td[5]/a".format(row_xpath)
            sync_status = "{}/td[6]".format(row_xpath)
            edit = "{}/td[8]/a[1]".format(row_xpath)
            delete = "{}/td[8]/a[2]".format(row_xpath)
            if not self.wait_element_present(row_xpath, timeout=3):
                print('不存在这个'+content)
                return False
            if action == 'audit':
                if self.selib.get_element_attribute(audiot_btn_status, 'data-status') == 'yes':
                    print('已经audit')
                    return True
                self.selib.click_element(audit_btn)
                self.selib.handle_alert()
                sleep(10)
                return self.selib.get_text(sync_status) == '成功'

            if action == 'delete':
                self.selib.click_element(delete)
                self.selib.handle_alert()
                result = self.wait_element_present("//*[contains(text(),'删除成功')]", timeout=6)
                self.selib.unselect_frame()
                return result
        except Exception as ex:
            print(ex)
            return False
        finally:
            self.selib.unselect_frame()


    def add_poem_author(self, name, dynasty, alias, abstract):
        self.selib.select_frame("mainFrame")
        try:
            self.selib.click_link("//a[@href='/poetryauthor/add']")
            self.selib.input_text('id:name', name)
            self.selib.click_element("id:dynasty")
            self.selib.click_element("//select[@id='dynasty']/option[text()='{}']".format(dynasty))
            self.selib.input_text('id:alias', alias)
            self.selib.input_text('id:abstract', abstract)
            self.selib.click_element("name:submit")
            result = self.wait_element_present("//*[contains(text(),'添加成功')]", timeout=6)
            print('添加古诗词作者状态', result)
            self.selib.unselect_frame()
            return result
        finally:
            self.selib.unselect_frame()

    def delete_poem_author(self, name):
        self.wait_element_present("mainFrame", timeout=5)
        self.selib.select_frame("mainFrame")
        try:
            row_xpath = "//a[text()='{}']/../..".format(name)
            if row_xpath:
                delete = "{}/td[6]/a[2]".format(row_xpath)
                self.selib.click_element(delete)
                self.selib.handle_alert()
                result = self.wait_element_present("//*[contains(text(),'删除成功')]", timeout=6)
                self.selib.unselect_frame()
                return result
            else:
                print('找不到该作者')
        except:
            print("该作者不存在")
        finally:
            self.selib.unselect_frame()


    def add_poem(self, title, author, dynasty, category, tagname, contents, phrase, translate):
        self.selib.select_frame("mainFrame")
        try:
            self.selib.click_link("//a[@href='/poetry/add']")
            self.selib.input_text('id:title', title)
            self.selib.input_text('id:name', author)
            self.selib.press_keys('id:name', 'TAB')
            sleep(5)
            self.selib.click_element("id:dynasty")
            self.selib.click_element("//select[@id='dynasty']/option[text()='{}']".format(dynasty))
            self.selib.click_element("id:type")
            self.selib.click_element("//select[@id='type']/option[text()='{}']".format(category))
            self.selib.input_text('id:tagname', tagname)
            self.selib.input_text('id:contents', contents)
            self.selib.input_text('id:phrase', phrase)
            self.selib.input_text('id:translate', translate)
            self.selib.click_element("name:submit")
            result = self.wait_element_present("//*[contains(text(),'添加成功')]", timeout=6)
            print('添加古诗词信息状态', result)
            self.selib.unselect_frame()
            return result
        finally:
            self.selib.unselect_frame()

    def get_poem_result(self, title):
        self.wait_element_present("mainFrame", timeout=5)
        self.selib.select_frame("mainFrame")
        try:
            row_xpath = "//a[text()='{}']/../..".format(title)
            author_result = "{}/td[4]".format(row_xpath)
            content_result = "{}/td[5]".format(row_xpath)
            category_result = "{}/td[6]".format(row_xpath)
            tagname_result = "{}/td[7]".format(row_xpath)
            if not self.wait_element_present(row_xpath, timeout=3):
                print('不存在这个' + title)
                return False
            author = self.selib.get_text(author_result)
            content = self.selib.get_text(content_result)
            category = self.selib.get_text(category_result)
            tagname = self.selib.get_text(tagname_result)

            print(author, content, category, tagname)
            return author, content, category, tagname

        finally:
            self.selib.unselect_frame()

    def poem_content_operation(self, title, action='audit'):
        self.wait_element_present("mainFrame", timeout=5)
        self.selib.select_frame("mainFrame")
        # self.selib.current_frame_should_contain('张宗昌')
        row_xpath = "//a[text()='{}']/../..".format(title)
        poem_audit_btn = "{}/td[8]".format(row_xpath)        #审核功能
        poem_audiot_btn_status = "{}/td[8]/a".format(row_xpath)
        poem_sync_status = "{}/td[9]".format(row_xpath)
        edit = "{}/td[11]/a[1]".format(row_xpath)
        delete = "{}/td[11]/a[2]".format(row_xpath)     # 删除功能
        if not self.wait_element_present(row_xpath, timeout=3):
            print('不存在这个' + title)
            return False
        if action == 'audit':
            if self.selib.get_element_attribute(poem_audiot_btn_status, 'data-status') == 'yes':
                print('已经audit')
                return True
            self.selib.click_element(poem_audit_btn)
            print('开始审核')
            self.selib.handle_alert()
            print("确认审核")
            sleep(5)
            assert self.selib.get_text(poem_sync_status) == '成功'
            # return self.selib.get_text(poem_sync_status) == '成功'
            print('同步成功')

        if action == 'delete':
            self.selib.click_element(delete)
            self.selib.handle_alert()
            result = self.wait_element_present("//*[contains(text(),'删除成功')]", timeout=6)
            self.selib.unselect_frame()
            return result

        self.selib.unselect_frame()
        print('退出mainframe')
'''
