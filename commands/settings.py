import csv

FILENAME = "databases/settings.csv"

def get_city(guild):
    with open(FILENAME, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == str(guild):
                return row[2]
    return None

def get_country(guild):
    with open(FILENAME, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == str(guild):
                return row[3]
    return None

def get_news_channel(guild):
    with open(FILENAME, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == str(guild):
                return row[4]
    return None

def set_location(guild, city, country):
    city, country = city.lower(), country.lower()

    with open(FILENAME, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    with open(FILENAME, "w") as f:
        writer = csv.writer(f)
        for row in rows:
            if row[1] == str(guild):
                row[2] = city
                row[3] = country
            writer.writerow(row)

    return True

def set_news_channel(guild, channel):
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