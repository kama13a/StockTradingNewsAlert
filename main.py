import time
import requests
import os
from dotenv import load_dotenv
import json
load_dotenv()
TREAD_API_KEY=os.environ.get("ALPHA_API_KEY")
NEWS_API_KEY=os.environ.get("NEWS_API_KEY")
TELEGRAM_TOKEN=os.environ.get("TELEGRAM_TOKEN")
CHAT_ID=os.environ.get("CHAT_IDhow the ")

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
USE_MOCK_DATA = True

if USE_MOCK_DATA:
#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
    with open("data.json", "r") as file:
        daily_data = json.load(file)
else:
    parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK_NAME,
        "apikey": TREAD_API_KEY
    }
    alpha_response = requests.get(STOCK_ENDPOINT, params=parameters)
    alpha_response.raise_for_status()
    daily_data = alpha_response.json()

    with open("data.json", "w") as file:
        json.dump(daily_data, file, indent=4)

list_data = [(date,value) for (date, value) in daily_data["Time Series (Daily)"].items()]
yesterday_tuple = list_data[0]
yesterday_date, yesterday_data = yesterday_tuple
yesterday_closing = float(yesterday_data["4. close"])
#TODO 2. - Get the day before yesterday's closing stock price
day_before_tuple = list_data[1]
day_before_date, day_before_data = day_before_tuple
day_before_closing = float(day_before_data["4. close"])
#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = round(yesterday_closing - day_before_closing, 2)
if difference < 0:
    increase = f"🔻"
    difference = abs(difference)
else:
    increase = f"🔺"

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.


#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percentage = round((difference/day_before_closing)*100, 2)

#TODO 5. - If TODO4 percentage how the is greater than 5 then print("Get News").
def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text,
        },
        timeout=10,
    )
    response.raise_for_status()


    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.


#TODO 9. - Send each article as a separate message via Twilio.
if diff_percentage > 5:
    news_parameters = {
        "q": "tesla",
        "from": yesterday_date,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY,
        "language": "en",
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()

    # TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    articles = news_data["articles"]
    three_articles = articles[:3]
    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    # to send a separate message with each article's title and description to your phone number.

    # TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    news_list = [f"{STOCK_NAME}: {increase}{diff_percentage}%\nHeadline: {i['title']}\nBrief: {i['description']}" for i
                 in three_articles]
    for msg in news_list:
        send_to_telegram(msg)
        print("send one message")
        time.sleep(1)
else:
    print("no news needed ")
#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

