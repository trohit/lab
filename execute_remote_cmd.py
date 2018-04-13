#!/usr/bin/python
import sys
import paramiko

#execute_remote_cmd('ls', '1.2.3.4', 'root', 'password')
def execute_remote_cmd (cmd, ip, username, password):
    port=22
    print "*************************"
    print "Executing Remote CMD: ", cmd    
    print "*************************"
    
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print "", ip,port,username,password
    ssh.connect(ip,port,username,password,allow_agent=False)
    stdin,stdout,stderr=ssh.exec_command(cmd)
    outlines=stdout.readlines()
    resp=''.join(outlines)

    print(resp)
    return stdout.channel.recv_exit_status()

# main
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: " + sys.argv[0] + " <ip> <user> <passwd> <cmd>")
        sys.exit(1)
    else:
        ip = sys.argv[1]
        user = sys.argv[2]
        passwd = sys.argv[3]
        cmd = sys.argv[4]
        print("executing: " + sys.argv[0] + " " + ip + " " + user + " " + passwd + " " + cmd)
        #sys.exit(1)
    execute_remote_cmd(cmd, ip, user, passwd)
