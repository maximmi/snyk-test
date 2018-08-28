#!/usr/bin/python

import pymysql.cursors
import pymysql
import os

print os.environ

print(os.environ.get('MYSQL_HOST'))

def test_mysqldb():

    connection = pymysql.connect(host=os.environ.get('MYSQL_HOST'),
                                   user=os.environ.get('MYSQL_USER'),
                                   password=os.environ.get('MYSQL_PASS'),
                                   db=os.environ.get('MYSQL_DBNAME'),
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create new table
            sql = "CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255), password VARCHAR(255))"
            cursor.execute(sql)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()


        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            assert result == {'id': 1, 'password': 'very-secret'}
    finally:
        connection.close()