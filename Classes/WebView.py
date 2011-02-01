import subprocess
import Service
import web
import re
import MySQLdb
import config


class Delete:
    def GET(self, id):
        delID = web.input(id=None)
        delID = delID.id
        query = 'DELETE FROM services,results,status USING services LEFT JOIN results ON results.services_id = "%s" LEFT JOIN status ON status.service_id = "%s" WHERE services.id = "%s"' % (delID,delID,delID)

        db = MySQLdb.connect (host = config.DB_HOST,
                                           user = config.DB_USER,
                                           passwd = config.DB_PASSWD,
                                           db = config.DB_NAME)
        c=db.cursor()
        c.execute(query)
        web.seeother('/status',absolute=True)

class RunAdd:

    def POST(self):
        monitor_option = web.input(_method="POST")
        option = monitor_option.simple_option
        tcp_ip = monitor_option.tcp_ip
        tcp_title = monitor_option.tcp_title
        tcp_port = monitor_option.tcp_port
        http_title = monitor_option.http_title
        http_url = monitor_option.http_url
        pop3_title = monitor_option.pop3_title
        pop3_ip = monitor_option.pop3_ip
        smtp_title = monitor_option.smtp_title
        smtp_ip = monitor_option.smtp_ip
        icmp_title = monitor_option.icmp_title
        icmp_ip = monitor_option.icmp_ip
        m_title = monitor_option.mysql_title
        m_hostname = monitor_option.mysql_hostname
        m_user = monitor_option.mysql_user
        m_pass = monitor_option.mysql_pass
        m_port = monitor_option.mysql_port
        m_db = monitor_option.mysql_db
        i_title = monitor_option.ipsec_title
        i_gateway = monitor_option.ipsec_gateway
        i_group = monitor_option.ipsec_group
        i_user = monitor_option.ipsec_user
        i_pass = monitor_option.ipsec_pass
        i_secret = monitor_option.ipsec_secret
        empty_value = """One or more Value(s) are missing."""
        if ( len(option) > 0 ):
            if(option == 'tcp'):
                pattern = r"^([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])$"
                re_ip = re.compile(pattern)
                match = re_ip.match(tcp_ip)
                if( match != None ):
                    if( len(tcp_title) > 0 ) and ( len(tcp_ip) > 0 ) and ( len(tcp_port) > 0 ):
                        query = 'INSERT INTO services (title,kind,tcp_port,tcp_ip) values ("%s","%s","%s","%s")' %  (tcp_title,option,tcp_port,tcp_ip)
                else:
                    return "Invalid IP Address"
            elif(option == 'mysql'):
                if( len(m_title) > 0 ) and ( len(m_db) > 0 ) and ( len(m_hostname) > 0 ) and ( len(m_user) > 0 ) and ( len(m_pass) > 0 ) and ( len(m_port) > 0 ):
                    query = 'INSERT INTO services (title,kind,db_name,db_host,db_port,db_user,db_pass) values ("%s","%s","%s","%s","%s","%s","%s")' % (m_title,option,m_db,m_hostname,m_port,m_user,m_pass)
                else:
                    return empty_value
            elif(option == 'smtp'):
                if( len(smtp_title) > 0 ) and ( len(smtp_ip) > 0 ):
                        query = 'INSERT into services (title,kind,smtp_ip) values ("%s","%s","%s") ' % (smtp_title,option,smtp_ip) 
                else:
                    return empty_value
            elif(option == 'icmp'):
                if( len(icmp_title) > 0 ) and ( len(icmp_ip) > 0 ):
                        query = 'INSERT into services (title,kind,icmp_ip) values ("%s","%s","%s") ' % (icmp_title,option,icmp_ip)
                else:
                    return empty_value
            elif(option == 'pop3'):
                if( len(pop3_title) > 0 ) and ( len(pop3_ip) > 0 ):
                        query = 'INSERT into services (title,kind,pop3_ip) values ("%s","%s","%s") ' % (pop3_title,option,pop3_ip)
                else:
                    return empty_value
            elif(option == 'ipsec'):
                if( len(i_title) > 0 ) and ( len(i_gateway) > 0 ) and ( len(i_group) > 0 ) and ( len(i_user) > 0 ) and ( len(i_secret) > 0 ) and ( len(i_pass) > 0 ):
                    query = 'INSERT into services(title,kind,ipsec_gateway,ipsec_group,ipsec_secret,ipsec_user,ipsec_pass) values ("%s","%s","%s","%s","%s","%s","%s")' % (i_title,option,i_gateway,i_group,i_secret,i_user,i_pass)
                else:
                    return empty_value
            elif(option == 'http'):
                if( len(http_title) > 0 ) and ( len(http_url) > 0 ):
                    query = 'INSERT into services (title,kind,http_url) values ("%s","%s","%s")' % (http_title,option,http_url)
                else:
                    return empty_value
            db = MySQLdb.connect (host = config.DB_HOST,
                                               user = config.DB_USER,
                                               passwd = config.DB_PASSWD,
                                               db = config.DB_NAME)
            c=db.cursor()
            c.execute(query)
            service_id = db.insert_id()
            c.execute("""
                INSERT INTO results (id,services_id)
                values (NULL,%s)
                """, (service_id))
            db.commit()
            web.seeother('/status',absolute=True)
        else:
            web.seeother('/status',absolute=True)
class Status:

    ## fetch all checks data and display
    def GET(self):
	
        self.serviceList = Service.Listing()
       
        content = """
        <html>
        <head>
        <title>Simple Server Status</title>
        <link rel="stylesheet" href="static/styles/reset.css" type="text/css" media="screen" />
        <link rel="stylesheet" href="static/styles/960.css" type="text/css" media="screen" />
        <link href='http://fonts.googleapis.com/css?family=Droid+Sans:bold' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" href="static/styles/norm.css" type="text/css" media="screen" />
        <script src="static/js/jquery.js" type="text/javascript"></script>
                  <script type="text/javascript">
                                          jQuery(document).ready(function() {
                                          jQuery(".button").click(function() {
                                                  var input_string = $$("input#textfield").val();
                                                  jQuery.ajax({
                                                          type: "POST",
                                                          data: {textfield : input_string},
                                                          success: function(data) {
                                                          jQuery('#foo').html(data).hide().fadeIn(1500);
                                                          },
                                                          });
                                                  return false;
                                                  });
                                          });
           
                                  </script>
        </head>
        <body>
        <div id="dhtmltooltip"></div>
        <script type="text/javascript">
        var offsetxpoint=-60 //Customize x offset of tooltip
        var offsetypoint=20 //Customize y offset of tooltip
        var ie=document.all
        var ns6=document.getElementById && !document.all
        var enabletip=false
        if (ie||ns6)
        var tipobj=document.all? document.all["dhtmltooltip"] : document.getElementById? document.getElementById("dhtmltooltip") : ""

        function ietruebody(){
                        return (document.compatMode && document.compatMode!="BackCompat")? document.documentElement : document.body
                        }

        function ddrivetip(thetext, thecolor, thewidth){
                        if (ns6||ie){
                                if (typeof thewidth!="undefined") tipobj.style.width=thewidth+"px"
                                if (typeof thecolor!="undefined" && thecolor!="") tipobj.style.backgroundColor=thecolor
                                tipobj.innerHTML=thetext
                                enabletip=true
                                return false
                                }
                        }

        function positiontip(e){
                        if (enabletip){
                                var curX=(ns6)?e.pageX : event.clientX+ietruebody().scrollLeft;
                                var curY=(ns6)?e.pageY : event.clientY+ietruebody().scrollTop;
                                //Find out how close the mouse is to the corner of the window
                                var rightedge=ie&&!window.opera? ietruebody().clientWidth-event.clientX-offsetxpoint : window.innerWidth-e.clientX-offsetxpoint-20
                                var bottomedge=ie&&!window.opera? ietruebody().clientHeight-event.clientY-offsetypoint : window.innerHeight-e.clientY-offsetypoint-20

                                var leftedge=(offsetxpoint<0)? offsetxpoint*(-1) : -1000

                                //if the horizontal distance isn't enough to accomodate the width of the context menu
                                if (rightedge<tipobj.offsetWidth)
                                //move the horizontal position of the menu to the left by it's width
                                tipobj.style.left=ie? ietruebody().scrollLeft+event.clientX-tipobj.offsetWidth+"px" : window.pageXOffset+e.clientX-tipobj.offsetWidth+"px"
                                else if (curX<leftedge)
                                tipobj.style.left="5px"
                                else
                                //position the horizontal position of the menu where the mouse is positioned
                                tipobj.style.left=curX+offsetxpoint+"px"

                                //same concept with the vertical position
                                if (bottomedge<tipobj.offsetHeight)
                                tipobj.style.top=ie? ietruebody().scrollTop+event.clientY-tipobj.offsetHeight-offsetypoint+"px" : window.pageYOffset+e.clientY-tipobj.offsetHeight-offsetypoint+"px"
                                else
                                tipobj.style.top=curY+offsetypoint+"px"
                                tipobj.style.visibility="visible"
                                }
                        }

        function hideddrivetip(){
                        if (ns6||ie){
                                enabletip=false
                                tipobj.style.visibility="hidden"
                                tipobj.style.left="-1000px"
                                tipobj.style.backgroundColor=''
                                tipobj.style.width=''
                                }
                        }

        document.onmousemove=positiontip
        </script>
        <div id="container" class="container_16">
        <div id="mainContent" class="grid_16">
        <div id="header" class="grid_8">
		<h1>Simple Server Status</h1>
		</div>
		<div id="spacer" class="grid_6">&nbsp;</div>	
		<div id="settings" class="grid_1"><a href="/new/"><img src="static/images/preferences_system.png" width="32" height="32"></a></div>
        <br /><br /><br />
		<div id="launcherbutton"><button id='run'>Run Checks Now</button></div>
          <br>
        """

        ## mysql
        listOfChecks = self.serviceList.mysql()
        if (listOfChecks.rowcount > 0):
            content += "<script src='static/js/csspopup.js' type='text/javascript'></script>"
            content += "<div class='checkModule grid_15'>"
            content += "<div class='checkName grid_6'><h2>MySQL</h2></div>"
            content += "<div class='grid_15'>"
            content += "<table class='checkTable' width='98%'>"
            content += "<thead><tr><th><b>status</b></th><th><b>title</b></th><th><b>when</b></th><th><b>database</b></th><th><b>host</b></th><th><b>user</b></th></tr></thead>"
            content += "<tbody>"
            for item in listOfChecks.fetchall():
                lastCheck = item['last_check']
                serviceID = item['services_id']
                myStatus = item['status']
                content += '<tr>'
                if(myStatus == 'bad'):
                    db = MySQLdb.connect (host = config.DB_HOST,
                                                       user = config.DB_USER,
                                                       passwd = config.DB_PASSWD,
                                                       db = config.DB_NAME)
                    c=db.cursor()
                    query = """SELECT status FROM status where check_date = "%s" AND service_id = "%s" """ % (lastCheck, serviceID)
                    c.execute(query)
                    curStatus = c.fetchall()
                if(myStatus == None):
                    content += '<td><img src=\"static/images/None.png\" width=15 height=15 /></td>'
                elif(myStatus == 'good'):
                    content += '<td><img src=\"static/images/good.png\" width=15 height=15 /></td>'
                else:
                    color='gray'
                    go = """ %s """ % (curStatus)
                    s = go
                    for i in """"'(),""":
                        if i in s:
                            s=s.replace(i,"")
                            returnStatus = s
                    content += """<td><img onMouseover="ddrivetip(' Error: %s','%s', 300)" onMouseout="hideddrivetip()" src="static/images/%s.png" width=
15 height=15 /></td>""" % (returnStatus,color,str(item['status']))

                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + str(item['last_check']) + '</td>'
                content += '<td>' + item['db_name'] + '</td>'
                content += '<td>' + item['db_host'] + '</td>'
                content += '<td>' + item['db_user'] + '</td>'
                content += '</tr>'        
            content += "</tbody>"
            content += "</table></div></div>"

        ## http
        listOfChecks = self.serviceList.http()
        if (listOfChecks.rowcount > 0):
            content += "<div class='checkModule grid_15'>"
            content += "<div class='checkName grid_6'><h2>HTTP</h2></div>"
            content += "<div class='grid_15'>"
            content += "<table class='checkTable' width='98%'>"
            content += "<thead><tr><th><b>status</b><th><b>title</b></th></th><th><b>when</b></th><th><b>url</b></th></tr></thead>"
            content += "<tbody>"
            for item in listOfChecks.fetchall():
                lastCheck = item['last_check']
                serviceID = item['services_id']
                myStatus = item['status']
                content += '<tr>'
                if(myStatus == 'bad'):
                    db = MySQLdb.connect (host = config.DB_HOST,
                                                       user = config.DB_USER,
                                                       passwd = config.DB_PASSWD,
                                                       db = config.DB_NAME)
                    c=db.cursor()
                    query = """SELECT status FROM status where check_date = "%s" AND service_id = "%s" """ % (lastCheck, serviceID)
                    c.execute(query)
                    curStatus = c.fetchall()
                if(myStatus == None):
                    content += '<td><img src=\"static/images/None.png\" width=15 height=15 /></td>'
                elif(myStatus == 'good'):
                    content += '<td><img src=\"static/images/good.png\" width=15 height=15 /></td>'
                else:
                    color='gray'
                    go = """ %s """ % (curStatus)
                    rex = re.compile(r'\W')
                    returnStatus = rex.sub(' ', go)
                    content += """<td><img onMouseover="ddrivetip(' Error: %s','%s', 300)" onMouseout="hideddrivetip()" src="static/images/%s.png" width=
15 height=15 /></td>""" % (returnStatus,color,str(item['status']))

                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + str(item['last_check']) + '</td>'
                content += '<td>' + str(item['http_url']) + '</td>'
                content += '</tr>'
            content += "</tbody>"
            content += "</table></div></div>"

        ## icmp
        listOfChecks = self.serviceList.icmp()
        if (listOfChecks.rowcount > 0):
            content += "<div class='checkModule grid_15'>"
            content += "<div class='checkName grid_6'><h2>ICMP</h2></div>"
            content += "<div class='grid_15'>"
            content += "<table class='checkTable' width='98%'>"
            content += "<thead><tr><th><b>status</b><th><b>title</b></th></th><th><b>when</b></th><th><b>ip address</b></th></tr></thead>"
            content += "<tbody>"
            for item in listOfChecks.fetchall():
                lastCheck = item['last_check']
                serviceID = item['services_id']
                myStatus = item['status']
                content += '<tr>'
                if(myStatus == 'bad'):
                    db = MySQLdb.connect (host = config.DB_HOST,
                                                       user = config.DB_USER,
                                                       passwd = config.DB_PASSWD,
                                                       db = config.DB_NAME)
                    c=db.cursor()
                    query = """SELECT status FROM status where check_date = "%s" AND service_id = "%s" """ % (lastCheck, serviceID)
                    c.execute(query)
                    curStatus = None
                    curStatus = c.fetchall()
                if(myStatus == None):
                    content += '<td><img src=\"static/images/None.png\" width=15 height=15 /></td>'
                elif(myStatus == 'good'):
                    content += '<td><img src=\"static/images/good.png\" width=15 height=15 /></td>'
                else:
                    color='gray'
                    go = """ %s """ % (curStatus)
                    rex = re.compile(r'\W')
                    returnStatus = rex.sub(' ', go)
                    content += """<td><img onMouseover="ddrivetip(' Error: %s','%s', 300)" onMouseout="hideddrivetip()" src="static/images/%s.png" width=15 height=15 /></td>""" % (returnStatus,color,str(item['status']))
                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + str(item['last_check']) + '</td>'
                content += '<td>' + str(item['icmp_ip']) + '</td>'
                content += '</tr>'

            content += "</tbody>"
            content += "</table></div></div>"

        ## pop3
        listOfChecks = self.serviceList.pop3()
        if (listOfChecks.rowcount > 0):
            content += "<div class='checkModule grid_15'>"
            content += "<div class='checkName grid_6'><h2>POP3</h2></div>"
            content += "<div class='grid_15'>"
            content += "<table class='checkTable' width='98%'>"
            content += "<thead><tr><th><b>status</b><th><b>title</b></th></th><th><b>when</b></th><th><b>ip address</b></th></tr></thead>"
            content += "<tbody>"
            for item in listOfChecks.fetchall():
                lastCheck = item['last_check']
                serviceID = item['services_id']
                myStatus = item['status']
                content += '<tr>'
                if(myStatus == 'bad'):
                    db = MySQLdb.connect (host = config.DB_HOST,
                                                       user = config.DB_USER,
                                                       passwd = config.DB_PASSWD,
                                                       db = config.DB_NAME)
                    c=db.cursor()
                    query = """SELECT status FROM status where check_date = "%s" AND service_id = "%s" """ % (lastCheck, serviceID)
                    c.execute(query)
                    curStatus = c.fetchall()
                if(myStatus == None):
                    content += '<td><img src=\"static/images/None.png\" width=15 height=15 /></td>'
                elif(myStatus == 'good'):
                    content += '<td><img src=\"static/images/good.png\" width=15 height=15 /></td>'
                else:
                    color='gray'
                    go = """ %s """ % (curStatus)
                    rex = re.compile(r'\W')
                    returnStatus = rex.sub(' ', go)
                    content += """<td><img onMouseover="ddrivetip(' Error: %s','%s', 300)" onMouseout="hideddrivetip()" src="static/images/%s.png" width=
15 height=15 /></td>""" % (returnStatus,color,str(item['status']))

                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + str(item['last_check']) + '</td>'
                content += '<td>' + str(item['pop3_ip']) + '</td>'
                content += '</tr>'
            content += "</tbody>"
            content += "</table></div></div>"

        ## smtp
        listOfChecks = self.serviceList.smtp()
        if (listOfChecks.rowcount > 0):
            content += "<div class='checkModule grid_15'>"
            content += "<div class='checkName grid_6'><h2>SMTP</h2></div>"
            content += "<div class='grid_15'>"
            content += "<table class='checkTable' width='98%'>"
            content += "<thead><tr><th><b>status</b><th><b>title</b></th></th><th><b>when</b></th><th><b>ip address</b></th></tr></thead>"
            content += "<tbody>"
            for item in listOfChecks.fetchall():
                lastCheck = item['last_check']
                serviceID = item['services_id']
                myStatus = item['status']
                content += '<tr>'
                if(myStatus == 'bad'):
                    db = MySQLdb.connect (host = config.DB_HOST,
                                                       user = config.DB_USER,
                                                       passwd = config.DB_PASSWD,
                                                       db = config.DB_NAME)
                    c=db.cursor()
                    query = """SELECT status FROM status where check_date = "%s" AND service_id = "%s" """ % (lastCheck, serviceID)
                    c.execute(query)
                    curStatus = c.fetchall()
                if(myStatus == None):
                    content += '<td><img src=\"static/images/None.png\" width=15 height=15 /></td>'
                elif(myStatus == 'good'):
                    content += '<td><img src=\"static/images/good.png\" width=15 height=15 /></td>'
                else:
                    color='gray'
                    go = """ %s """ % (curStatus)
                    rex = re.compile(r'\W')
                    returnStatus = rex.sub(' ', go)
                    content += """<td><img onMouseover="ddrivetip(' Error: %s','%s', 300)" onMouseout="hideddrivetip()" src="static/images/%s.png" width=
15 height=15 /></td>""" % (returnStatus,color,str(item['status']))

                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + str(item['last_check']) + '</td>'
                content += '<td>' + str(item['smtp_ip']) + '</td>'
                content += '</tr>'
            content += "</tbody>"
            content += "</table></div></div>"

        ## tcp
        listOfChecks = self.serviceList.tcp()
        if (listOfChecks.rowcount > 0):
            content += "<div class='checkModule grid_15'>"
            content += "<div class='checkName grid_6'><h2>TCP Port</h2></div>"
            content += "<div class='grid_15'>"
            content += "<table class='checkTable' width='98%'>"
            content += "<thead><tr><th><b>status</b><th><b>title</b></th></th><th><b>when</b></th><th><b>ip</b></th><th><b>port</b></th></tr></thead>"
            content += "<tbody>"
            for item in listOfChecks.fetchall():
                lastCheck = item['last_check']
                serviceID = item['services_id']
                myStatus = item['status']
                content += '<tr>'
                if(myStatus == 'bad'):
                    db = MySQLdb.connect (host = config.DB_HOST,
                                                       user = config.DB_USER,
                                                       passwd = config.DB_PASSWD,
                                                       db = config.DB_NAME)
                    c=db.cursor()
                    query = """SELECT status FROM status where check_date = "%s" AND service_id = "%s" """ % (lastCheck, serviceID)
                    c.execute(query)
                    curStatus = None
                    curStatus = c.fetchall()
                if(myStatus == None):
                    content += '<td><img src=\"static/images/None.png\" width=15 height=15 /></td>'
                elif(myStatus == 'good'):
                    content += '<td><img src=\"static/images/good.png\" width=15 height=15 /></td>'
                else:
                    color='gray'
                    go = """ %s """ % (curStatus)
                    rex = re.compile(r'\W')
                    returnStatus = rex.sub(' ', go)
                    content += """<td><img onMouseover="ddrivetip(' Error: %s','%s', 300)" onMouseout="hideddrivetip()" src="static/images/%s.png" width=15 height=15 /></td>""" % (returnStatus,color,str(item['status']))
                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + str(item['last_check']) + '</td>'
                content += '<td>' + str(item['tcp_ip']) + '</td>'
                content += '<td>' + str(item['tcp_port']) + '</td>'
                content += '</tr>'
            content += "</tbody>"
            content += "</table></div></div>"

        ## ipsec
        listOfChecks = self.serviceList.ipsec()
        if (listOfChecks.rowcount > 0):
            content += "<div class='checkModule grid_15'>"
            content += "<div class='checkName grid_6'><h2>IPsec</h2></div>"
            content += "<div class='grid_15'>"
            content += "<table class='checkTable' width='98%'>"
            content += "<thead><tr><th><b>status</b><th><b>target</b><th><b>title</b></th></th><th><b>when</b></th><th><b>gateway</b></th><th><b>group</b></th><th><b>user</b></th><th><b>target</b></th></tr></thead>"
            content += "<tbody>"
            for item in listOfChecks.fetchall():
                content += '<tr>'
                content += '<td><img src=\"static/images/' + str(item['status']) + '.png\" width=15 height=15 /></td>'
                content += '<td><img src=\"static/images/' + str(item['status_secondary']) + '.png\"  width=15 height=15 /></td>'
                content += '<td>' + item['title'] + '</td>'
                content += '<td>' + str(item['last_check']) + '</td>'
                content += '<td>' + str(item['ipsec_gateway']) + '</td>'
                content += '<td>' + str(item['ipsec_group']) + '</td>'
                content += '<td>' + str(item['ipsec_user']) + '</td>'
                content += '<td>' + str(item['ipsec_target_host_ip']) + '</td>'
                content += '</tr>'
            content += "</tbody>"
            content += "</table></div></div>"
        content += """
		<script type="text/javascript">            		    
		$("#run").click(function()
		{
		$("#launcherbutton").append('<br><img src="static/images/ajax-loader.gif" />');
		$.get("/run/", function(data) {
		$('.result').html(data);
		location.reload();
		});
		});
		</script>
		</div>
		</div>
		</body>
		</html>
		"""        
        return content

class RunChecks:
    
    def GET(self):
        #TODO: this needs to be called securely!
        subprocess.call('/usr/bin/python /export/web/people/jynx.net/public_html/simple-server-status/launch_checks.py', shell=True)
        
class AddCheck:

    def GET(self):
        content = """
        <html>
		<head>
		<title>Simple Server Status</title>
		<link rel="stylesheet" href="../static/styles/reset.css" type="text/css" media="screen" />
		<link rel="stylesheet" href="../static/styles/960.css" type="text/css" media="screen" />
		<link href='http://fonts.googleapis.com/css?family=Droid+Sans:bold' rel='stylesheet' type='text/css'>
		<link rel="stylesheet" href="../static/styles/norm.css" type="text/css" media="screen" />
		</head>
		<body>
        <script type="text/javascript">
        function confirmDel(delUrl) {
          if (confirm("Are you sure you want to delete this service?")) {         
              document.location = delUrl;
             }
          }
        </script>
		<div id="container" class="container_16">
		<div id="mainContent" class="grid_16">
		<div id="header" class="grid_8">
		<h1>Simple Server Status</h1>
		</div>
		<br /><br /><br />
		<div class='checkModule grid_15'>
		<div class='checkName grid_6'><h2>Add New Check</h2></div>
		<div class='grid_15'>
		<form name="finalCheck" action="/do" method="post">
		<div id="typeCheck">
		<select name="simple_option" id="checkType">
		<option value=""></option>
		<option value="http">Http</option>
		<option value="tcp">TCP</option>
		<option value="mysql">MySQL</option>
		<option value="icmp">ICMP</option>
		<option value="smtp">SMTP</option>
		<option value="pop3">POP3</option>
		<option value="ipsec">IPSec</option>
		</select>
		</div>
		<div id="addCheckTable">
		<table id="http" class='checkTable' width='98%'>
		<thead>
		<tr>
		<th><b>title</b></th>
		<th><b>url</b></th>
		</tr>
		</thead>
		<tbody>
		<tr>
		<td><input name="http_title" type="text" size="35" /></td>
		<td><input name="http_url" type="text" size="35" /></td>
		</tr>
		</tbody>
		</table>
        <table id="icmp" class='checkTable' width='98%'>
        <thead>
        <tr>
        <th><b>title</b></th>
        <th><b>ip address</b></th>
        </tr>
        </thead>
        <tbody>
        <tr>
        <td><input name="icmp_title" type="text" size="35" /></td>
        <td><input name="icmp_ip" type="text" size="35" /></td>
        </tr>
        </tbody>
        </table>
        <table id="smtp" class='checkTable' width='98%'>
        <thead>
        <tr>
        <th><b>title</b></th>
        <th><b>ip address</b></th>
        </tr>
        </thead>
        <tbody>
        <tr>
        <td><input name="smtp_title" type="text" size="35" /></td>
        <td><input name="smtp_ip" type="text" size="35" /></td>
        </tr>
        </tbody>
        </table>
        <table id="pop3" class='checkTable' width='98%'>
        <thead>
        <tr>
        <th><b>title</b></th>
        <th><b>ip address</b></th>
        </tr>
        </thead>
        <tbody>
        <tr>
        <td><input name="pop3_title" type="text" size="35" /></td>
        <td><input name="pop3_ip" type="text" size="35" /></td>
        </tr>
        </tbody>
        </table>
		<table id="tcp" class='checkTable' width='98%'>
		<thead>
		<tr>
		<th><b>title</b></th>
		<th><b>IP Address</b></th>
		<th><b>Port</b></th>
		</tr>
		</thead>
		<tbody>
		<tr>
		<td><input name="tcp_title" type="text" size="35" /></td>
		<td><input name="tcp_ip" type="text" size="35" /></td>
		<td><input name="tcp_port" type="text" size="15" /></td>
		</tr>
		</tbody>
		</table>
		<table id="mysql" class='checkTable' width='98%'>
		<thead>
		<tr>
		<th><b>title</b></th>
		<th><b>mysql hostname</b></th>
		<th><b>mysql username</b></th>
		</tr>
		</thead>
		<tbody>
		<tr>
		<td><input name="mysql_title" type="text" size="35" /></td>
		<td><input name="mysql_hostname" type="text" size="35" /></td>
		<td><input name="mysql_user" type="text" size="35" /></td>
		</tr>
		<tr>
		<th><b>mysql password (AES 256 Enabled)</b></th>
		<th><b>mysql port</b></th>
		<th><b>mysql database name</b></th>
		<th>&nbsp;</th>
		</tr>
		<tr>
		<td><input name="mysql_pass" type="text" size="35" /></td>
		<td><input name="mysql_port" type="text" size="35" /></td>
		<td><input name="mysql_db" type="text" size="35" /></td>
		<td>&nbsp;</td>
		</tr>
		</tbody>
		</table>
		<table id="ipsec" class='checkTable' width='98%'>
		<thead>
		<tr>
		<th><b>title</b></th>
		<th><b>ipsec gateway</b></th>
		<th><b>ipsec group</b></th>
		</tr>
		</thead>
		<tbody>
		<tr>
		<td><input name="ipsec_title" type="text" size="35" /></td>
		<td><input name="ipsec_gateway" type="text" size="35" /></td>
		<td><input name="ipsec_group" type="text" size="35" /></td>
		</tr>
		<tr>
		<th><b>ipsec username</b></th>
		<th><b>ipsec password (AES 256 Enabled)</b></th>
		<th><b>ipsec secret</b></th>
		</tr>
		<tr>
		<td><input name="ipsec_user" type="text" size="35" /></td>
		<td><input name="ipsec_pass" type="text" size="35" /></td>
		<td><input name="ipsec_secret" type="text" size="35" /></td>
		</tr>
        <!-- end table -->
		</div>
		<input type="submit" value="Add New Check" />
		</form>
		</body>
		<script src="http://code.jquery.com/jquery-1.4.3.min.js" type="text/javascript"></script>
		<script type="text/javascript">
		$(document).ready(function()
		{
		$(".checkTable").hide();
		$("#checkType").change(function()
		{
		$(".checkTable").hide();
		$("#"+$("#checkType").val()).show();
		});
		});
		</script></html>"""
        ## come here
        self.serviceLists = Service.Listing()
        listServices = self.serviceLists.showall()
        if(listServices.rowcount > 0):
            content += """<BR><BR><div id='display'><table border="0" cellpadding="2" width="80%" class=''>
                          <thread>
                          <th width="15%" align="left" valign="top">Service ID:</th>
                          <th width="40%" align="left" valign="top">Service</th>
                          <th width="40%" align="left" valign="top">Title</th>
                          <th width="15%" align="left" valign="top"></th>
                          </thread>"""
            for item in listServices.fetchall():
                content += """<tbody><tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td><a href="javascript:confirmDel('/delete/?id=%s')">delete</a></td>
                </tr></tbody>""" % (item['id'],item['kind'],item['title'],item['id'])

            content += """</table><BR>"""
        content += """<form name="return_home" action="/">
        <input type="submit" value="Return Home" />
        </form>
        </tbody>
                </table>
                </div>
                </div>
                </div>
                </div>
                """
	return content
