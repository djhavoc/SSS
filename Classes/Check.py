import sys
import os
import pexpect
import copy
import MySQLdb
import ping
import socket
import urllib2
import Database
import config
import time
import smtplib

class Checks:
    
    def __init__(self):
        self.db = Database.Connection()
        
    def closeDatabase(self):
        self.db.cursor.close()
        self.db.connection.commit()
        self.db.connection.close()
    
    ## build list of services for an inspection
    def servicesToInspect(self, kind):
        if (kind == 'mysql'):
            self.db.cursor.execute("""SELECT id, 
                                                title, 
                                                db_name, 
                                                db_host,
                                                db_user, 
                                                db_port,
                                                db_pass
                                        FROM services 
                                        WHERE services.kind = 'mysql'""")

        elif (kind == 'http'):
            ## http
            self.db.cursor.execute("""SELECT id, http_url
                                                        FROM services 
                                                        WHERE services.kind = 'http'""")
        elif (kind == 'icmp'):
            ## icmp
            self.db.cursor.execute("""SELECT id, icmp_ip
                                                        FROM services
                                                        WHERE services.kind = 'icmp'""")
        elif (kind == 'smtp'):
            ## smtp
            self.db.cursor.execute("""SELECT id, smtp_ip
                                                        FROM services
                                                        WHERE services.kind = 'smtp'""")
        elif (kind == 'pop3'):
            ## pop3 
            self.db.cursor.execute("""SELECT id, pop3_ip
                                                        FROM services
                                                        WHERE services.kind = 'pop3'""")
        
        elif (kind == 'tcp'):
            self.db.cursor.execute("""SELECT id, tcp_ip, tcp_port
                                                        FROM services 
                                                        WHERE services.kind = 'tcp'""")

        if (kind == 'ipsec'):
            self.db.cursor.execute("""SELECT id, 
                                                title, 
                                                ipsec_gateway, 
                                                ipsec_group, 
                                                AES_DECRYPT(ipsec_secret,'%s') as ipsec_secret,
                                                ipsec_user,
                                                AES_DECRYPT(ipsec_pass,'%s') as ipsec_pass,
                                                ipsec_target_host_ip                                                
                                        FROM services
                                        WHERE services.kind = 'ipsec'""" %(config.DB_CRYPTOKEY,config.DB_CRYPTOKEY))

    def recordResult(self, status, serviceID, myerror=None):
        self.db.cursor.execute("""UPDATE results SET last_check = NOW(), status = '%s' WHERE services_id = %s """ % (status, serviceID))
        lastrowid = self.db.cursor.lastrowid
        if(myerror != None):
            query = """INSERT into status (service_id,status,check_date) values ("%s","%s",NOW())
                    """ % (serviceID,myerror)
            self.db.cursor.execute(query)
        return lastrowid

    def recordResultSecondary(self, status, serviceID):
        self.db.cursor.execute("""UPDATE results SET last_check = NOW(), status_secondary = '%s' WHERE services_id = %s """ % (status, serviceID))
        return self.db.cursor.lastrowid


    ## perform inspections
    def run(self, kind):
        if (kind == 'mysql'):
            if (self.db.cursor.rowcount > 0):
                for item in self.db.cursor.fetchall():
                    self.mysql(item['id'], item['db_host'], item['db_name'], item['db_user'], item['db_pass'], item['db_port'])

        elif (kind == 'http'):
            if (self.db.cursor.rowcount > 0):
                for item in self.db.cursor.fetchall():
                    self.http(item['id'], item['http_url'])        
        
        elif (kind == 'tcp'):
            if (self.db.cursor.rowcount > 0):
                for item in self.db.cursor.fetchall():
                    self.tcp(item['id'], item['tcp_ip'], item['tcp_port'])        

        elif (kind == 'smtp'):
            if (self.db.cursor.rowcount > 0):
                for item in self.db.cursor.fetchall():
                    self.smtp(item['id'], item['smtp_ip'], 25)

        elif (kind == 'pop3'):
            if (self.db.cursor.rowcount > 0):
                for item in self.db.cursor.fetchall():
                    self.pop3(item['id'], item['pop3_ip'], 110)

        elif (kind == 'icmp'):
            if (self.db.cursor.rowcount > 0):
                for item in self.db.cursor.fetchall():
                    self.icmp_c(item['id'], item['icmp_ip'])

        elif (kind == 'ipsec'):
            if (self.db.cursor.rowcount > 0):
                for item in self.db.cursor.fetchall():
                    self.ipsec(item['id'], item['ipsec_gateway'], item['ipsec_group'], item['ipsec_secret'], item['ipsec_user'], item['ipsec_pass'], item['ipsec_target_host_ip'])        

        return True

    def ipsec(self, serviceID, ipsec_gateway, ipsec_group, ipsec_secret, ipsec_user, ipsec_pass, ipsec_target_host_ip):
        '''check ipsec tunnel'''
        print 'ipsec'
        socket.setdefaulttimeout(2)
        ## establish vpn tunnel
        try:
            vpncShell = pexpect.spawn('/sbin/vpnc')
            vpncShell.logfile = sys.stdout
            vpncShell.expect('Enter IPSec gateway address:')
            vpncShell.sendline(ipsec_gateway)        
            vpncShell.expect('Enter IPSec ID for %s:' %(ipsec_gateway))
            vpncShell.sendline(ipsec_group)
            vpncShell.expect('Enter IPSec secret for %s@%s:' % (ipsec_group, ipsec_gateway))
            vpncShell.sendline(ipsec_secret)
            vpncShell.expect('Enter username for %s:' % (ipsec_gateway))
            vpncShell.sendline(ipsec_user)
            vpncShell.expect('Enter password for %s@%s:' % (ipsec_user, ipsec_gateway))
            vpncShell.sendline(ipsec_pass)
            vpncShell.expect('VPNC started in background')
            self.recordResult('good', serviceID)
        except:
            self.recordResult('bad', serviceID)
        time.sleep(1)
        pexpect.run('/sbin/route add -host %s dev tun0' % (ipsec_target_host_ip))
        
        print pexpect.run('/bin/netstat -r')
        try:
            delay = ping.doOne(ipsec_target_host_ip, timeout=2)
            #print 'DELAY: %s' % (delay)
            if delay >= 0.0:
                self.recordResultSecondary('good', serviceID)
            else:
                self.recordResultSecondary('bad', serviceID)
        except socket.error, e:
            #print "Ping Error:", e
            self.recordResultSecondary('bad', serviceID)
        vpncDisconnectShell = pexpect.spawn('/sbin/vpnc-disconnect')
                    
    ## check a mysql connection
    def mysql(self, serviceID, host, name, user, passwd, port):
        print 'mysql'
        try:
            dbConn = MySQLdb.connect (host = host,
                                    port = port,
                                    user = user,
                                    passwd = passwd,
                                    db = name,
                                    connect_timeout = 2)
            status = 'good'
            error_msg = None
            dbConn.close()
        except MySQLdb.Error, e:
            error_msg = e.args[1]
            status = 'bad'

        self.recordResult(status, serviceID, error_msg)
                    
    ## check a web service
    def http(self, serviceID, url):
        print 'http'
        socket.setdefaulttimeout(2)
        try:
            result = urllib2.urlopen(url)
            status = 'good'
            error_msg = None
        except IOError, e:
            status = 'bad'
            error_msg = e.args[0]
        self.recordResult(status, serviceID, error_msg)

    ## check icmp packets
    def icmp_c(self, serviceID, ip):
        print 'icmp'
        socket.setdefaulttimeout(2)
        delay = ping.doOne(ip, timeout=3)
        if delay >= 0.0:
            self.recordResult('good', serviceID)
        else:
            error_msg = "No Response from Target"
            self.recordResult('bad', serviceID, error_msg)
        
    ## check a tcp port
    def tcp(self, serviceID, ip, port):
        print 'tcp'
        socket.setdefaulttimeout(2)
        s = None
        for res in socket.getaddrinfo(ip, int(port), socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
                status = 'good'
                error_msg = None
            except socket.error, msg:
                status = 'bad'
                error_msg = msg.args[1]
                s = None
                continue
            try:
                s.connect(sa)
                status = 'good'
                error_msg = None
            except socket.error, msg:
                status = 'bad'
                s.close()
                error_msg = msg.args[1]
                s = None
                continue
            break
        self.recordResult(status, serviceID, error_msg)

    def pop3(self, serviceID, ip, port):
        print 'pop3'
        socket.setdefaulttimeout(2)
        s = None
        for res in socket.getaddrinfo(ip, int(port), socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
                status = 'good'
                error_msg = None
            except socket.error, msg:
                status = 'bad'
                error_msg = msg.args[1]
                s = None
                continue
            try:
                s.connect(sa)
                status = 'good'
                error_msg = None
            except socket.error, msg:
                status = 'bad'
                error_msg = msg.args[1]
                s.close()
                s = None
                continue
            break
        self.recordResult(status, serviceID, error_msg)

    def smtp(self, serviceID, ip, port):
        print 'smtp'
        hostname = socket.gethostname()
        socket.setdefaulttimeout(2)
        s = None
        for res in socket.getaddrinfo(ip, int(port), socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
                status = 'good'
                error_msg = None
            except socket.error, msg:
                status = 'bad'
                error_msg = msg.args[1]
                s = None
                continue
            try:
                s.connect(sa)
                status = 'good'
                error_msg = None
            except socket.error, msg:
                status = 'bad'
                error_msg = msg.args[1]
                s.close()
                s = None
                continue
            break
        self.recordResult(status, serviceID, error_msg)

