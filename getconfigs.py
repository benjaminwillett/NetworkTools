__author__ = 'benwillett'

#File name: telnetautomation.py
#!/usr/bin/python
#Script starts here

import getpass
import sys
import telnetlib
import time
import smtplib
import re
import openpyxl
import string


print "loading global variables!!"
time.sleep(1)
ftpserver = "172.30.2.84"
ftpuser = "##########"
ftppass = "##########"
user = "#########"
pwd1 = "#########"
#pwd2 = "privilege_exec_mode_password"
startup = "startup-config"
running = "running-config"
fullStartUnc = "full unc path for access to files"
fullRunUnc = "full unc path for access to files"
startUnc = "current directory for your FTP server"
runUnc = "current directory for your FTP server"
mailHost = "outlook.office365.com"
fromEmail = "###@###"
toEmail = "###@###"
emailPass = "#####"
devices = "devices.xlsx"

print "********************************************************"
print "********************************************************"
print "**        Network backup and config sync tool         **"
print "**  ************************************************  **"
print "**  ************************************************  **"
print "**  ************************************************  **"
print "**          Created by benw@techcamp.com.au           **"
print "********************************************************"
print "********************************************************"

time.sleep(5)

print "Connecting to Mail host " + mailHost + ", please wait!!"

try:
    smtpObj = smtplib.SMTP(mailHost, 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(fromEmail, emailPass)
    answer = ()
    print "Connected to " + mailHost + " Successfully"
except:
    print "Unable to connect to " + mailHost

try:
    print "Importing devices from Spreadsheet"
    time.sleep(1)
    wb = openpyxl.load_workbook(fullStartUnc + devices)
    sheet = wb.get_sheet_by_name("Sheet 1")
except:
    print "Could not import spreadsheet"
    time.sleep(1)
    smtpObj.quit()
    sys.exit('operation completed')


#Create a list of router IP address, and router hostname

rowCount = 0
columnA = sheet.columns[0]
columnB = sheet.columns[1]


#Use for loop to telnet into each routers and execute commands

def getconfig():
    cmd1 = "en"
    cmd2 = "copy " + startup + " ftp://" + ftpuser + ":" + ftppass + "@" + ftpserver + startUnc + hostNames + ".txt"
    cmd3 = "copy " + running + " ftp://" + ftpuser + ":" + ftppass + "@" + ftpserver + runUnc + hostNames + ".txt"

    try:
        telnet = telnetlib.Telnet(ipAddresses, 10)
        #telnet.set_debuglevel(5)
        time.sleep(1)
        telnet.write(user.encode('ascii') + b"\n")
        time.sleep(1)
        telnet.write(pwd1.encode('ascii') + b"\n")
        time.sleep(1)
        telnet.write(cmd1.encode('ascii') + b"\n")
        time.sleep(1)
        telnet.write(cmd2.encode('ascii') + b"\n")
        time.sleep(2)
        telnet.write(b"\n")
        time.sleep(1)
        telnet.write(b"\n")
        time.sleep(1)
        telnet.write(cmd3.encode('ascii') + b"\n")
        time.sleep(2)
        telnet.write(b"\n")
        time.sleep(1)
        telnet.write(b"\n")
        time.sleep(1)
        telnet.close()
        time.sleep(1)
        print "Successfully transfered config for " + hostNames
    except:
        print "Unable to telnet into " + hostNames
        pass

for i in columnA:
    ipAddresses = columnA[rowCount].value
    #hostNames = columnA[rowCount].value
    hostNames = columnB[rowCount].value
    if ipAddresses == None:
        rowCount = 0
        print "Empy Cell in Spreadsheet"
        print "Finished collecting configurations"
        break
    else:
        print "Getting config for " + ipAddresses + " " + hostNames
        getconfig()
        rowCount = rowCount + 1

answer = raw_input("Do you want to compare configs for differences?")
if answer in list(["yes", "y", "Yes", "Y"]):
    print "comparing configs now"
else:
    print "ending program"
    time.sleep(2)
    sys.exit("operation completed")



for i in columnA:
    chopStart = re.compile(r'certificate self-signed.*?.cer', re.DOTALL)
    chop = re.compile(r'certificate self-signed.*?quit', re.DOTALL)
    #hostNames = columnA[rowCount].value
    hostNames = columnB[rowCount].value
    if hostNames == None:
        rowCount = 0
        print "Finished Analyzing"
        break
    else:
        print "Analysing " + hostNames + " configurations"
        time.sleep(1)
        try:
            startup = open("%s%s.txt" %(fullStartUnc, hostNames)).readlines()
            readStart = open("%s%s.txt" %(fullStartUnc, hostNames), 'w').writelines(startup[5:])
            startup = open("%s%s.txt" %(fullStartUnc, hostNames), 'r')
            dataStart = startup.read()
            data_chopped = chopStart.sub('', dataStart)
            readStart = open("%s%s.txt" %(fullStartUnc, hostNames), 'w').writelines(data_chopped)
            readStart = open("%s%s.txt" %(fullStartUnc, hostNames)).readlines()

            running = open("%s%s.txt" %(fullRunUnc, hostNames)).readlines()
            readRun = open("%s%s.txt" %(fullRunUnc, hostNames), 'w').writelines(running[5:])
            running = open("%s%s.txt" %(fullRunUnc, hostNames), 'r')
            dataRun = running.read()
            data_chopped = chop.sub('', dataRun)
            readRun = open("%s%s.txt" %(fullRunUnc, hostNames), 'w').writelines(data_chopped)
            readRun = open("%s%s.txt" %(fullRunUnc, hostNames)).readlines()

            if readRun == readStart:
                print("" + hostNames + " OK")

            else:
                print("" + hostNames + " has a difference")
                smtpObj.sendmail(fromEmail, toEmail, 'Subject:' + hostNames + ' config' +
                                 " out" + ' of sync.\n')

        except:
            print "No Files for " + hostNames
            pass


        rowCount = rowCount + 1


try:
    smtpObj.quit()
except:
    sys.exit("operation completed")
sys.exit("operation completed")
#script ends here