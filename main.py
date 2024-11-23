import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "******"
NEWS_API_KEY = "**********"
TWILIO_SID = "AC5ea6c7329181fb1a86f8043126797587"
TWILIO_AUTH_TOKEN = "*******" # visiable
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)


day_before_yesterday_data = data_list[1]
d_b_y_closing_price = day_before_yesterday_data["4. close"]
print(d_b_y_closing_price)

difference = float(yesterday_closing_price) - float(d_b_y_closing_price)
print(difference)

diff_percent = round((difference / float(yesterday_closing_price))* 100)
print(diff_percent)

up_down = None
if difference < 0:
    up_down = "🔻"
else:
    up_down = "🔺"

if abs(diff_percent) > 3:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]
    print(three_articles)

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
             body=article,
            from_="whatsapp:+*****",#twilio number
            to="whatsapp:+*****",#your number
        )

