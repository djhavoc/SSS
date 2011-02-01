import MySQLdb
import config

class Connection:

    def __init__(self):
        ## establish db session
    	try:
    		self.connection = MySQLdb.connect (host = config.DB_HOST,
    								user = config.DB_USER,
    								passwd = config.DB_PASSWD,
    								db = config.DB_NAME)
    	except MySQLdb.Error, e:
    		print "Error %d: %s" % (e.args[0], e.args[1])
    		sys.exit (1)
    	self.cursor = self.connection.cursor (MySQLdb.cursors.DictCursor)
