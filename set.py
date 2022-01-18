import json
import requests
import os
from PIL import Image, ImageDraw, ImageFont
import tweepy
import time
from threading import Timer
import os
from dotenv import load_dotenv


load_dotenv()
run = True


# Get Price of Ticker
def getTickerData(ticker_list):
    data_list = []
    for i in ticker_list:
        res = requests.get(
            f'https://api.binance.com/api/v3/ticker/price?symbol={i}')

        data = json.loads(res.text)
        data_list.append(data)
    return data_list


def test():

    # -------------------------------------------------------------------------
    consumer_key = os.getenv('consumer_key')  # API
    consumer_secret = os.getenv('consumer_secret')  # Secret_Key
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    access_token = os.getenv('access_token')
    access_token_secret = os.getenv('access_token_secret')
    auth.set_access_token(access_token, access_token_secret)
    # -------------------------------------------------------------------------

    api = tweepy.API(auth)
    user = api.me()

    # -------------------------------------------------------------------------

    def limit_handler(cursor):
        try:
            while True:
                yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(5000)

    # -------------------------------------------------------------------------

    # get recent followers
    recent_followers = []
    for follower in (tweepy.Cursor(api.followers).items(5)):
        recent_followers.append(follower.screen_name)

    # -------------------------------------------------------------------------

    img = Image.new(mode="RGB", size=(1500, 500), color=(8, 9, 37))
    I1 = ImageDraw.Draw(img)

    # Draw Crypto Ticker
    symbol_font = ImageFont.truetype(
        './Fonts/New_Comic_Title/newcomictitle.ttf', 55)
    price_font = ImageFont.truetype(
        './Fonts/louis_george_caf/Louis George Cafe.ttf', 55)
    ticker_list = getTickerData(['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'SOLUSDT'])

    y_axis = 40
    for item in ticker_list:
        price = round(float(item["price"]), 1)
        symbol = item['symbol'] + "-" + "$ "
        price = str(price)
        I1.text((40, y_axis), symbol,
                font=symbol_font, fill=(255, 104, 241))
        I1.text((280, y_axis), price,
                font=price_font, fill=(255, 104, 241))
        y_axis += 75

    # Draw FOLLOWER COUNT

    user = api.get_user('thecryptogo')
    num_followers = user.followers_count

    # --------------------
    count_font = ImageFont.truetype(
        './Fonts/New_Comic_Title/newcomictitle.ttf', 190)
    myFont = ImageFont.truetype(
        './Fonts/New_Comic_Title/newcomictitle.ttf', 65)
    I1.text((640, 70), f"{num_followers}",
            font=count_font, fill=(255, 104, 241))
    I1.text((600, 250), f"Followers", font=myFont, fill=(255, 104, 241))

    # Draw RECENT FOLLOWER Title

    I1.text((1050, 40), f"Recent Followers", font=ImageFont.truetype(
        './Fonts/New_Comic_Title/newcomictitle.ttf', 60), fill=(255, 104, 241))

    # Draw recent followers
    y_axis = 120
    for i in recent_followers:
        I1.text((1050, y_axis), f"@{i}", font=ImageFont.truetype(
            './Fonts/louis_george_caf/Louis George Cafe Bold.ttf', 40), fill=(255, 104, 241))
        y_axis += 60

    # --------------------------------------------------------------

    img.save('header.jpg')
    # update profile banner
    api.update_profile_banner('header.jpg')

    if run:
        Timer(300, test).start()
        print('DONE')


test()
