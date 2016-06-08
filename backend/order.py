# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import webdriverwrapper


class OrderFood(object):
    def __init__(self):
        self.driver = webdriverwrapper.Ie()
        self.driver.implicitly_wait(30)
        self.base_url = "http://wiki.checkpoint.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def order_food(self):
        driver = self.driver
        driver.get(self.base_url + "/confluence/")
        driver.find_element_by_css_selector("#FoodPoint > div").click()

        driver.wait_for_element(xpath="//h2")
        print (driver.get_elm(xpath="//h2"))
        driver.find_element_by_xpath(u"(//img[@alt='בצע הזמנה'])[19]").click()
        driver.find_element_by_id("Continue").click()
        driver.find_element_by_id("OrderCancelationBtn").click()
        driver.find_element_by_id("selectDishFromLastOrderLink").click()
        driver.find_element_by_id("fancybox-close").click()

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
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    OrderFood().order_food()
