import telnetlib
import re
import struct

HOST = "127.0.0.1"
PORT = "4444"

s = telnetlib.Telnet(HOST , PORT)
s.set_debuglevel(0)
s.read_until(">")

def overwrite_registers():

 for i in xrange(13):

    s.write("reg r" + str(i) + " " +  hex(0x04) + "\n")
    s.read_until(">")

def print_registers():

 for i in xrange(13):

    s.write("reg r" + str(i) + "\n")
    data = re.findall(r'0x[0-9afA-F]+', s.read_until(">"))
    if (data[0] != "0x00000004") and (data[0] != "0xFFFFFFFF"): 
        print "-----------reg r" + str(i) + " = " + data[0]

s.write("reset halt\n")
s.read_until(">")
for x in xrange(0,100,2):
 
    print "====step==== " + str(x)
    
    pc = int("0x6d0",16)
    pc += x
    print " pc ",hex(pc)
    s.write("reg pc " + hex(pc) +"\n")
    s.read_until(">")

    overwrite_registers()

    s.write("step\n")
    s.read_until(">")

    s.write("reg pc\n")
    data = re.findall(r'0x[0-9afA-F]+', s.read_until(">"))
    print "pc = " + data[0]

    print_registers()
