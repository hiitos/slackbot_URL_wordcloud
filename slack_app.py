# slackapiを使って所望の情報を取得するクラス(加工はしない)
from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient
import os
from email import message
import requests
import json
from tqdm import tqdm
import pandas as pd
import logging

class SlackApp:
    def __init__(self, Bot_User_OAuth_Token, CHANNEL):
        history_url = "https://slack.com/api/conversations.history"
        self.api_token = str(Bot_User_OAuth_Token)
        self.ch = str(CHANNEL)
        self.headers = {"Authorization": "Bearer "+ self.api_token}
        params = {
            "channel": self.ch
            #,"limit": 10
        }
        self.r = requests.get(history_url, headers=self.headers, params=params)
        #print(json.dumps(self.r.json(), indent=4, sort_keys=True))

    def all_get(self):
        # 全表示
        data = self.r.json()
        list = []
        for l in range(len(data["messages"])):
            list.append(data["messages"][l]["text"])
        #print(json.dumps(data, indent=2, ensure_ascii=False))
        # print("--------過去のメッセージ--------")
        # print(list)
    
    def part_get(self):
        data = self.r.json()
        #最新のメッセージ取得
        latest_data = str(data["messages"][0]["text"])
        print("--------最新のメッセージ--------")
        new_text = latest_data.replace('<',"")
        new_text = new_text.replace('>', "")
        print(new_text)
        print("")
        return new_text

    def submit_image(self):
        print("Submmit Image!!")
        client = WebClient(token=self.api_token)
        logger = logging.getLogger(__name__)
        file_name = "/Users/hitose.k/Desktop/PlayGround/Python_WorkPlace/Slack_ScraClud/wc_image_ja.png"
        
        try:
            # Call the files.upload method using the WebClient
            # Uploading files requires the `files:write` scope
            result = client.files_upload(
                channels=self.ch,
                initial_comment="Create a wordCloud from a URL:smile:",
                file=file_name,
            )
            # Log the result
            logger.info(result)
        except SlackApiError as e:
            logger.error("Error uploading file: {}".format(e))
    
    def submit_text(self):
        url = "https://slack.com/api/chat.postMessage"
        params = {
            'channel': self.ch,
            'text': 'テストテキスト'
        }
        r = requests.post(url, headers=self.headers, data=params)
        # r = requests.post(url, headers=self.headers, params=params)  
        print("return ", r.json())
