#!/usr/bin/python

from functions import connect_sptu, close_connect, execute_query, \
connect_moodle, connect_django
from datetime import date

import gc
print gc.isenabled()

moodle_uid_temp=[1,2,3,4,5,6,7,8,9]
foss_temp=['php-and-mysql','php','linux','linux','linux','linux','linux','linux','linux']


ST = 'from spoken tutorial'
date = date.today()


def fetch_user():
  try:
    
    testcode = []
    foss = []
    moodle_uid = []
    username = []
    password = []
    status = []

 
    db = connect_sptu()
    
    # cursor object
    cursor = db.cursor()

    # retrieve user_id with status 1 from attendance_register
    query = 'select ar.moodle_uid, ar.test_code, tr.foss_category from attendance_register as ar inner join test_requests as tr on tr.test_code=ar.test_code and ar.status = 1 and ar.id < 20' 
    print query
    cursor = execute_query(query, cursor)
    

    # fetch the row
    rows = cursor.fetchall()
    for row in rows:
        #print "%s\t%s\t%s\n" % (row[0], row[1], row[2])
        moodle_uid.append(row[0])
        testcode.append(row[1])
        foss.append(row[2])

    # close connection
    close_connect(db)
    #print moodle_uid
    #for (a,b) in zip(moodle_uid, foss):
       # print a,b
    fetch_password(moodle_uid, username, password)
    insert_django(username, password, foss, testcode, moodle_uid, status)
     
    return username, foss, status
  except Exception, e:
    #db.close()
    print e

##############################################################################
"""
create table in mim

"""
###############################################################################
#fetch()
###############################################################################

def fetch_password(moodle_uid, username, password): 
 try:
    # Connect to moodle
    db2 = connect_moodle()

    # cursor object
    cursor2 = db2.cursor()

    query2 = 'select username, password, id  from mdl_user  where id in ('+ ",".join(str(x) for x in moodle_uid_temp)+')'
    print query2
    # execute query
    cursor2 = execute_query(query2, cursor2)

    data2 = cursor2.fetchall()
    for d in data2:
        print d[0], d[1], d[2]
        username.append(d[0])
        password.append(d[1])

    for u in username:
        print u
    for p in password:
        print p
    close_connect(db2)
 except Exception,e:
    # db2.close()
    print e

###############################################################################
#if moodle_uid:
#    print len(moodle_uid)
    #fetch_password()
    #update_status()
###############################################################################
def update_status():
    """
        update the status to 2 in attendance_register
    """
    try:
        db = connect_sptu()
        cursor = db.cursor()
        for (uid, tc) in zip(moodle_uid, testcode):
            query = 'update attendance_register set status =22 where moodle_uid=%d and test_code="%s";' %(uid, tc)
            print query
            cursor = execute_query(query, cursor)
            db.commit()
    except Exception, e:
         print e        
###############################################################################
###############################################################################
""" 
    insert into mim table
"""
##############################################################################

###############################################################################
"""
    insert users into django auth_user and exam_profile table and exam_spokentutorialuser
"""

def insert_django(username, password, foss, testcode, moodle_uid, status):
 try:
    # connect to online test (sqlite database)
    con = connect_django()
    # cursor object
    cursor3 = con.cursor()

    insert  = 'insert into auth_user(username,password,first_name,last_name,email,is_staff,is_active,is_superuser,last_login,date_joined) values'

 
    for (user,passw) in zip(username, password):
        query3 = '%s ( "%s","%s", "%s","%s", "%s", 0, 1, 0, "%s", "%s")' % (insert, user, passw, ST, ST, ST, date, date)
        print query3
        cur = execute_query(query3, cursor3)
        if cur is not None:
            print "here"
            query_profile = 'insert into exam_profile(user_id,roll_number,institute,department,position) values (last_insert_rowid(),"sptu","sptu","sptu","sptu" );'
            
            print query_profile
            execute_query(query_profile, cursor3)
            # Commit your changes in the database
            
            con.commit()
            # insert into exam_sptu_user
            status.append("USER_ADDED")
        else:
            status.append("USER_NOT_ADDED")
    insert_user_foss(con, cursor3, username, foss)
    insert_mim(con, cursor3, moodle_uid, username, password, foss, testcode, status)
    close_connect(con)
 except Exception,e:
    print e
###############################################################################
        
###############################################################################
def insert_user_foss(CON, cursor, username, foss):
    """
        insert user and foss into exam_sptu_user, for activating correponding quiz
    """
    try:
        for (user, fos) in zip(username, foss):
            query = 'INSERT INTO exam_spokentutorialuser (sptu_username, foss)\
                     SELECT "%s" as sptu_username, "%s" as foss WHERE NOT \
                     EXISTS(SELECT * FROM exam_spokentutorialuser WHERE \
                     foss="%s" and sptu_username = "%s");'\
                     % (user, fos, fos, user)
            print query
            execute_query(query, cursor)
            CON.commit()
        
    except Exception, e:
        print e
###############################################################################
def insert_mim(CON, cursor, moodle_uid, username, password, foss, testcode, status):
    """
       insert user details in mim table
    """
    try:
        for (uid, user, passwd, fos, tc, stat ) in zip(moodle_uid_temp, username, password, foss, testcode, status):
            query = 'insert into mim_spokentutorialdetail (user_id, username, password, foss, testcode, status, result, result_status, date_added) values (%d, "%s", "%s", "%s", "%s", "%s", "%f", "%s", "%s")' %(uid, user, passwd, fos, tc, stat, 0, "NULL", date)
            print query
            execute_query(query, cursor)
            CON.commit()
    except Exception, e:
        print e 
###############################################################################
#insert_django()
