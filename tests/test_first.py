import unittest
import cv2
import numpy as np
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
SERVER_URL_BASE = 'http://localhost:4723/wd/hub'

class TestFirst(unittest.TestCase):
    def setUp(self):
        desired_caps = {
            "deviceName": "Galaxy Note10+",
            "deviceUDID": "R3CM70H0BAV",
            "app": "C:\\Users\\KIWIPLUS\\Desktop\\apk\\kiwiplay-v1.1.2(112)-stage-debug.apk",
            'platformName': 'Android',
            'appPackage': 'io.kiwiplus.app.kiwiplay.stage',
            'noReset': 'true',
            'fullReset': 'false'
        }
        self.driver = webdriver.Remote(SERVER_URL_BASE, desired_caps)
        self.driver.implicitly_wait(30)

    def test_title(self):
        id_field = self.driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/android.widget.EditText[1]")
        pw_field = self.driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/android.widget.EditText[2]")
        fnd_pw_Btn = self.driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/android.widget.TextView[1]")
        login_Btn = self.driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/android.widget.Button")
        join_Btn = self.driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/android.widget.TextView[2]")
        sns_textview = self.driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/android.widget.TextView[3]")

        if id_field.get_attribute("text") != "????????? ????????? ??????" or pw_field.get_attribute("text") != "???????????? ??????" \
                or fnd_pw_Btn.get_attribute("text") != "???????????? ??????" or login_Btn.get_attribute("text") != "?????????" \
                or join_Btn.get_attribute("text") != "????????????" or sns_textview.get_attribute("text") != "SNS???????????? ????????????????????????.":
            assert False
        else:
            pass

    def test_kakaobtn(self):
        thr = 0.95
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '?????????')]")))
        self.driver.save_screenshot('screencap.png')

        img = cv2.imread('screencap.png') #?????? ?????????
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #?????? ?????????
        template = cv2.imread('kakaobtn.png', cv2.IMREAD_GRAYSCALE) # ????????? ?????????, grayscale ????????? ??????
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(imgray, template, cv2.TM_CCOEFF_NORMED)#????????? ?????? ?????? matchTemplate(?????? ?????????, ????????? ?????????, ????????? ?????? ?????????) / ???????????? 8????????? ?????? ?????? ????????? ??????
        loc = np.where(res >= thr) #(array_row, array_column) row = y, column = x

        try:
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            TouchAction(self.driver).tap(x=pt[0] + w / 2, y=pt[1] + h / 2).perform()
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '?????????????????? ???????????????')]")))
        except NoSuchElementException:
            assert False
        finally:
            self.driver.press_keycode(4)

if __name__ == '__main__':
    unittest.main()