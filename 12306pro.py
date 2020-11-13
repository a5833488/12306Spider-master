import urllib
from asyncio import  get_event_loop

from google.auth.transport import requests
from pyppeteer import launch
from random import randint
from main import main
from verification_code import slide_list
import time


class Zt12306Spider:
    def getllticket(ss):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Cookie': "JSESSIONID=54F975536A08984C356AFCDA2BFB93CB; tk=BMJClXIfqC9OzGjw1IiQjT1hw6aTsxf-M4ZNVg73m1m0; RAIL_DEVICEID=IuVi2_YCOAZAds2tlhQAp_iTyMBHdkzbwtbRpcr6Rfx-EuKF1C7lwtZxhxJ4a-imLgQUywLUlUwylB0iZgchQnN2bVJPmYnQ8MHvEKbOPQdXkvN3qogoh4wyNbdZCFJQ4ugDkRUiQt0w2kcdUXkxxa7Zco-OhDP8; RAIL_EXPIRATION=1605200089549; _jc_save_showIns=true; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u4E0A%u6D77%2CSHH; _jc_save_toStation=%u5317%u4EAC%2CBJP; _jc_save_toDate=2020-11-11; BIGipServerpool_passport=132383242.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; _jc_save_fromDate=2020-11-11; current_captcha_type=Z; BIGipServerpassport=870842634.50215.0000; BIGipServerportal=3067347210.17695.0000; BIGipServerotn=66060810.50210.0000; uKey=d2306123c0469bc9a8a91489ab300948062a74fca0f71ad189ae75f64d50dcfb"
        }
        url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2020-11-11&leftTicketDTO.from_station=SHH&leftTicketDTO.to_station=BJP&purpose_codes=ADULT'
        result = requests.get(url, headers=header)
        return result

    def submitOrderRequest(secretStr):
        secretStr = urllib.parse.unquote(secretStr)
        data = {
            'secretStr': secretStr,
            'train_date': '2020-11-11',  # 出发时间
            'back_train_date': '2020-11-11',  # 返程时间
            'tour_flag': 'dc',  # 旅途类型
            'purpose_codes': 'ADULT',  # 成人 | 学生
            'query_from_station_name': '上海',
            'query_to_station_name': '北京'
        }
    def __init__(self,username,password):
        self.width, self.height = 1920, 1080
        self.username = username
        self.password = password
        get_event_loop().run_until_complete(self.init())
        get_event_loop().run_until_complete(self.login())

    async def init(self):
        self.browser = await launch(headless=False,
                                   args=['--disable-infobars', f'--window-size={self.width},{self.height}', '--no-sandbox'])
        self.page = await self.browser.newPage()
        await self.page.setViewport({'width': self.width, 'height': self.height})
        await self.page.goto('https://kyfw.12306.cn/otn/resources/login.html')
        await self.page.evaluate('()=>{Object.defineProperties(navigator,{webdriver:{get:()=>false}})}')

    async def login(self):
        time.sleep(1)
        await self.page.click('.login-hd-account')
        await self.page.type('#J-userName', self.username, {'delay': randint(60, 120)})  # 账号
        await self.page.type('#J-password', self.password, {'delay': randint(100, 151)})  # 密码
        # 验证码
        code = await self.page.waitForSelector('#J-loginImg')  # 通过css selector定位验证码元素
        # 验证码截图
        await code.screenshot({'path': 'captcha.jpg'})
        # 获取验证码坐标
        box = await code.boundingBox()
        # 获取验证码
        result = ''
        text, check = main('captcha.jpg')
        for t in text:
           for pos, l in check:
               if t == l:
                   result += str(pos) + ','
        resultNums = result[:-1]
        print(resultNums)  # 字符串
        if len(resultNums) > 0:
            resList = resultNums.split(',')

            await self.page.waitFor(1 * 1000)
            for res in resList:
               if int(res) < 5:
                   await self.page.mouse.click(box['x'] + 37 * (2 * int(res) - 1), box['y'] + 70)
                   await self.page.waitFor(randint(567, 3456))
               else:
                   await self.page.mouse.click(box['x'] + 37 * (2 * int(res) - 9), box['y'] + 150)
                   await self.page.waitFor(randint(567, 3456))
            await self.page.waitFor(1 * 1000)
            await self.page.click('#J-login')

            slider = await self.page.Jeval('#login_slide_box', 'node => node.style')  # 是否有滑块
            if slider:
                print('出现滑块')
                await self.page.waitFor('.btn_slide')
                await self.slide_move('.btn_slide')
            await self.page.waitForNavigation()
            result = await self.getllticket()
            await print(result)
            await print()
            # await self.page.goto('https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2020-11-10&leftTicketDTO.from_station=SHH&leftTicketDTO.to_station=BJP&purpose_codes=ADULT', timeout=30000)
            # await time.sleep(10)
            # await self.page.goto('https://kyfw.12306.cn/otn/confirmPassenger/initDc', timeout=30000)
            # slide_btn = await self.page.waitForSelector('#slide_passcode .nc-lang-cnt', timeout=30000)
            # rect = await slide_btn.boundingBox()
            # pos = DomBounding(rect)
            # pos.x += 5
            # pos.y += 10
            # await page.mouse.move(pos.x, pos.y)
            # await page.mouse.down()
            # await page.mouse.move(pos.x + pos.width, pos.y, steps=30)
            # await self.page.waitFor(3 * 1000)
            # await self.page.click('.modal-ft >a')
            # await self.page.goto('https://kyfw.12306.cn/otn/leftTicket/init') #跳转到个人信息页面
            cookies = await self.page.cookies()
            await print(cookies)


        else:
            print('验证码自动识别失败，请重试')

    async def slide_move(self, slide_id):
        await self.page.hover(slide_id)
        # await self.page.evaluate('document.querySelector("'+slide_id+'").hover()')
        await self.page.mouse.down()
        slides = slide_list(300)
        x = self.page.mouse._x
        for distance in slides:
            x += distance
            await self.page.mouse.move(x, 0, )
        await self.page.mouse.up()


if __name__ == '__main__':
    username = '15702129194'
    password = 'a5833488'
    Zt12306Spider(username, password)
