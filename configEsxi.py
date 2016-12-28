#Ready for production. just remove clutter from commands. 
#This script is for configuring networking on esxi hosts.
import pexpect
import getpass
import sys
import collections

esxiPrompt='~ #' #This prompt is to be expected after each command execution. 
#This dictionary is very important. This contains key value pairs. Key starts with a number and dot directly after number. This should be unique. 
#Key contains human readable description while value contains actual commands to be run on esxi host. 
commands = collections.OrderedDict()
commands.update({'1. List all network cards':'esxcli network nic list'})
commands.update({'2. list down vswitches on esxi':'esxcli network vswitch standard list'})
commands.update({'3. Get policy of active/standby vmnics on vswitch0':'esxcli network vswitch standard policy failover get --vswitch-name vSwitch0'})
commands.update({'4. Get policy of active/standby vmnics on vswitch1':'esxcli network vswitch standard policy failover get --vswitch-name vSwitch1'})
#Need to work on following command. 
commands.update({'5. Set 4 nics as active nics':'esxcli network vswitch standard policy failover set --active-uplinks vmnic0,vmnic1,vmnic2,vmnic3 --vswitch-name  vSwitch0'})
commands.update({'6. List all of the port groups currently on the system.':'esxcli network vswitch standard portgroup list'})
commands.update({'7. Configure vlan on vswitch0':'esxcli network vswitch standard portgroup '})
commands.update({'q or quit':'To quit the script'})
#
#This function returns two value tuple. matcheCount denotes number of matches in whole list. if this is 0 means no command found for selection. If 1 means correct command exists. if >1 means somehow multiple commands match the selection criteria. 
def getCommand(choice):
 choice=choice+"."
 print choice
 matchedValue=""
 matchedCount=0;
 for key, value in commands.iteritems():
  if(key.startswith(choice)):
   matchedValue=value
   matchedCount=matchedCount+1
 return (matchedCount,matchedValue)
def getInput():
 inputSelection=raw_input("Select:")
 return inputSelection
def showMenu():
 
 for key, value in commands.iteritems():
  print "%s : %s" %(key,value)

class loginDetails:
 username=""
 password=""
 def set_UserName(self,username):
  self.username=username 
 def set_password():
  self.password=password 

#Getting username,password and esxi host IP
esxihost=raw_input("Enter ESXi Host IP:")
username=raw_input("Enter user name: root or equally prvileged:")
password=getpass.getpass()
loginObj=loginDetails()
loginObj.set_UserName(username)

#If esxi host prompts for accepting RSA figner prints
ssh_newkey = 'Are you sure you want to continue connecting'
p = pexpect.spawn ('ssh root@%s' %esxihost)
fout = open('mylog.txt','a')
p.logfile = fout
i=p.expect([ssh_newkey,'assword:',pexpect.EOF])
if i==0:
    p.sendline('yes')
    i=p.expect([ssh_newkey,'assword:',pexpect.EOF])
if i==1:
    p.sendline(password)
    p.expect(esxiPrompt)

var =1
while var ==1:
 p.logfile = sys.stdout
 showMenu()
 p.logfile = fout

 selection= getInput();
 if selection.lower() in ['q','qu','qui','quit','','exit']:
  print "Exiting....."
  p.kill(0)
  exit(0)
 [matchCount,commandReturn] = getCommand(selection)

 if matchCount==1:
#This if block is for configuring vlan on vswitch. 
  if commandReturn == "esxcli network vswitch standard portgroup ":
   vswitchName=raw_input("which vswitch? vswitch0 or 1. input number only:")
   vswitchName='--vswitch-name vSwitch'+vswitchName
   portGroup = raw_input("Type vlan name:")
   portGroup = '--portgroup-name '+portGroup
   vlanId = raw_input("Type vlan number:")
   vlanId = '--vlan-id '+vlanId
   commandReturnplus = commandReturn + 'set ' + portGroup +" "+vlanId
   commandReturn=commandReturn+ 'add '+vswitchName+" "+portGroup
   print commandReturn
   print commandReturnplus
   p.sendline(commandReturn)
   p.expect (esxiPrompt)
   p.sendline(commandReturnplus)
   p.expect (esxiPrompt)
  else:
   p.sendline(commandReturn)
   p.expect (esxiPrompt)
 print p.before

fout.close()
p.kill(0)

