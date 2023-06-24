import psycopg2
from datetime import date
import datetime

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
        # Deleting the data in the  given student Id
        """ arguments:
                      del_s_id : the id of the student that we wish to delete
        """
        
        print('deleting the data')
        cur.execute("DELETE FROM students WHERE id = %s", (str(del_s_id),))

    def add_student(self , id , name , email , phone):
        # adding the student to the database
        """ arguments:
                      id : the id of the student that we wish to add
                      name : name of the student
                      email : email of the student
                      phone: contact number of the student
        """
        sql = """INSERT INTO students (ID , NAME , EMAIL , PHONE) VALUES ( %s , %s , %s , %s)""";
        cur.execute(sql , (str(id) , str(name) , str(email) , str(phone)))
        print('adding the data')

    def update_student_data(self , id , field , new_data ):
        #updating the field in the given ID 
        """ arguments:
                      id : the id of the student that we wish to update
                      field : the field that we wish to update
                      new_data : the new updated data
        """
        sql_update = "UPDATE students SET {} = %s WHERE id = %s".format(str(field))
        cur.execute(sql_update , (str(new_data) , str(id)))
        print('updating the data')

class books:
    def __init__(self) -> None:
        pass

    def del_book(self , del_b_id):
        # Deleting the book with the given book code from the database
        """ arguments:
                      del_b_id : the code of the book that we wish to delete
        """
        print('deleting the data')
        cur.execute("DELETE FROM books WHERE code = %s", (str(del_b_id),))

    def add_book(self , code , title , author , description):
        #adding the new book into the database
        """ arguments:
                      code : the code of the book that we wish to add
                      title : the title of the book
                      author : the name of the author of the book
                      description : description of the book
        """
        sql = """INSERT INTO books (code , title , author , description) VALUES ( %s , %s , %s , %s)""";
        cur.execute(sql , (str(code) , str(title) , str(author) , str(description)))
        print('adding the data')

    def update_data(self , code , field , new_data ):
        #updating the book data in the database
        """ arguments:
                      code : the id of the book that we wish to update
                      field : the field that we wish to update
                      new_data : the new updated data
        """
        sql_update = "UPDATE books SET {} = %s WHERE code = %s".format(str(field))
        cur.execute(sql_update , (str(new_data) , str(code)))
        print('updating the data')

class book_lending(student , books):
    
    def __init__(self) -> None:
        super().__init__()

# getting the list of books that are issued to students
    sql = """SELECT book_code FROM book_student_map""";
    cur.execute(sql)
    val = cur.fetchall()
    list_books_issued = []
    for v in val:
        list_books_issued.append(v[0])

        

    def book_student_map(self , bk_code , st_id):

        books_per_student = 3  # Max number of books a student can take
        
        # Getting the name of the student who the book is being issued
        sql = """SELECT name FROM students WHERE id = %s""";
        cur.execute(sql , (str(st_id) ,))
        student_name = cur.fetchone()[0]

        # Getting the contact of the student who the book is being issued
        sql = """SELECT phone FROM students WHERE id = %s""";
        cur.execute(sql , (str(st_id) ,))
        student_contact = cur.fetchone()[0]

        # getting the title of the book
        sql = """SELECT title FROM books WHERE code = %s""";
        cur.execute(sql , (str(bk_code) ,))
        book_name = cur.fetchone()[0]

        query = "SELECT COUNT(*) FROM book_student_map WHERE student_id = %s ;"
        cur.execute(query , (st_id  , ))
        count = cur.fetchone()[0]

        if count < books_per_student :
            try:
                # Add the book in the table of issued books
                sql = """INSERT INTO book_student_map (book_code, student_id , student_name , student_contact) VALUES (%s, %s , %s , %s )""";
                cur.execute(sql , (str(bk_code) , str(st_id) , str(student_name) , str(student_contact)))

                # Get the current date
                now = datetime.datetime.now()
                current_date = now.strftime('%Y-%m-%d')


                # Adding the data to history
                sql = """INSERT INTO history (book_code , book_name , student_id , student_name , issue_date) VALUES ( %s , %s , %s ,%s , %s)""";
                cur.execute(sql , (bk_code , book_name ,st_id , student_name , current_date))
            except:
                print("Book is not available")
        else:
            print("limmit exeeded")

    def del_map(self ,bk_code):
        #delete the book from book_student_map indicating the book is returned by the previous student and is available for issuing
        cur.execute("DELETE FROM book_student_map WHERE book_code = %s", (str(bk_code),))

        # Get the current date
        now = datetime.datetime.now()
        return_date = now.strftime('%Y-%m-%d')

        # Adding data to history

        # Getting the id of the book in the history table
        sql = 'SELECT id FROM history WHERE {} = %s ORDER BY id DESC LIMIT 1'.format('book_code')
        cur.execute(sql, (bk_code,))

        row = cur.fetchone()

        if row is None:
            id = None
        else:
            id = row[0]

        # updating the history table with the return date
        sql = 'UPDATE {} SET {} = %s WHERE id = %s'.format('history', 'returned_date')
        cur.execute(sql, (return_date, id))

        # getting the issue date
        query = 'SELECT issue_date FROM history WHERE {} = %s'.format('id')
        cur.execute(query , (id,))
        issue_date = cur.fetchone()[0]

        # Getting the number of days between issue and return of book
        num_of_days = (now.date() - issue_date).days

        # fine calculation
        if num_of_days > 14:
            print("You have been fined with " , (num_of_days - 14)*4 , "rupees")



        
        


"""
Please ensure that when passing the data pass a string 
"""
sol = book_lending()
# sol.del_map('909' )
# sol.book_student_map('909' , '43')
cur.close()
conn.close()