import sqlite3

def create_table():
    conn = sqlite3.connect('points.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS points_table (
                userID INTEGER PRIMARY KEY,
                points INTEGER
                )""")
    conn.commit()
    conn.close()
    
def add_user(userID, starting_points):
    conn = sqlite3.connect('points.db')
    c = conn.cursor()
    # Check if user already exists
    c.execute("SELECT * FROM points_table WHERE userID=?", (userID,))
    user = c.fetchone()
    if user is None:
        c.execute("INSERT INTO points_table (userID, points) VALUES (?, ?)", (userID, starting_points))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

def get_points(userID):
    conn = sqlite3.connect('points.db')
    c = conn.cursor()
    c.execute("SELECT points FROM points_table WHERE userID=?", (userID,))
    points = c.fetchone()
    conn.close()
    return points[0]

def add_points(userID, points):
    conn = sqlite3.connect('points.db')
    c = conn.cursor()
    c.execute("UPDATE points_table SET points = points + ? WHERE userID=?", (points, userID))
    conn.commit()
    conn.close()