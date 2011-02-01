## launch web app

import sys
sys.stderr = None #Comment this line for better error checking - Wrenbjor 10-23-2010
sys.path.append('Classes/')
sys.path.append('Classes/webpy/')
import web 
from WebView import *

## define views
urls = ( 
'/', 'Status',
'/status.*', 'Status',
'/do.*', 'RunAdd',
'/run.*', 'RunChecks',
'/new.*', 'AddCheck',
'/delete/(.*)', 'Delete'
    )

app = web.application(urls, globals())
        
if __name__ == "__main__":
    app.run()
