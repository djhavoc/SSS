## launch all checks

import sys
import os
import commands
sys.path.append('Classes/')
import Check
 
if __name__ == "__main__":
    
    ## check if vpnc is running
    psOutput = commands.getoutput('ps -A')
    if 'vpnc' in psOutput:
        print 'vpnc is already running'
        sys.exit()

    ## check ps lock
    lock_file_name = 'checksrunning.lock'
    if os.path.isfile(lock_file_name):
        print 'already running, exiting'
        sys.exit()
    else:
        open(lock_file_name, 'w')


    launcher = Check.Checks()

    launcher.servicesToInspect('mysql')
    launcher.run('mysql')

    launcher.servicesToInspect('http')
    launcher.run('http')

    launcher.servicesToInspect('tcp')
    launcher.run('tcp')

    launcher.servicesToInspect('smtp')
    launcher.run('smtp')

    launcher.servicesToInspect('pop3')
    launcher.run('pop3')

    launcher.servicesToInspect('icmp')
    launcher.run('icmp')
    
    launcher.servicesToInspect('ipsec')
    launcher.run('ipsec')    

    launcher.closeDatabase()
    
    ## remove lock file
    os.remove(lock_file_name)
