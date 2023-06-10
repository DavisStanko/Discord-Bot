import json
import requests

# Import custom modules
from commands import settings

FILENAME = "databases/settings.csv"

def get_news(country_code, NEWS_API_KEY):
    news = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&country={country_code}"
    print(news)
    response = requests.get(news)
    data = json.loads(response.text)
    return data

def parse_news(data):
    #get the links
    data = data["results"]
    links = []
    for i in range(3):
        links.append(data[i]["link"])
    return links    

def main(guild, NEWS_API_KEY): 
    country_code = settings.get_country(guild)
    print(country_code)
    news = get_news(country_code, NEWS_API_KEY)
    print(news)
    parsed_news = parse_news(news)
    print(parsed_news)
    split_news = "\n".join(parsed_news)
    print(split_news)
    news_report = f"Here are the top 3 news stories right now:\n{split_news}"
    print(news_report)
    return news_report