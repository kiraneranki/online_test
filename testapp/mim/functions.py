import MySQLdb, sqlite3

###############################################################################

def connect_sptu():
    """
       Connect to the database
    """
    try:
        # Open database connection
        DB = MySQLdb.connect('localhost', 'root', 'root', 'OTCworksop')
        return DB
    except Exception, e:
        print e

###############################################################################

def close_connect(DB):
    """
       Close connection to the database
    """
    try:
        DB.close()
    except Exception, e:
        print e

###############################################################################

def execute_query(query, cursor):
    """
       Execute query
    """
    try:
        c = cursor.execute(query)
        print c
        return cursor
    except Exception, e:
        print e

###############################################################################

def connect_moodle():
    """
       Connect to the database
    """
    try:
        # Open database connection
        DB = MySQLdb.connect('localhost', 'root', 'root', 'newmoodle2_4')
        return DB
    except Exception, e:
        print e

###############################################################################

def connect_django():
    """
        connect to the database
    """
    try:
        CON = sqlite3.connect('/home/ttt/github-p/test/online_test/testapp/exam.db')
        print CON
        return CON
    except Exception, e:
        print e

############################################################################### 
