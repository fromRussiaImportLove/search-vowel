#DataBase content manager module
import mysql.connector

class ConnectionError(Exception):
    pass

class CredentialsError(Exception):
    pass

class SQLError(Exception):
    pass

class UseDatabase:

    def __init__(self, config: dict) -> None:
        """Initialization configuration for connect to DB"""
        self.configuration = config


    def __enter__(self) -> 'cursor':
        """Make connect to DB and initial cursor"""
        try:
            self.conn = mysql.connector.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
        except mysql.connector.errors.InterfaceError as err:
            raise ConnectionError(err)
        except mysql.connector.errors.ProgrammingError as err:
            raise CredentialsError(err)

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        """Commit any change, disable cursor, disconnect from DB"""
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type is mysql.connector.errors.ProgrammingError:
            raise SQLError(exc_value)
        elif exc_type:
            raise exc_type(exc_value)


def select_SQL(cursor: 'self.cursor', _SQL: 'SQL select') -> 'SQL Answer':
        cursor.execute(_SQL)
        return cursor.fetchall()


        
