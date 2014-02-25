#!/usr/bin/python
import subprocess

# Important note: this doesn't do anything about the actual Internet Sharing.  That
# will still need to be enabled independently with correct "attwifi" SSID.

# The goal here is to rotate the MAC addresses between 4E:53:50:4F:4F:40 and 4E:53:50:4F:4F:4F.
# So what we're going to do is check the current value of the last chunk, make sure it's 
# between 64-79 decimal, and then increase it by one.  If it's not over 79, commit it. If it
# is over 79, roll back to 64.

MAC_base = '4E:53:50:4F:4F:'
WiFi = 'en0' # assumes you're on an MBA/rMBP; otherwise this will be 'en1'

# First, find out the current MAC address using ifconfig en0 ether
p1 = ['/sbin/ifconfig',WiFi,'ether']
p2 = ['/usr/bin/tail','-n','1']
p3 = ['/usr/bin/cut','-f','6','-d:']

result1 = subprocess.Popen(p1, stdout=subprocess.PIPE)
result2 = subprocess.Popen(p2, stdin=result1.stdout, stdout=subprocess.PIPE)
result1.stdout.close()
result3 = subprocess.Popen(p3, stdin=result2.stdout, stdout=subprocess.PIPE)
result2.stdout.close()
output = result3.communicate()[0].rstrip()

FinalCurrentGroup = int(output, 16)

if (FinalCurrentGroup < 64) or (FinalCurrentGroup >= 79):
	FinalGroup = hex(64).lstrip("0x")
	#If it's under 0x40 or at 0x4F or above, then roll set it back to 0x40.
else:
	FinalGroup = hex(FinalCurrentGroup + 1).lstrip("0x")
	#Otherwise, increment by one.

MAC = MAC_base + FinalGroup

# Now we commit this MAC address
p1 = ['/sbin/ifconfig',WiFi,'ether',MAC]
result1 = subprocess.Popen(p1, stdout=subprocess.PIPE)
output = result1.communicate()

# Flip the WiFi power
p1 = ['/usr/sbin/networksetup','-setairportpower',WiFi,'off']
p2 = ['/usr/sbin/networksetup','-setairportpower',WiFi,'on']
result1 = subprocess.Popen(p1, stdout=subprocess.PIPE)
output = result1.communicate()
result2 = subprocess.Popen(p2, stdout=subprocess.PIPE)
output = result2.communicate()
