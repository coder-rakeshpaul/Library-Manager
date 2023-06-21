import psycopg2

print("----Welcome human-----")
# Create a connection object to the PostgreSQL server
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    user='postgres',
    database= 'postgres',
    password= str(input('Enter the password: '))
)
conn.autocommit = True
cur = conn.cursor()

# Create the database
sql = """CREATE DATABASE lib;"""
cur.execute(sql)

cur.close()
conn.close()

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    user='postgres',
    database= 'lib',
    password= str(input('Enter the password: '))
)
conn.autocommit = True
cur = conn.cursor()

# Create the database
sql = """CREATE TABLE students (id text PRIMARY KEY , name text , email text, phone text);"""
cur.execute(sql)

sql = """CREATE TABLE books (code text PRIMARY KEY , title text , author text, description text);"""
cur.execute(sql)

sql = """CREATE TABLE book_student_map (book_code text PRIMARY KEY, student_id text, student_name text , student_contact text);"""
cur.execute(sql)

cur.close()
conn.close()