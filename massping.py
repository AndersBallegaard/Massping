#!/usr/bin/python3
"""
A tool for simutaniously checking avalibility of multiple hosts inspired by BIGPHATTOBY/fineping 
"""
import sys
import subprocess
import time
import threading
import signal


def help():
    '''
    Prints the help page for -h or no argument
    '''
    print("massping.py\n \
        --csv -c <file>    CSV like file. Format: [name],[address] newline [name],[address]....\n\
    \
    ")


#dict of host objects with human name, ip/DNS, and status
#the host's human friendly name is used as the key each item have a dict with 2 keys host and status
hosts = {}

#variable used to indicate if pings should run or be stopped
should_pings_run = True

def ping(host_tuple):
    '''
    ping function that takes in a tupel or list where obj 0 is the name and obj 1 is the address
    no output is returned 
    '''
    hostname = host_tuple[0]
    address = host_tuple[1]

    global hosts

    #create a clear key and dict in hosts
    hosts[hostname] = {}
    
    #set hostname in dict
    hosts[hostname]["host"] = address
    
    #set inital status
    #status 0 = working, 1 = error, 2 = initalizing
    hosts[hostname]["status"] = 2

    #start loop that pings and update status every 2 secounds
    while should_pings_run:
        failed = subprocess.call(["ping","-c","1","-w","1",address],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        if not failed:
            hosts[hostname]["status"] = 0
        else:
            hosts[hostname]["status"] = 1
        time.sleep(2)




def pad(string,l):
    '''
    Pads a string with spaces until it's the desired lenght
    '''
    spaces = "                                  "
    sl = l - len(str(string))
    return(string + spaces[0:sl])



def update():
    #status decoder
    status_decoder = {
        0 : "\033[1;32mConnected\033[1;m",
        1 : "\033[1;31mError\033[1;m",
        2 : "\033[1;36mInit\033[1;m"
    }

    #banner names
    b_name = "Name"
    b_address = "Address"
    b_status = "Status"

    #find lengths diffrent fields need to be
    f_name = len(b_name)
    f_address = len(b_address)
    f_status = len(b_status)

    for h , v in hosts.items():
        #set name field length
        if len(str(h)) > f_name:
            f_name = len(str(h))
        
        #set address field lenght
        if len(str(v["host"])) > f_address:
            f_address = len(str(v["host"]))
        
    #set status lenght
    for s, i in status_decoder.items():
        if len(str(s)) > f_status:
            f_status = len(str(s))


    #stop when ctrl+x is pressed or another event trigers varible
    while should_pings_run:
        #clear screen
        subprocess.call('clear')

        print("Massping")
        print(f"{pad(b_name,f_name)} \
             {pad(b_address,f_address)}   \
              {pad(b_status,f_status)}")
        for h, v in hosts.items():
            host = v["host"]
            status = status_decoder[v["status"]]
            print(f"{pad(h,f_name)} \
             {pad(host,f_address)}   \
              {pad(status,f_status)}")
        print("press ctrl+c to stop")
        time.sleep(2)


def csv_like_list():
    '''
    Parse a csv like file with [name],[address] formatting and start threads 
    '''
    #check if file argument exists and that file can be opened
    try:
        f = open(sys.argv[2])
        f.read()
        f.close()
    except:
        print("Please add a valid file")


    #open file
    f = open(sys.argv[2])

    #make list of hosts
    hosts_text_list = f.read().split('\n')

    #start all the threads for pinging
    for h in hosts_text_list:
        host = h.split(',')[0]
        address = h.split(',')[1]
        t = threading.Thread(target=ping,args=[(host,address)])
        t.start()
    
    update()



def argument_handeler():
    """
    Handels arguments and calls the right functions
    """
    arguemts = {
        "-h" : help,
        "--help" : help,
        "-c" : csv_like_list,
        "--csv" : csv_like_list
    }
    
    ro = None
    try:
        ro = arguemts[sys.argv[1]]
    except:
        ro = help
    return(ro())


#handle ctrl+c
def sigint_handler(signum, frame):
    global should_pings_run
    should_pings_run = False
    print("\nstopping\n")
 
signal.signal(signal.SIGINT, sigint_handler)



if __name__ == "__main__":
    argument_handeler()