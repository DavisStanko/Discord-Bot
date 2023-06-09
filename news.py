import csv
import requests

FILENAME = "settings.csv"

def get_news_location(guild):
    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[1] == str(guild):
                country_code = row[3]
                return country_code

def get_news(news_location, NEWS_API_KEY):
    news = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&country={news_location}"
    response = requests.get(news)
    data = response.json()
    return data

def parse_news(data):
    # get first 3 news articles' links
    articles = data["results"]
    links = []
    for article in articles[:3]:
        links.append(article["link"])
    return links

def main(guild, NEWS_API_KEY): 
    # get guild's news location
    news_location = get_news_location(guild)
    news = get_news(news_location, NEWS_API_KEY)
    parsed_news = parse_news(news)
    split_news = "\n".join(parsed_news)
    news_report = f"Here are the top 3 news right now:\n{split_news}"
    return split_news