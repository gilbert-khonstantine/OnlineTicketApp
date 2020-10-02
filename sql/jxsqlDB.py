import sqlite3
from sqlite3 import Error
import time


# connect to db file
def connectDB(db):
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        return e
    return conn


# creates table, if file doesnt exist creates file and table
def createtableDB(db, sql):
    try:
        conn = connectDB(db)
        if conn is not None:
            c = conn.cursor()
            c.execute(sql)
            c.close()
        else:
            return "Error! cannot create the database connection."
    except Error as e:
        return e


# Insert purchase
def updatePurchaseHist(db, uid, values):
    try:
        conn = connectDB(db)
        sql = """INSERT INTO PurHist (uid, product, amount,cost) VALUES (?,?,?,?)"""
        if conn is not None:
            c = conn.cursor()
            for i in range(len(values)):
                data = (uid, values[i][0], values[i][1], values[i][2])
                time.sleep(1)
                c.execute(sql, data)
                conn.commit()
            c.close()
    except Error as e:
        return e


# get data from DB
def getPurchaseHist(uid):
    try:
        redata = ""
        conn = connectDB(db)
        sql = """SELECT * FROM PurHist WHERE uid=""" + str(uid)
        if conn is not None:
            c = conn.cursor()
            c.execute(sql)
            # list format
            data = c.fetchall()
            conn.commit()
            c.close()
            for item in data:
                string = ','.join([str(item[i]) for i in range(1, 4)])
                redata += string + ","
            redata = redata[:-1]
            return redata
    except Error as e:
        return e


# sql syntax to create database
'''
db = r"..\\PurHistTest.db"
purhistsql = """CREATE TABLE IF NOT EXISTS PurHist(
                uid INTEGER NOT NULL,
                product VARCHAR(255) NOT NULL,
                amount INTEGER NOT NULL,
                cost INTEGER NOT NULL,
                datecreated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(uid, product, datecreated)
                );"""
'''
