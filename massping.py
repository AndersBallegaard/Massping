#!/usr/bin/python3
"""
A tool for simutaniously checking avalibility of multiple hosts inspired by BIGPHATTOBY/fineping
"""
import sys
import subprocess
import time
import threading
import signal
import platform



def help_menu():
    '''
    Prints the help page for -h or no argument
    '''
    print("massping.py\n \
        --csv -c <file>    CSV like file. Format: [name],[address] newline [name],[address]....\n\
    \
    ")


#dict of host objects with human name, ip/DNS, and status
#the host's human friendly name is used as the key each item have a dict with 2 keys host and status
HOSTS = {}

#variable used to indicate if pings should run or be stopped
SHOULD_PING_RUN = True

def ping(host_tuple):
    '''
    ping function that takes in a tupel or list where obj 0 is the name and obj 1 is the address
    no output is returned
    '''
    hostname = host_tuple[0]
    address = host_tuple[1]

    global HOSTS

    #create a clear key and dict in hosts
    HOSTS[hostname] = {}

    #set hostname in dict
    HOSTS[hostname]["host"] = address

    #set inital status
    #status 0 = working, 1 = error, 2 = initalizing
    HOSTS[hostname]["status"] = 2

    #detect os and set command in cmd var
    cmd = ["ping", "-c", "1", "-w", "1", address]
    if platform.system() == 'Windows':
        cmd = ["ping", "-n", "1", address]


    #start loop that pings and update status every 2 secounds
    while SHOULD_PING_RUN:
        failed = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        if not failed:
            HOSTS[hostname]["status"] = 0
        else:
            HOSTS[hostname]["status"] = 1
        time.sleep(2)




def pad(string, deciered_len):
    '''
    Pads a string with spaces until it's the desired lenght
    '''
    spaces = "                                  "
    space_len = deciered_len - len(str(string))
    return string + spaces[0:space_len]



def update():
    '''
    Update the screen with the latest information from all the threads
    '''
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

    for host, value in HOSTS.items():
        #set name field length
        if len(str(host)) > f_name:
            f_name = len(str(host))

        #set address field lenght
        if len(str(value["host"])) > f_address:
            f_address = len(str(value["host"]))

    #set status lenght
    for status, value in status_decoder.items():
        if len(str(status)) > f_status:
            f_status = len(str(status))


    #stop when ctrl+x is pressed or another event trigers varible
    while SHOULD_PING_RUN:
        #clear screen
        subprocess.call('clear')

        print("Massping")
        print(f"{pad(b_name,f_name)} \
             {pad(b_address,f_address)}   \
              {pad(b_status,f_status)}")
        for host_, value in HOSTS.items():
            host = value["host"]
            status = status_decoder[value["status"]]
            print(f"{pad(host_,f_name)} \
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
        csv_file = open(sys.argv[2])
        csv_file.read()
        csv_file.close()
    except (FileNotFoundError, IndexError):
        print("Please add a valid file")
        exit(1)


    #open file
    host_file = open(sys.argv[2])

    #make list of hosts
    hosts_text_list = host_file.read().split('\n')

    #start all the threads for pinging
    for host_ in hosts_text_list:
        host = host_.split(',')[0]
        address = host_.split(',')[1]
        host_thread = threading.Thread(target=ping, args=[(host, address)])
        host_thread.start()

    update()



def argument_handeler():
    """
    Handels arguments and calls the right functions
    """
    arguemts = {
        "-h" : help_menu,
        "--help" : help_menu,
        "-c" : csv_like_list,
        "--csv" : csv_like_list
    }

    return_function = None
    try:
        return_function = arguemts[sys.argv[1]]
    except (KeyError, IndexError):
        return_function = help_menu
    return return_function()


#handle ctrl+c
def sigint_handler(*args):
    '''
    Handels exits by gently telling all threads to stop
    '''
    global SHOULD_PING_RUN
    SHOULD_PING_RUN = False
    print("\nstopping\n")

signal.signal(signal.SIGINT, sigint_handler)



if __name__ == "__main__":
    argument_handeler()
