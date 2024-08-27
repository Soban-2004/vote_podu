import psycopg2

def initialize_database():
    conn = psycopg2.connect(
        dbname='votes_e29f',
        user='votes_e29f_user',
        password='OyKZT8cTOkwF0EdmVmxSg2Zu5tGBj8O6',
        host='dpg-cr6p3pd6l47c7397q0qg-a.oregon-postgres.render.com',
        port='5432'
    )
    cursor = conn.cursor()

    # Create the votes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS votes (
        id SERIAL PRIMARY KEY,
        registration_number TEXT NOT NULL,
        position TEXT NOT NULL,
        candidate TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
