import unittest
import cv2
import numpy as np
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException

from desired_capabilities import android_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TestFirst(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.driver = android_driver()

    def test_first(self):
        id_field = self.driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/android.widget.EditText[1]")
        pw_field = self.driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/android.widget.EditText[2]")
        fnd_pw_Btn = self.driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/android.widget.TextView[1]")
        login_Btn = self.driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/android.widget.Button")
        join_Btn = self.driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/android.widget.TextView[2]")
        sns_textview = self.driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/android.widget.TextView[3]")

        if id_field.get_attribute("text") != "이메일 아이디 입력" or pw_field.get_attribute("text") != "비밀번호 입력" \
                or fnd_pw_Btn.get_attribute("text") != "비밀번호 찾기" or login_Btn.get_attribute("text") != "로그인" \
                or join_Btn.get_attribute("text") != "회원가입" or sns_textview.get_attribute("text") != "SNS계정으로 간편로그인하세요.":
            assert False
        else:
            pass

    def test_kakaobtn(self):
        thr = 0.95
        self.driver.save_screenshot('screencap.png')

        img = cv2.imread('screencap.png') #원본 이미지
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #원본 이미지
        template = cv2.imread('kakaobtn.png', cv2.IMREAD_GRAYSCALE) # 템플릿 이미지, grayscale 이미지 사용
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(imgray, template, cv2.TM_CCOEFF_NORMED)#템플릿 매칭 함수 matchTemplate(원본 이미지, 템플릿 이미지, 템플릿 매칭 플래그) / 이미지는 8비트의 단일 채널 이미지 사용
        loc = np.where(res >= thr) # (array_row, array_column) row = y, column = x

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        try:
            TouchAction(self.driver).tap(x=pt[0] + w / 2, y=pt[1] + h / 2).perform()
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '카카오톡으로 간편로그인')]")))
        except NoSuchElementException:
            assert False
        finally:
            self.driver.press_keycode(4)

if __name__ == '__main__':
    unittest.main()