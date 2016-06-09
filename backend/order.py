# -*- coding: utf-8 -*-
import smtplib
import time
from datetime import datetime

import webdriverwrapper
from selenium.webdriver import FirefoxProfile

MSG_TEMPLATE = """From: Auto_Food <olegb@lacoon.com>
To: To Person <{to}>
MIME-Version: 1.0
Content-type: text/html
Subject: Your food was ordered by Auto-Food.

<b>{msg}</b>
<h2>{rest}</h2>
<br/>
<img src="http://i.imgur.com/UNdb1p0.gif"  >
"""

RESTS = {
    "BBB": "6969",
    "SOHO": "4801",
    "Salad Neto": "12096",
    "Diana": "1015",
    "Prusot": "11832",
    "Lehem Vered": "3684"
}

def get_rest_number_by_code(code):
    for key, val in RESTS.iteritems():
        if val == code:
            return key

    return "UNKNOWN REST"

class OrderFood(object):
    def set_up(self, browser="FIREFOX"):
        if browser=='IE':
            self.driver = webdriverwrapper.Ie()
        else:
            path_to_my_profile = "C:\\Users\\amirbl\\AppData\\Roaming\Mozilla\\Firefox\\Profiles\\7tr50x99.default"
            profile = FirefoxProfile(path_to_my_profile)
            self.driver = webdriverwrapper.Firefox(profile)
        self.driver.implicitly_wait(30)
        self.base_url = "http://wiki.checkpoint.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def send_email(self, to, message, code):
        msg = MSG_TEMPLATE.format(to=to, msg=message, rest=get_rest_number_by_code(code))
        print (msg)
        fromaddr = 'auto_food@gmail.com'
        toaddrs = 'amirb@lacoon.com'

        # Credentials (if needed)
        username = 'autofood3@gmail.com'
        password = 'auto1234'

        # The actual mail send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, to, msg)
        server.quit()

    def goto_food_point(self, browser):
        self.set_up(browser)
        self.driver.get(self.base_url + "/confluence/")
        self.driver.find_element_by_css_selector("#FoodPoint > div").click()

        self.driver.wait_for_element(xpath="//h2")
        print (self.driver.get_elm(xpath="//h2").text)

    def order_food(self, rest_id, date, round_id, really=True, browser='FIREFOX'):
        try:
            self.goto_food_point(browser)
            # self.check_order_food(date)

            print ("goToRes('{rest_id}', '{date}', '{round_id}', 'Full')".format(rest_id=rest_id, date=date,
                                                                                 round_id=round_id))
            self.driver.execute_script(
                "goToRes('{rest_id}', '{date}', '{round_id}', 'Full')".format(rest_id=rest_id, date=date,
                                                                              round_id=round_id))
            self.driver.find_element_by_id("Continue").click()
            self.driver.find_element_by_id("selectDishFromLastOrderLink").click()

            if really:
                time.sleep(5)
                self.driver.execute_script("javascript:SubmitOrder()")
                self.send_email(to='amirb@lacoon.com', message='Your food was ordered by Auto-Food.', code=rest_id)
            else:
                self.driver.find_element_by_id("fancybox-close").click()
            time.sleep(5)
            print ("order succeeded")
        finally:
            self.tear_down()

    def tear_down(self):
        self.driver.quit()

if __name__ == "__main__":
    today = "{:%d/%m/%y}".format(datetime.now())
    OrderFood().order_food(rest_id='6969', date='15/06/2016', round_id='1', really=True)
