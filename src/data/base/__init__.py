import sqlite3

con = sqlite3.connect(r"data\base\main.db")
cur = con.cursor()


def init():
    cur.execute(f'CREATE TABLE IF NOT EXISTS users (userid INT NOT NULL PRIMARY \
    KEY, default_keyword CHAR(32) NOT NULL DEFAULT `#w`, language CHAR(64))')
    cur.execute('CREATE TABLE IF NOT EXISTS pictures (userid INT NOT NULL, \
    file_id VARCHAR(256) NOT NULL, keyword CHAR(64), \
    FOREIGN KEY (userid) REFERENCES userid (users))')
    con.commit()


def magic_func(_iter: tuple | list | dict, symbol=None):
    if symbol is None:
        symbol = ['?', ', ']

    res = ''
    for i, v in enumerate(_iter):
        if i != len(_iter):
            res += symbol[0] + symbol[1]
        else:
            res += symbol[0]

    return res


class Users:
    DEFAULT_KW = 0
    LANGUAGE = 1

    def __init__(self, userid):
        self.__uid = userid
        cur.execute('SELECT default_keyword, language FROM users WHERE userid = ?', (userid,))
        row = cur.fetchone()

        if row:
            self.__d = row
        else:
            cur.execute('INSERT INTO users (userid, language) VALUES (?, ?)',
                        (userid, None))
            con.commit()
            self.__d = ['w', None]

    def __call__(self, *args, **kwargs):
        if len(args) > 0:
            res = tuple()
            if len(self.__d) == 3:
                for i in args:
                    res += (self.__d[i],)

            return res

        into = str()
        vals = tuple()

        for k, v in kwargs:
            into += k
            vals += (v,)

        cur.execute(f'''INSERT OR REPLACE INTO users (userid, {into}) 
        VALUES (?, {[magic_func(vals)]})''', vals)

        con.commit()

    def lang(self, value=None):
        if value is None:
            return self.__d[self.LANGUAGE]
        else:
            cur.execute('INSERT OR REPLACE INTO users (userid, language) VALUES (?, ?)',
                        (self.__uid, value))
            con.commit()

    def default_keyword(self, value=None):
        if value is None:
            return self.__d[self.LANGUAGE]
        else:
            cur.execute('INSERT OR REPLACE INTO users (userid, default_value) VALUES (?, ?)',
                        (self.__uid, value))
            con.commit()


class Picture:
    def __init__(self, user_id, keyword=None, file_id=None):
        self.__d = [user_id, keyword]
        if file_id:
            cur.execute('INSERT INTO pictures (userid, file_id, keyword) \
                    VALUES (?, ?, ?)', (user_id, file_id, keyword))
            con.commit()
        else:
            cur.execute('SELECT file_id FROM pictures WHERE userid = ? AND keyword = ?',
                        (user_id, keyword))
            self.__r = cur.fetchall()

    def get(self):
        return self.__r

    def set(self, file_id, keyword=None):
        kw = keyword if keyword else self.__d[1]
        user_id = self.__d[0]
        cur.execute('INSERT INTO pictures (userid, file_id, keyword) \
                VALUES (?, ?, ?)', (user_id, file_id, kw))
        con.commit()

    @staticmethod
    def edit_default_keyword(userid, keyword):
        cur.execute('SELECT default_keyword FROM users WHERE userid = ?', (userid,))
        row = cur.fetchone()
        print(row)
        cur.execute('UPDATE pictures SET keyword = ? WHERE userid = ? AND keyword = ?',
                    (keyword, userid, row[0]))
        con.commit()
        cur.execute('UPDATE users SET default_keyword = ? WHERE userid = ?', (keyword, userid))
        con.commit()
