#!/usr/bin/python3
# -*- coding: latin-1 -*-

import psycopg2
 
def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = [
        """
        CREATE TABLE comments (
            comment_ip VARCHAR(50),
            comment_time TIMESTAMP,
            comment_message TEXT
        )
        """]
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
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
 
if __name__ == '__main__':
    print("Created")
    create_tables()