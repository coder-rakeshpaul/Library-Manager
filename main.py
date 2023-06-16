import psycopg2

print("----Welcome human-----")
# Create a connection object to the PostgreSQL server
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    user='postgres',
    database= str(input("Enter the database name")),
    password= str(input('Enter the password'))
)

print("welcome to the database")

conn.autocommit = True
cur = conn.cursor()

class student:
    def __init__(self) -> None:
        pass

    def del_student(self , del_s_id):
    
        print('deleting the data')

        cur.execute("DELETE FROM students WHERE id = %s", (str(del_s_id),))

    def add_student(self , id , name , email , phone):

        sql = """INSERT INTO students (ID , NAME , EMAIL , PHONE) VALUES ( %s , %s , %s , %s)""";
        cur.execute(sql , (str(id) , str(name) , str(email) , str(phone)))
        print('adding the data')

    def update_student_data(self , id , field , new_data ):

        sql_update = "UPDATE students SET {} = %s WHERE id = %s".format(str(field))
        cur.execute(sql_update , (str(new_data) , str(id)))
        print('updating the data')

class books:
    def __init__(self) -> None:
        pass

    def del_book(self , del_b_id):
    
        print('deleting the data')

        cur.execute("DELETE FROM books WHERE code = %s", (str(del_b_id),))

    def add_book(self , code , title , author , description):

        sql = """INSERT INTO books (code , title , author , description) VALUES ( %s , %s , %s , %s)""";
        cur.execute(sql , (str(code) , str(title) , str(author) , str(description)))
        print('adding the data')

    def update_data(self , code , field , new_data ):
   
        sql_update = "UPDATE books SET {} = %s WHERE code = %s".format(str(field))
        cur.execute(sql_update , (str(new_data) , str(code)))
        print('updating the data')

sol = student()
sol.add_student('sttt_65' , 'jttoy' , 'joy@joyf00ul.com' , '8989tt898')

cur.close()
conn.close()