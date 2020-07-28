from bs4 import BeautifulSoup as bs
from datetime import datetime
import time
import pathlib
import os
content = []
# Read the XML file

with open("/mysql-data/mysql/audit.log", "r") as file:
    # Read each line in the file, readlines() returns a list of lines
    content = file.readlines()
    # Combine the lines in the list into a string
    content = "".join(content)
    bs_content = bs(content, "lxml")
lop=len(bs_content.find_all('audit_record'))
now_utc = datetime.utcnow()
system=datetime.strftime(now_utc,"%Y-%m-%d %H:%M")
f=time.strftime('%Y-%m-%d %H:%M EST', time.localtime())
fle=time.strftime('%Y-%m-%d_%H_%M', time.localtime())
myoutfile='/mysql-work/session_trace/audit_details_%s.txt' % fle
file = pathlib.Path(myoutfile)
#outF = open(myoutfile, "w")
if file.exists ():
   outF = open(myoutfile, "a+")
   outF.write('\n Event already capture and send to user')
   outF.close()
   exit()
else:
    outF = open(myoutfile, "w")
    for i in range(1,lop,1):
      d=bs_content.find_all('audit_record')[i]
      #print(d.command_class.string)
      #local = tz.gettz()
      r=d.timestamp.string
      utc=datetime.strptime(r,"%Y-%m-%dT%H:%M:%S UTC")
      audit_time=datetime.strftime(utc,"%Y-%m-%d %H:%M")
      if (audit_time==system):
         if (d.sqltext is None):
            print ("\n" + str(d.user.string) + "," + str(d.host.string) + "," + f, end="",file=outF)
         else:
            print ("\n" + str(d.user.string) + "," + str(d.host.string) + "," + str(d.sqltext.string)+ "," + f, end="",file=outF)
    outF.close()

path='/mysql-work/session_trace'
for root, dirs, files in os.walk(path):
   for f in files:
     fullname = os.path.join(root, f)
     if os.path.getsize(fullname) == 0:
        os.remove(fullname)
