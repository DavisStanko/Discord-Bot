import csv

FILENAME = "databases/settings.csv"

def get_city(guild):
    # read the city from the settings file for the guild
    with open(FILENAME, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == str(guild):
                return row[2]
    return None

def get_country(guild):
    # read the country from the settings file for the guild
    with open(FILENAME, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == str(guild):
                return row[3]
    return None

def get_news_channel(guild):
    # read the news channel from the settings file for the guild
    with open(FILENAME, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            print(f"{row[1]} == {str(guild)}")
            if row[1] == str(guild):
                return row[4]
    return None


def set_city(guild, city):
    # set the city in the settings file for the guild
    with open(FILENAME, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
    with open(FILENAME, "w") as f:
        writer = csv.writer(f)
        for row in rows:
            if row[1] == str(guild):
                row[2] = city
            writer.writerow(row)
    return True

def set_country(guild, country):
    # set the country in the settings file for the guild
    with open(FILENAME, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
    with open(FILENAME, "w") as f:
        writer = csv.writer(f)
        for row in rows:
            if row[1] == str(guild):
                row[3] = country
            writer.writerow(row)
    return True

def set_news_channel(guild, channel):
    # set the news channel in the settings file for the guild
    with open(FILENAME, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
    with open(FILENAME, "w") as f:
        writer = csv.writer(f)
        for row in rows:
            if row[1] == str(guild):
                row[4] = channel
            writer.writerow(row)
    return True