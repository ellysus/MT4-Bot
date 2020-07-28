from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from credentials import acc_login, acc_password, acc_server
from time import sleep
import configparser
import re
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)
from telethon import TelegramClient, events

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

class MTBot():
    def __init__(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("dom.forms.number", False) 
        self.driver = webdriver.Firefox(profile)

    def login(self):
        self.driver.get('https://trade.mql5.com/')

        sleep(2)

        usrname_in = self.driver.find_element_by_xpath('//*[@id="login"]')
        usrname_in.send_keys(acc_login)

        password_in = self.driver.find_element_by_xpath('//*[@id="password"]')
        password_in.send_keys(acc_password)

        server_in = self.driver.find_element_by_xpath('//*[@id="server"]')
        server_in.clear()
        server_in.send_keys(acc_server)

        login_btn = self.driver.find_element_by_xpath('/html/body/div[14]/div/div[3]/button[2]')
        login_btn.click()
    
    def place_order(self, symbol, buysell, tp, sl):
        order_btn = self.driver.find_element_by_xpath('/html/body/div[3]/div[1]/a[1]')
        order_btn.click()
        
        select = Select(self.driver.find_element_by_xpath('//*[@id="symbol"]'))
        select.select_by_value(symbol.upper())

        stop_loss_fld = self.driver.find_element_by_xpath('//*[@id="sl"]')
        stop_loss_fld.clear()
        stop_loss_fld.send_keys(Keys.CONTROL, 'a')
        stop_loss_fld.send_keys(str(sl))

        take_profit_fld = self.driver.find_element_by_xpath('//*[@id="tp"]')
        take_profit_fld.clear()
        take_profit_fld.send_keys(Keys.CONTROL, 'a')
        take_profit_fld.send_keys(str(tp))

        buy_btn = self.driver.find_element_by_xpath('/html/body/div[16]/div/div[3]/button[3]')
        sell_btn = self.driver.find_element_by_xpath('/html/body/div[16]/div/div[3]/button[2]')
        ok_btn = self.driver.find_element_by_xpath('/html/body/div[16]/div/div[3]/button[6]')
        if buysell.lower() == "buy":
            buy_btn.click()
            sleep(0.5)
            ok_btn.click()
        elif buysell.lower() == "sell":
            sell_btn.click()
            sleep(0.5)
            ok_btn.click()
        else:
            pass

bot = MTBot()
bot.login()

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)


async def main():
    print('Client Started.')


@client.on(events.NewMessage(chats=-1001262107919))
async def signal_handler(event):
    print('New Signal!')
    signal = event.text

    trade_data = signal.split()

    symbol = trade_data[0]
    order_type = trade_data[1]
    stop_loss_str = trade_data[5]
    take_profit_str = trade_data[7]

    try:
        stop_loss = float(stop_loss_str)
        take_profit = float(take_profit_str)
        trade_is_valid = True
    except:
        trade_is_valid = False
        print("No trade found in message... disregarded.", trade_is_valid, sep=' --- ')

    if trade_is_valid == True:
        bot.place_order(symbol, order_type, take_profit, stop_loss)
    elif trade_is_valid == False:
        print("Order data not found... Disregarding")
    else:
        pass


with client:
    client.start()
    client.run_until_disconnected()

#bot.place_order("Eurusd", 1.1540, 1.1800, "sell")

