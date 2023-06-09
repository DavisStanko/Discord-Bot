import csv

FILENAME = "settings.csv"

def get_news_channel(guild):
    # read the news channel from the settings file for the guild
    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (headers)
        for row in reader:
            if row[1] == str(guild.id):
                try:
                    news_channel = guild.get_channel(int(row[4]))
                except ValueError:
                    news_channel = None
                return news_channel