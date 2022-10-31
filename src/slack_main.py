import slack_app as sa
import scraping as sc
import cleanning_wordcloud as clean_word
import sys
import json
import re

def main():
    # -------------------------------------
    # load api token
    # -------------------------------------
    credentials_root = 'data/'
    credential_fpath = credentials_root + 'file.json'
    print('load file.json ...')
    print("")
    with open(credential_fpath, 'r') as f:
        credentials = json.load(f)

    TOKEN = credentials['Bot_User_OAuth_Token']  # API Token
    CHANNEL = credentials['CHANNEL']
    # -------------------------------------
    # start slack app
    # -------------------------------------
    print('start slack app ...')
    print("")
    app = sa.SlackApp(
        TOKEN,  # API Token
        CHANNEL 
    )
    # -------------------------------------
    # messsage all get
    # -------------------------------------
    app.all_get()
    # -------------------------------------
    # message part get
    # -------------------------------------
    output_url = app.part_get()
    # -------------------------------------
    # scraping
    # -------------------------------------
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    if re.match(pattern, output_url):
        print("Is URL")
        print("")
        # ここでscraping.py の Scrapingを呼び出す
        print("Scraping Start!!")
        print("")
        scraping = sc.Scraping(output_url)
        text = scraping.return_text()
        print("WordCloud Start!!")
        print("")
        list_data = clean_word.wakati(text)
        clean_word.word_cloud(list_data)
        # -------------------------------------
        # slackに送信
        # -------------------------------------
        # app.submit_text()
        print("Submit Image to Slack!!")
        app.submit_image()

    else:
        print("Not URL")

if __name__ == "__main__":
    main()
