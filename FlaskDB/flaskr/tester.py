#!/usr/bin/python3
# -*- coding: latin-1 -*-

import psycopg2
import time
 
 
def insert_message(ip_message, message):
    """ insert a new item into the comments table """
    sql = """INSERT INTO comments(comment_ip, comment_time, comment_message)
             VALUES(%s, %s, %s);"""
    conn = None
    try:
        POSTGRESDATABASE = "flaskdb"
        POSTGRESUSER = "ignacio"
        POSTGRESPASS = "holas"
        conn = psycopg2.connect(
            database=POSTGRESDATABASE,
            user=POSTGRESUSER,
            password=POSTGRESPASS
        )
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (ip_message, time.strftime('%Y-%m-%d %H:%M:%S'), message))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
if __name__ == "__main__":
    insert_message("127.0.0.1", "holiiiiiiiii soy un mensaje")