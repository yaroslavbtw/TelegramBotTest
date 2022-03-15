import sqlite3

conn = None


def open_db():
    global conn
    if conn is None:
        conn = sqlite3.connect('usersId.db')


def close_db():
    global conn
    if conn is not None:
        conn.close()
        conn = None


def get_cursor():
    open_db()
    curs = conn.cursor()
    return curs


def check_user_in_db(chat_id, name):
    cur = get_cursor()
    cur.execute(f"SELECT * FROM `users` WHERE chat_id={chat_id};")
    if cur.fetchone() is None:
        cur.execute("INSERT INTO `users` (name, chat_id, num_question,test_started) VALUES(?, ?, 0, 0);", (name, chat_id))
        conn.commit()


def find_number_of_question(chat_id):
    cur = get_cursor()
    cur.execute(f"SELECT * FROM `users` WHERE chat_id={chat_id};")
    return cur.fetchone()[3]


def check_status(chat_id):
    cur = get_cursor()
    cur.execute(f"SELECT * FROM `users` WHERE chat_id={chat_id};")
    if cur.fetchone()[4] == 0:
        return False
    else:
        return True
