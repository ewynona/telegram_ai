from db.db_connect import ConnectDB


class Use:
    def __init__(self, table_name):
        self.cur = ConnectDB(dbname='character_ai', host='localhost', user='bikbulat', password='bikbulat', port='5432')
        self._table_name = table_name

    def add_record(self, query):
        self.cur.query(f"INSERT INTO {self._table_name} {query}")

    def del_record(self, query):
        self.cur.query(f"DELETE FROM {self._table_name} {query}")

    def get_record(self):
        self.cur.query(f"SELECT * FROM {self._table_name}")
        return self.cur.fetch()

    def __del__(self):
        self.cur.close()


class UserInfo(Use):
    def __init__(self):
        super().__init__('user_info')

    def table_create(self):
        print(self._table_name)
        self.cur.query(f"CREATE TABLE IF NOT EXISTS {self._table_name} ("
                       "id SERIAL PRIMARY KEY,"
                       "user_id INTEGER NOT NULL UNIQUE,"
                       "username VARCHAR(32) NOT NULL,"
                       "name VARCHAR(64) NOT NULL,"
                       "surname VARCHAR(64),"
                       "reg_date TIMESTAMP DEFAULT DATE_TRUNC('second', NOW()),"
                       "current_character INTEGER,"
                       "FOREIGN KEY (current_character) REFERENCES characters(character_id) ON DELETE CASCADE"
                       ")")

    def add_user(self, user_id, username, name, surname):
        self.cur.query(f"INSERT INTO {self._table_name} (user_id, username, name, surname) VALUES("
                       f"'{user_id}', "
                       f"'{username}', "
                       f"'{name}', "
                       f"'{surname}')"
                       f"ON CONFLICT DO NOTHING")


class Characters(Use):
    def __init__(self):
        super().__init__('characters')

    def table_create(self):
        self.cur.query(f"CREATE TABLE IF NOT EXISTS {self._table_name} ("
                       "character_id SERIAL PRIMARY KEY,"
                       "character VARCHAR)")

    def add_character(self, character):
        self.cur.query(f"INSERT INTO {self._table_name} (character) VALUES({character})")


class CharacterMsg(Use):
    def __init__(self):
        super().__init__('character_msg')

    def table_create(self):
        self.cur.query(f"CREATE TABLE IF NOT EXISTS {self._table_name} ("
                       "msg_id SERIAL PRIMARY KEY,"
                       "user_id INTEGER NOT NULL,"
                       "character_id INTEGER NOT NULL,"
                       "msg TEXT,"
                       "msg_date TIMESTAMP DEFAULT DATE_TRUNC('second', NOW()),"
                       "FOREIGN KEY (user_id) REFERENCES user_info(user_id) ON DELETE CASCADE,"
                       "FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE)")

    def add_msg(self, user_id, character_id, msg):
        self.cur.query(f"INSERT INTO {self._table_name} (user_id, character_id, msg) VALUES("
                       f"{user_id},"
                       f"{character_id},"
                       f"{msg})")




