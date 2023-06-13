import os
import csv

FILENAME = 'databases/points.csv'

def create_table():
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'UserID', 'Points', 'Income Timestamp'])
            print(f'{FILENAME} created successfully.')
    else:
        print(f'{FILENAME} already exists.')

def has_account(userID):
    # Load all rows from the CSV file
    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Check if userID is in the CSV
    for row in rows:
        if row[1] == str(userID):
            return True

    return False

def add_user(userID, starting_points):
    # Load all rows from the CSV file
    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Check if userID is already in the rows list
    for row in rows:
        if row[1] == str(userID):
            return False

    # If userID is not found, add the user to the CSV
    with open(FILENAME, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['none', userID, starting_points, '0'])
        return True

def get_points(userID):
    # Check if userID is in the CSV
    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == str(userID):
                return int(row[2])

def add_points(userID, points):
    # Check if userID is in the CSV
    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)  # Convert reader to a list of rows
        
    with open(FILENAME, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            if row[1] == str(userID):
                current_points = int(row[2])
                new_points = current_points + points
                row[2] = str(new_points)  # Convert back to string for writing to CSV
            writer.writerow(row)
            
def get_last_income(userID):
    # Check if userID is in the CSV
    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == str(userID):
                return int(row[3])
            
def set_last_income(userID, timestamp):
    # Check if userID is in the CSV
    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)  # Convert reader to a list of rows
        
    with open(FILENAME, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            if row[1] == str(userID):
                row[3] = str(timestamp)  # Convert back to string for writing to CSV
            writer.writerow(row)

def get_top_users(number):
    # Load all rows from the CSV file
    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row

        # Sort rows by points
        rows = sorted(reader, key=lambda x: int(x[2]), reverse=True)

        # get top number of rows
        top_rows = rows[:number]

        # get user ids
        top_users = []
        for row in top_rows:
            top_users.append(row[1])

        # get points
        top_points = []
        for row in top_rows:
            top_points.append(int(row[2]))

        # return
        return top_users, top_points