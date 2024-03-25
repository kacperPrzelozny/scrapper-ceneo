from app.Services.SQLiteService import SQLiteService


class Model:
    @staticmethod
    def executeQuery(sql, args=None):
        if args is None:
            args = []
        db = SQLiteService()
        connection = db.getConnection()
        cursor = connection.cursor()
        cursor.execute(sql, args)
        rows = cursor.fetchall()
        connection.commit()

        return rows
