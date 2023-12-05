import mysql.connector

def get_db_connection():
    db_config = {
        'user': 'root',
        'password': 'Lolcats1560733!',
        'host': 'localhost',
        'database': 'Academicas',
        'raise_on_warnings': True
    }
    conn = mysql.connector.connect(**db_config)
    return conn

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

