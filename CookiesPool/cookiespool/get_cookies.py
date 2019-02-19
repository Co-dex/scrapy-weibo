from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class WeiboCookies():
    def __init__(self, username, password):
        """

        :param username: 用户名
        :param password: 密码
        """
        self.username = username
        self.password = password
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(
            'user-agent="Nokia5250/10.0.011 (SymbianOS/9.4; U; Series60/5.0 Mozilla/5.0; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/525 (KHTML, like Gecko) Safari/525 3gpp-gba"')
        self.broswer = webdriver.Chrome(chrome_options=self.options)
        self.actionchains = ActionChains(self.broswer)
        self.url = 'https://weibo.cn'
        self.userinput = None
        self.userpswd = None
        self.logoin_submit = None
        self.check_btn = None
        self.success_tag = False

    def __del__(self):
        self.broswer.delete_all_cookies()
        self.broswer.quit()

    def get_logoinpage(self):
        self.broswer.get(self.url)
        try:
            self.logoin_btn = WebDriverWait(self.broswer, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.u > div > a:nth-child(1)')))
            self.logoin_btn.click()  # 跳转至登录页
            # self.get_logoin_elements()
        except TimeoutException:
            print('超时！未找到登陆按钮')

    def get_logoin_elements(self):

        self.userinput = WebDriverWait(self.broswer, 20).until(
            EC.presence_of_element_located((By.ID, 'loginName')))
        self.userpswd = WebDriverWait(self.broswer, 20).until(
            EC.presence_of_element_located((By.ID, 'loginPassword')))
        self.logoin_submit = WebDriverWait(self.broswer, 20).until(
            EC.element_to_be_clickable((By.ID, 'loginAction')))

        self.actionchains.move_to_element_with_offset(self.userinput, 101, 20).click().perform()
        self.userinput.send_keys(self.username)
        time.sleep(1)
        self.actionchains.move_to_element_with_offset(self.userpswd, 101, 20).click().perform()
        self.userpswd.send_keys(self.password)
        time.sleep(3)
        try:
            self.logoin_submit.click()  # 点击登陆
        except: pass
        self.check_btn = WebDriverWait(self.broswer, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        self.actionchains.move_to_element_with_offset(self.check_btn, 30, 40).click()
        # self.check_btn.click()
        # self.success_tag = self.success()

    def success(self, timeout=30):
        try:
            print('验证环节。等待用户验证！')
            WebDriverWait(self.broswer, timeout).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'),
                                                 '验证成功'))  # 此处会抛出超时异常
            print('验证成功')
            time.sleep(3)
            self.broswer.get(self.url)
            return True
        except TimeoutException:
            print('超时！未检测到成功标志..')
            return False

    def run(self):
        self.get_logoinpage()
        self.get_logoin_elements()
        try:
            self.success_tag = self.success()
            if self.success_tag:
                print('返回Cookies！')
                cookies = {
                    'status': 1,
                    'content': self.broswer.get_cookies()
                }
                self.broswer.close()
                return cookies

            else:

                print('发现验证码！ 等待用户操作！')
                if self.success(timeout=30):
                    print('成功！ 尝试返回cookies！')
                    cookies =  {
                        'status': 1,
                        'content': self.broswer.get_cookies()
                    }
                    self.broswer.close()
                    return cookies
                else:
                    print('获取失败！ 模块退出')
                    self.broswer.close()
                    return {}
        except:
            print('遇到错误！ 程序退出')
            return {
                'status': 3,
                'content': '登陆失败'
            }
