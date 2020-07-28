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
        
        
    
    print(symbol, order_type, stop_loss, take_profit, trade_is_valid, sep="---")

with client:
    client.start()
    client.run_until_disconnected()