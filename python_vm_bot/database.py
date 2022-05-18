import sqlite3

from config_reader import read_config_key

conn = sqlite3.connect(read_config_key('db_file'), check_same_thread=False)

cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, token STRING, folder STRING)')

cur.close()

# cur.execute('CREATE TABLE IF NOT EXISTS servers (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER)')


class entry(dict):
    __getattr__ = dict.get


def check_user(user_id):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO users (id) VALUES (?)', (user_id, ))
        conn.commit()
        cur.close()
        return True
    except sqlite3.IntegrityError:
        cur.execute('SELECT token FROM users WHERE id = ?', (user_id, ))
        user = cur.fetchone()
        cur.close()
        return not user[0]


def get_user_data(user_id):
    cur = conn.cursor()
    cur.execute('SELECT token, folder FROM users WHERE id = ?', (user_id, ))
    user = cur.fetchone()
    cur.close()
    if user is not None:
        res = {
            'token': user[0],
            'folder': user[1]
        }
        return res
    return None


def clear_user(user_id):
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE id = ?', (user_id, ))
    cur.close()


def set_token(user_id, token):
    cur = conn.cursor()
    cur.execute('UPDATE users SET token = ? WHERE id = ?', (token, user_id))
    conn.commit()
    cur.close()


def set_folder(user_id, folder):
    cur = conn.cursor()
    cur.execute('UPDATE users SET folder = ? WHERE id = ?', (folder, user_id))
    conn.commit()
    cur.close()
