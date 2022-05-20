import os
import re

from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()
api_id = int(os.getenv('TELEGRAM_ID'))
api_hash = os.getenv('TELEGRAM_HASH')

# Channels
cmc_channel = '1519789792'
cg_channel = '1618359068'
travladd_channel = '1549900075'
travladd_channel2 = '1334459060'
banana_channel = '1550510484'
rugdoc_channel = '1375401113'
chiatk_channel = '1441067640'

client = TelegramClient('session_name', api_id, api_hash)
client.start()

@client.on(events.NewMessage())
async def main(event):
     try:
          # print(event)
          ctcExtract(event)
          # _event = event
          # _message = _event.message.message
          # print(_message)
          # _0xthing = re.findall(r'(0x\w+)', _message)
          # for s in _0xthing:
          #      if len(s) == 42:
          #           _contract = s
          #           print(_contract)


     except:
          print("error")
          pass

def ctcExtract(_event):
     _channel_id = _event.peer_id.channel_id
     if _channel_id == cmc_channel or _channel_id == travladd_channel or _channel_id == travladd_channel2 or _channel_id == cg_channel:
          _message = _event.message.message
          print(f"Message: {_message}")
          _0xthing = re.findall(r'(0x\w+)', _message)
          for s in _0xthing:
               if len(s) == 42:
                    _contract = s
                    print(f"Channel: {_channel_id}")
                    print(f"Contract: {_contract}")
                    f = open("contracts.txt", "a")
                    f.write(_contract + "\n")
                    f.close()


client.run_until_disconnected()