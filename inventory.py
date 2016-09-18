__author__ = 'benwillett'

import telnetlib
import paramiko
import time
import sys
import smtplib
import re
import openpyxl
import string
from colours import colour
import os

print ("loading global variables!!")
time.sleep(1)

user = "XXXXX"
pwd1 = "XXXXX"
# pwd2 = "privilege_exec_mode_password"
spreadsheetPath = "/Users/benwillett/Desktop/ITWork/DET/configs/"
spreadsheet = "devices.xlsx"
mailHost = "outlook.office365.com"
fromEmail = "###@###"
toEmail = "###@###"
emailPass = "#####"
ios_cli_length = " terminal length 0"
timeout_for_reply = 1  # 1 second time variable
line_break = "\r\n"  # need to be sent after a command to get it executed like sending "enter" key stroke
inventory = {}
configs = []
noConfigs = []


print ("********************************************************")
print ("********************************************************")
print ("**             Network Inventory tool                 **")
print ("**  ************************************************  **")
print ("**          Created by benw@techcamp.com.au           **")
print ("********************************************************")
print ("********************************************************")
print ("**  This tool collects information about your network **")
print ("**  It uses the ips in your spreadsheet to collect    **")
print ("**  device configuration information for an inventory **")
print ("********************************************************")
print ("********************************************************")

# FIXME uncomment
# time.sleep(5)
# print ("Connecting to Mail host " + mailHost + ", please wait!!")
#
# try:
#     smtpObj = smtplib.SMTP(mailHost, 587)
#     smtpObj.ehlo()
#     smtpObj.starttls()
#     smtpObj.login(fromEmail, emailPass)
#     answer = ()
#     print ("Connected to " + mailHost + " Successfully")
# except:
#     print ("Unable to connect to " + mailHost)

try:
    message = "importing devices from spreadsheet"
    os.system('say "{0}"'.format(message + " " + spreadsheet))
    print (message)
    time.sleep(1)
    wb = openpyxl.load_workbook(spreadsheetPath + spreadsheet)
    sheet = wb.get_sheet_by_name("Sheet 1")
except:
    message = "could not import devices from spreadsheet"
    os.system('say "{0}"'.format(message + " " + spreadsheet))
    time.sleep(1)
    smtpObj.quit()
    sys.exit('operation completed')


# Create a list of router IP addresses

rowCount = 0
columnA = sheet.columns[0]


# TODO learn the items for this syntax
# Use for loop to telnet into each routers and execute commands

def getconfig():
    cmd1 = "en"
    cmd2 = "show clock \r\n"

    try:
        inventory[ipAddresses]['name'] = "empty"
        telnet = telnetlib.Telnet(ipAddresses)
        # telnet.set_debuglevel(5)

        telnet.write("\n")
        login_prompt = "Username: "
        response = telnet.read_until(login_prompt, 5)
        telnet.write("%s\n" % user)
        password_prompt = "Password:"
        response = telnet.read_until(password_prompt, 3)
        telnet.write("%s\n" % pwd1)

        time.sleep(1)
        telnet.write(cmd1.encode('ascii') + b"\n")
        time.sleep(2)

        time.sleep(timeout_for_reply)
        telnet.write(" terminal length 0" + "\r\n")
        device_name = telnet.read_until(" terminal length 0").split()[-len(" terminal length 0".split(' '))]
        device_name = device_name[:-1]
        inventory[ipAddresses]['name'] = device_name
        #         telnet.write(cmd2)
        #         time.sleep(1)
        #         clock = telnet.read_until("UTC")
        #         clock = clock[len(device_name):]
        #         #dict["name"] = device_name
        #         #dict["ip"] = ipAddresses
        #         #dict["time"] = clock
        #         #list.append(dict)
        #         print list
        #
        #
        #
        time.sleep(5)

        telnet.write(b"\n")
        time.sleep(1)
        telnet.write(b"\n")
        time.sleep(1)

        telnet.close()
        time.sleep(1)
        print ("Successfully got inventory for " + device_name + " (" + ipAddresses + ")")
    except:
        print ("Unable to telnet into " + ipAddresses)



def sshconnect(ip):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=pwd1)
    # inventory[ipAddresses]['name'] = "empty"
    remote_conn = client.invoke_shell()
    print("Interactive SSH session established")
     # Strip the initial router prompt
    output = remote_conn.recv(1000)
    # See what we have
    print output
    # Turn off paging
    #disable_paging(remote_conn)
    # Now let's try to send the router a command
    remote_conn.send("\n")
    # Wait for the command to complete
    time.sleep(2)
    output = remote_conn.recv(1100)
    print output


# TODO create a list of dictionary objects
for i in columnA:
    ipAddresses = columnA[rowCount].value
    if ipAddresses != None:
        inventory.setdefault(ipAddresses, {})
        message = "collecting configurations"
        os.system('say "{0}"'.format(message))
        print ("Getting inventory for " + ipAddresses)
        getconfig()
        rowCount += 1
    else:
        rowCount = 0
        print ("Empy Cell in Spreadsheet")
        print ("Finished collecting configurations")
        break


def collectioncheck():
    for key, name in inventory.iteritems():
        try:
            nameValue = name['name']
        except:
            pass
        if nameValue != "empty":
            configs.append(nameValue)

        else:
            noConfigs.append(key)


collectioncheck()
print ("\nCollected configs for:")
for i in configs:
    print colour.green(i)
    os.system('say "{0}"'.format(i + " was successful"))

print ("\nCould not collect configs for:")
for i in noConfigs:
    print colour.red(i)
    os.system('say "{0}"'.format(i + " Failed"))
    print("Trying " + i + " using SSH instead")
    try:
        sshconnect(i)
    except:
        print("Could not connect to " + i + " using SSH")
print ("\nCould not collect configs for:")
for i in noConfigs:
    print colour.red(i)
    os.system('espeak -ven+f3 "{0}"'.format(i + " Failed"))

try:
    smtpObj.quit()
except:
    time.sleep(2)
    sys.exit("operation completed")
time.sleep(2)
sys.exit("operation completed")
# script ends here
