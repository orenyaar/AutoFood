# -*- coding: utf-8 -*-
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import webdriverwrapper


class OrderFood(object):
    def __init__(self):
        path_to_my_profile = "C:\\Users\\amirbl\\AppData\\Roaming\Mozilla\\Firefox\\Profiles\\7tr50x99.default"
        profile = FirefoxProfile(path_to_my_profile)
        self.driver = webdriverwrapper.Firefox(profile)
        self.driver.implicitly_wait(30)
        self.base_url = "http://wiki.checkpoint.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def goto_food_point(self):
        self.driver.get(self.base_url + "/confluence/")
        self.driver.find_element_by_css_selector("#FoodPoint > div").click()

        self.driver.wait_for_element(xpath="//h2")
        print (self.driver.get_elm(xpath="//h2").text)

    # def check_order_food(self, date):
    #     # parsed_date = date.replace("/", "_").replace("/", "_")
    #     #current_shift_obj = self.driver.get_elm(xpath='[id^= personalOrder_%s]' % parsed_date)
    #
    #     if u"הזמנת" in self.driver.get_elm(xpath="//h2").text:
    #         print "OK"
    #
    #     else:
    #         "not ok"
    #
    #     # self.driver.find_element_by_link_text(u"ההזמנות שלי").click()

    def order_food(self, rest_id, date, round_id, really=True):
        try:
            self.goto_food_point()
            # self.check_order_food(date)

            print ("goToRes('{rest_id}', '{date}', '{round_id}', 'Full')".format(rest_id=rest_id, date=date,
                                                                                 round_id=round_id))
            self.driver.execute_script(
                "goToRes('{rest_id}', '{date}', '{round_id}', 'Full')".format(rest_id=rest_id, date=date,
                                                                              round_id=round_id))
            self.driver.find_element_by_id("Continue").click()
            self.driver.find_element_by_id("selectDishFromLastOrderLink").click()

            if really:
                self.driver.execute_script("javascript:SubmitOrder()")
            else:
                self.driver.find_element_by_id("fancybox-close").click()
            print ("order succeeded")
        finally:
            self.tear_down()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tear_down(self):
        self.driver.quit()


if __name__ == "__main__":
    today = "{:%d/%m/%y}".format(datetime.now())
    OrderFood().order_food(rest_id='6969', date='15/06/2016', round_id='1', really=True)
