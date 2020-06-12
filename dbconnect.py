import pymysql


def connection():
    conn = pymysql.connect(host="localhost",
                           user="root",
                           passwd="cookies!",
                           db="pythonprogramming")
    c = conn.cursor()
    return c, conn
