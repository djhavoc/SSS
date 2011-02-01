import Database

class Listing:
        
    def __init__(self):
        self.db = Database.Connection()    
    
    def mysql(self):
        self.db.cursor.execute("""SELECT 
                                        services.id,
                                        services.title,
                                        services.db_name,
                                        services.db_host,
                                        services.db_user,
                                        results.services_id,
                                        results.last_check,
                                        results.status
                                    FROM services, results
                                    WHERE services.id = results.services_id
                                    AND services.kind = 'mysql'
                                """)
        return self.db.cursor

    def showall(self):
        self.db.cursor.execute("SELECT * from services")
        return self.db.cursor

    def delid(self,service_id):
        self.db.cursor.execute("""DELETE FROM services,results,status USING services
                                    LEFT JOIN results ON results.services_id = '%s'
                                    LEFT JOIN status ON status.service_id = '%s'
                                    WHERE services.id = '%s'""" % (service_id,service_id,service_id))
        return self.db.cursor

    def mysqlstatus(self,log_date, service_id):
        self.db.cursor.execute("""SELECT
                                        status
                                    FROM status where check_date = '%s'
                                    AND service_id = '%s'""" & (log_date, service_id))
        return self.db.cursor

    def icmp(self):
        self.db.cursor.execute("""SELECT 
                                        services.id,
                                        services.title,
                                        services.icmp_ip,
                                        results.services_id,
                                        results.last_check,
                                        results.status
                                    FROM services, results
                                    WHERE services.id = results.services_id
                                    AND services.kind = 'icmp'
                                """)
        return self.db.cursor

    def pop3(self):
        self.db.cursor.execute("""SELECT 
                                        services.id,
                                        services.title,
                                        services.pop3_ip,
                                        results.services_id,
                                        results.last_check,
                                        results.status
                                    FROM services, results
                                    WHERE services.id = results.services_id
                                    AND services.kind = 'pop3'
                                """)
        return self.db.cursor

    def smtp(self):
        self.db.cursor.execute("""SELECT 
                                        services.id,
                                        services.title,
                                        services.smtp_ip,
                                        results.services_id,
                                        results.last_check,
                                        results.status
                                    FROM services, results
                                    WHERE services.id = results.services_id
                                    AND services.kind = 'smtp'
                                """)
        return self.db.cursor

        
    def http(self):
        self.db.cursor.execute("""SELECT 
                                        services.id,
                                        services.title,
                                        services.http_url,
                                        results.services_id,
                                        results.last_check,
                                        results.status
                                    FROM services, results
                                    WHERE services.id = results.services_id
                                    AND services.kind = 'http'
                                """)
        return self.db.cursor
        
    def tcp(self):
        self.db.cursor.execute("""SELECT 
                                        services.id,
                                        services.title,
                                        services.tcp_ip,
                                        services.tcp_port,
                                        results.services_id,
                                        results.last_check,
                                        results.status
                                    FROM services, results
                                    WHERE services.id = results.services_id
                                    AND services.kind = 'tcp'
                                """)
        return self.db.cursor

    def ipsec(self):
        self.db.cursor.execute("""SELECT 
                                        services.id,
                                        services.title,
                                        services.ipsec_gateway,
                                        services.ipsec_group,
                                        services.ipsec_user,
                                        services.ipsec_target_host_ip,
                                        results.services_id,
                                        results.last_check,
                                        results.status,
                                        results.status_secondary
                                    FROM services, results
                                    WHERE services.id = results.services_id
                                    AND services.kind = 'ipsec'
                                """)
        return self.db.cursor
