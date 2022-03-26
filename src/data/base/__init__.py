import sqlite3

con = sqlite3.connect(r"data\base\main.db")
cur = con.cursor()


def init():
    """
    Инициализация базы данных (создание таблиц, если они не существуют)
    :return: None
    """
    cur.execute(f'CREATE TABLE IF NOT EXISTS users (userid INT NOT NULL PRIMARY \
    KEY, default_keyword CHAR(32) NOT NULL DEFAULT `#w`, language CHAR(64))')
    cur.execute('CREATE TABLE IF NOT EXISTS pictures (userid INT NOT NULL, \
    file_id VARCHAR(256) NOT NULL, keyword CHAR(64), \
    FOREIGN KEY (userid) REFERENCES userid (users))')
    con.commit()


def magic_func(_iter: tuple | list | dict, symbol=None):
    """
    Магическая функция для SQL запросов
    :param _iter:
    :param symbol:
    :return:
    """
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

    user_data = {}

    def __init__(self, userid):
        """
        Класс-обёртка над SQL таблицей users для упрощенной работы с ней.
        :param userid: telegram userid
        """
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
        """
        Метод вызова объекта класса, в будущем возможно пригодится.
        :param args: for get data
        :param kwargs: for set data
        :return: result of selecting from `users` or None
        """
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
        """
        Метод для получения/изменения языка пользователя.
        :param value: language
        :return:
        """
        if value is None:
            return self.__d[self.LANGUAGE]
        else:
            cur.execute('INSERT OR REPLACE INTO users (userid, language) VALUES (?, ?)',
                        (self.__uid, value))
            con.commit()

    def storage(self, *args, default=None, **kwargs):
        try:
            udata = self.user_data[self.__uid]
        except KeyError:
            udata = self.user_data[self.__uid] = {}

        if len(kwargs):
            for k, v in kwargs.items():
                udata.update(k=v)
        if len(args):
            res = tuple()
            for k in args:
                try:
                    a = udata[k]
                except KeyError or IndexError:
                    return None
                else:
                    res += (a,)

            return res



class Picture:
    def __init__(self, user_id, keyword=None, file_id=None):
        """
        Класс-обёртка над SQL таблицей picture для упрощённой работы с ней.
        :param user_id: Telegram user id
        :param keyword: keyword of picture (for searching or inserting)
        :param file_id: file_id of picture (only for inserting)
        """
        self.__d = [user_id, keyword]
        if file_id:
            cur.execute('INSERT INTO pictures (userid, file_id, keyword) \
                    VALUES (?, ?, ?)', (user_id, file_id, keyword))
            con.commit()
        else:
            cur.execute('SELECT file_id FROM pictures WHERE keyword LIKE ? AND userid = ?',
                        ('%' + keyword + '%', user_id))
            self.__r = cur.fetchall()
            print(self.__r)

    def __call__(self):
        """
        Метод для получения найденных file_id-ов из SELECT запроса в __init__
        :return: list of file_ids
        """
        return self.__r

    @staticmethod
    def edit_default_keyword(userid, keyword):
        """
        Статический метод для изменения дефолт-ключа
        :param userid: telegram userid
        :param keyword: new user default-keyword
        :return: None
        """
        cur.execute('SELECT default_keyword FROM users WHERE userid = ?', (userid,))
        row = cur.fetchone()
        print(row)
        cur.execute('UPDATE pictures SET keyword = ? WHERE userid = ? AND keyword = ?',
                    (keyword, userid, row[0]))
        con.commit()
        cur.execute('UPDATE users SET default_keyword = ? WHERE userid = ?', (keyword, userid))
        con.commit()
