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

    def book_student_map(self , bk_code , st_id):
        """the agument that are needed are the book code and the student ID
            if the book is already issued it can't be given to the student
            also ensure that a single student can only take 'N' books at a time
            extra featuer that can be added is the time the book is issued and the time it is returned
            make a fine calculation for late returning the book"""
        sql = """SELECT name FROM students WHERE id = %s""";
        cur.execute(sql , (str(st_id) ,))
        student_name = cur.fetchone()[0]

        sql = """SELECT phone FROM students WHERE id = %s""";
        cur.execute(sql , (str(st_id) ,))
        student_contact = cur.fetchone()[0]

        try:
            sql = """INSERT INTO book_student_map (book_code, student_id , student_name , student_contact) VALUES (%s, %s , %s , %s)""";
            cur.execute(sql , (str(bk_code) , str(st_id) , str(student_name) , str(student_contact)))
            # sql = """INSERT INTO book_student_map (book_code, student_id) VALUES (%s, %s)""";
            # cur.execute(sql , (str(bk_code) , str(st_id)))
        except:
            print("Book is not available")


        
        


"""
Please ensure that when passing the data pass a string 
"""
sol = book_lending()
sol.book_student_map('43' , '566')
cur.close()
conn.close()