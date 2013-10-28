#!/usr/bin/python

import MySQLdb, sqlite3

from  functions import *

#############################################################################
def fetch_user_result():
 try:
    username = []
    foss = []
    # connect to online test (sqlite database)
    con = connect_django()

    # cursor object

    cursor = con.cursor()

    #query
    query = 'select distinct username, foss from mim_spokentutorialdetail where result_status="NULL";'

    c = execute_query(query, cursor)
    

    # fetch the row
    result = cursor.fetchall()
    for row in result:
        username.append(row[0])
        foss.append(row[1])

    for (a, b) in zip(username, foss):
        print a +"   "+ b
    close_connect(con)
    return username, foss
 except Exception, e:
    
    print e

#
############################################################################
#fetch_user_result()
##############################################################################
"""Insert result into moodle"""
def insert_moodle(user, fos, percent):
 try:
    # Connect to moodle
    db2 = connect_moodle()

    # cursor object
    cursor2 = db2.cursor()

    query2 = 'insert into user_result(username, foss, percent_score) value("%s","%s", %f)' % (user, fos, percent)

    print query2
    # execute query
    c = execute_query(query2, cursor2)

    db2.commit()
    close_connect(db2)
 except Exception, e:
   
    print e


#query to fetch result in django
#"""select  sum(ea.marks) from exam_answer as ea inner join exam_answerpaper_answers as eaa on  eaa.answerpaper_id=35 and eaa.answer_id=ea.id;"""
#create table in moodle
#"""create table if not exists user_result (username varchar(25), foss varchar(25), percent_score decimal(4,2), primary key(username, foss) );"""
