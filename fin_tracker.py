
import psycopg2
from datetime import datetime
from secret import DATABASE_PASSWORD

global_user = None

def open_connection():
    conn = psycopg2.connect(
        database="fin_manager_python",
        host="localhost",
        user="postgres",
        password=DATABASE_PASSWORD,
        port=5432
    )
    return conn


def close_connection(conn, cur):
    cur.close()
    conn.close()


def create_database():
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(
        f"""
        create table if not exists Users(
            user_id bigint primary key,
            fullname varchar(100),
            username varchar(200),
            created_at timestamp,
            password varchar(10)
        );

        create table if not exists Income(
            id serial primary key,
            user_id bigint references Users(user_id),
            amount bigint,
            category varchar(150),
            description text,
            created_at timestamp
        );

        create table if not exists Expense(
            id serial primary key,
            user_id bigint references Users(user_id),
            amount bigint,
            category varchar(150),
            description text,
            created_at timestamp
        );
        
        """
    )
    conn.commit()
    close_connection(conn, cur)


create_database()

# def register_user():
#     conn = open_connection()
#     cur = conn.cursor()
#     cur.execute("""
#
#     """)
#     conn.commit()
#     close_connection(conn,cur)
#
# register_user()

def login():
    conn = open_connection()
    cur = conn.cursor()
    us = int(input("enter user_id: "))
    passw = input("enter password: ")
    cur.execute(f"""
                select user_id from register where user_id = '{us}' and password = '{passw}'"""
                )
    global global_user
    user = cur.fetchone()
    if user:
        global_user = user[0]
    else:
        print("incorrect user_id or password")
    conn.commit()
    close_connection(conn,cur)
    if global_user:
        print(f"you are successfully logged in as: {global_user}")



def add_income():
    conn = open_connection()
    cur = conn.cursor()
    if global_user:
        try:
            amount = int(input("enter amount: "))
            category = None
            cat = input("SELECT Category \n"
                             "1. Salary: \n"
                             "2. Gift: \n"
                             "3. Loan: \n"
                             "4. Freelance: \n"
                             "5. Other: ")
            if cat == "1":
                category = "Salary"
            elif cat == "2":
                category = "Gift"
            elif cat == "3":
                category = "Loan"
            elif cat == "4":
                category = "Freelance"
            elif cat == "5":
                category = "Other"
            cur.execute(f"""
            insert into income(user_id, amount, category, created_at) values
            ('{global_user}', '{amount}', '{category}', '{datetime.now()}')
            """)
            print(f"{amount} as {category} was successfully added to your income")
            conn.commit()
            close_connection(conn,cur)
        except:
            print("it appears you entered wrong value or some other error")
    else:
        print("you have to login to insert")

def get_income():
    try:
        conn = open_connection()
        cur = conn.cursor()
        if global_user:
            cur.execute(f"""
            select id, amount, category from income where user_id = '{global_user}'
            """)
        res = cur.fetchall()
        for item in res:
            print(item)

    except:
        print("you are either not logged in or value error")


def update_income():
    if global_user:
        try:
            conn = open_connection()
            cur = conn.cursor()
            id = int(input("enter ID you of the income you want to update: "))
            cur.execute(f"""
            select id from income where user_id = '{global_user}' and id = {id}
            """)
            conn.commit()
            res = cur.fetchone()
            if res:
                update_amount = int(input("enter new amount: "))
                update_category = input("enter new category: ")

                cur.execute(f"""
                update income
                set amount = '{update_amount}',
                category = '{update_category}'
                where id = {id}
                
                """)
                conn.commit()
                close_connection(conn, cur)
                print(f"ID {id} was successfully updated. Amount is now: {update_amount} and Category is now: {update_category}")
            else:
                print("you entered ID that does not exist. please enter correct ID.")
        except:
            print("something is wrong or value error")
    else:
        print("please login to update")



def del_income():
    conn = open_connection()
    cur = conn.cursor()
    if global_user:
        try:
            cur.execute(f"""
            delete from income where user_id = '{global_user}'
            """)
            conn.commit()
            close_connection(conn,cur)
            print("your income was deleted successfully")
        except:
            print("you are not logged in or something is wrong")
    else:
        print("you are not logged in. please login to delete")

def del_expense():
    conn = open_connection()
    cur = conn.cursor()
    if global_user:
        try:
            cur.execute(f"""
            delete from expense where user_id = '{global_user}'
            """)
            conn.commit()
            close_connection(conn,cur)
            print("your expense was deleted successfully")
        except:
            print("you aren't logged in or something is wrong")
    else:
        print("you are not logged in. please login to delete")

def add_expense():
    conn = open_connection()
    cur = conn.cursor()
    if global_user:

        amount = int(input("enter amount: "))
        category = None
        cat = input("SELECT Category \n"
                         "1. Entertainment: \n"
                         "2. Rent: \n"
                         "3. Lend money: \n"
                         "4. Shopping: \n"
                         "5. Other Expenses: ")
        if cat == "1":
            category = "Entertainment"
        elif cat == "2":
            category = "Rent"
        elif cat == "3":
            category = "Lend money"
        elif cat == "4":
            category = "Shopping"
        elif cat == "5":
            category = "Other Expenses"
        cur.execute(f"""
        insert into expense(user_id, amount, category, created_at) values
        ('{global_user}', '{amount}', '{category}', '{datetime.now()}')
        """)
        print(f"{amount} as {category} was successfully added to your expenses")
        conn.commit()
        close_connection(conn,cur)
    else:
        print("you have to login to insert")

def get_expense():
    try:
        conn = open_connection()
        cur = conn.cursor()
        if global_user:
            cur.execute(f"""
            select id, amount, category from expense where user_id = '{global_user}'
            """)
        res = cur.fetchall()
        for item in res:
            print(item)

    except:
        print("you are either not logged in or value error")


def update_expense():
    if global_user:
        try:
            conn = open_connection()
            cur = conn.cursor()
            id = int(input("enter ID you of the expense you want to update: "))
            cur.execute(f"""
            select id from expense where user_id = '{global_user}' and id = {id}
            """)
            res = cur.fetchone()
            if res:
                update_amount = int(input("enter new amount: "))
                update_category = input("enter new category: ")

                cur.execute(f"""
                update expense
                set amount = '{update_amount}',
                category = '{update_category}'
                where id = {id}
    
                """)
                conn.commit()
                close_connection(conn, cur)
                print(
                    f"ID {id} was successfully updated. Amount is now: {update_amount} and Category is now: {update_category}")
            else:
                print("There is no such ID. Please enter correct ID number.")
        except:
            print("something is wrong or value error")
    else:
        print("please login to update")


def summary():
    conn = open_connection()
    cur = conn.cursor()
    if global_user:
        cur.execute(f"""
        select sum(amount) from income where user_id = '{global_user}'
        """)
        conn.commit()
        res = cur.fetchone()
        inc_total = res[0] or 0

        cur.execute(f"""
        select sum(amount) from expense where user_id = '{global_user}'
        """)
        conn.commit()
        res2 = cur.fetchone()
        exp_total = res2[0] or 0
    close_connection(conn,cur)
    total_summary = inc_total - exp_total
    print(f"""
    your income total: {inc_total} \n
    your expense total: {exp_total} \n
    Your TOTAL Summary is: {inc_total} - {exp_total} = {total_summary}

""")

def logout():
    global global_user
    global_user = None
    print("You are now logged out")
while True:
    if global_user:
        print(f"You are logged in as {global_user}")
    choice = input("1. login: \n"
                   "2. add income: \n"
                   "3. get income: \n"
                   "4. update income: \n"
                   "5. add expense: \n"
                   "6. get expense: \n"
                   "7. update expense \n"
                   "8. delete income \n"
                   "9. delete expense \n"
                   "10. summary \n"
                   "11. logout")

    if choice == "1":
        login()

    elif choice == "2":
        add_income()

    elif choice == "3":
        get_income()

    elif choice == "4":
        update_income()

    elif choice == "5":
        add_expense()

    elif choice == "6":
        get_expense()

    elif choice == "7":
        update_expense()

    elif choice == "8":
        del_income()

    elif choice == "9":
        del_expense()

    elif choice == "10":
        summary()

    elif choice == "11":
        logout()

