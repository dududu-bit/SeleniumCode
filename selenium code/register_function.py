#coding  = utf-8
#优化了register_code里面的代码，把其中的值进行的封装，无论怎么变，只需要去配置文件改 > 后面的值就行
#register_function -> find_element -> read_ini -> LocalElement


from  selenium import  webdriver
import time
import random
from PIL import Image
from ShowapiRequest import ShowapiRequest
from base.find_element import FindElement

class RegisterFunction(object):


    #因为driver后面要用，所以放入构造函数__init__中
    def __init__(self,url,i):
        self.driver = self.get_driver(url)


    #获取driver并且打开url
    def get_driver(self,url,i):
        if i == 1:
            driver = webdriver.Chrome()
        elif i==2:
            driver = webdriver.Firefox()
        else:
            driver = webdriver.Edge()
        driver.get(url)
        driver.maximize_window()
        return driver


    #输入用户信息
    def send_user_info(self,key,data):
        self.get_user_element(key).send_keys(data)


    #主要改变的是这里
    #定位元素用户信息，获取element
    def get_user_element(self,key):
        find_element =  FindElement(self.driver)
        user_element = find_element.get_element(key)
        return  user_element


    # 获取随机数
    def get_range_user(self):
        user_info = ''.join(random.sample('1234567890abcdefghijklmn', 8))
        return user_info


    # 获取图片
    def get_code_image(self,file_name):
        self.driver.save_screenshot(file_name)
        #无论怎么变，我只需要去配置文件改 > 后面的值就行
        code_element = self.get_user_element("code_image")
        left = code_element.location['x']
        top = code_element.location['y']
        right = code_element.size['width'] + left
        height = code_element.size['height'] + top
        im = Image.open(file_name)
        img = im.crop((left, top, right, height))
        img.save(file_name)


    # 解析图片获取验证码
    def code_online(self,file_name):
        self.get_code_image(file_name)
        r = ShowapiRequest("http://route.showapi.com/184-4", "62626", "d61950be50dc4dbd9969f741b8e730f5")
        r.addBodyPara("typeId", "35")
        r.addBodyPara("convert_to_jpg", "0")
        r.addFilePara("image", file_name)
        res = r.post()
        print(res.text)
        text = res.json()['showapi_res_body']['Result']
        return text

    # 运行主程序
    def main(self):
        user_name_info = self.get_range_user()
        user_email = user_name_info + "@163.com"
        file_name = "/Users/pmy/Downloads/selenium code/test.png"
        code_text = self.code_online(file_name)
        self.send_user_info('user_email',user_email)
        self.send_user_info('user_name', user_name_info)
        self.send_user_info('password', "111111")
        self.send_user_info('code_text', code_text)
        # 检测整个流程是否通过
        code_error = self.get_user_element('code_text_error')
        if code_error == None:
            print("success")
        else:
            self.driver.save_screenshot("/Users/pmy/Downloads/selenium code/code_error.png")
        time.sleep(5)
        self.driver.close()

if __name__ == '__main__':
    #多浏览器跑case，检查脚本兼容性，循环一个个跑，减少内存的使用
    for i in range(3):
        register_function = RegisterFunction("http://www.5itest.cn/register",i)
        register_function.main()

