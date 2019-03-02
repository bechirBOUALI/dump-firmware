import telnetlib
import re
import struct
import time
import sys 
HOST = "127.0.0.1"
PORT = "4444"

s = telnetlib.Telnet(HOST , PORT)
s.set_debuglevel(0)
s.read_until(">")

#s.write("reset halt\n") # first command to openocd
#s.read_until(">")

f = open("firmware_chunk_3.bin","a+")
init_value = 0
    
s.write("reset halt\n") # first command to openocd
s.read_until(">")
offset = int(sys.argv[1])
address = 0
test = 0

while address < 16384:
    
    print "\n"
    print " ===Begining=== \n"

    time.sleep(1)

    s.write("reset halt\n") # first command to openocd
    #time.sleep(0.5)
    p = s.read_until(">")
    print "first reset",p
    
    time.sleep(1)

    for address in xrange(offset,int("0x4000",16),4):

        print "[+]" + hex(address)
        s.write("reset halt\n") # first command to openocd
        p2=s.read_until(">")
        print "p2",p2
        
        time.sleep(1)
        
        s.write("reg pc 0x6DC\n")
        time.sleep(0.5)
        show1 = s.read_until(">")
        print "show1 ",show1        
        show1_value = re.findall(r': 0x[0-9afA-F]+', show1)
        print show1_value
        if show1_value != [': 0x000006DC']:
            offset = address
            test = 1
            print "test 1"
            s.write("reset halt\n") # first command to openocd
            #time.sleep(0.5)
            s.read_until(">")
            break



        time.sleep(0.5)

        s.write("reg r3 " + hex(address) + "\n")
        time.sleep(0.5)
        show2 = s.read_until(">")
        print "show2 ",show2
        
        show2_value = re.findall(r': 0x[0-9afA-F]+', show2)
        print show2_value
        print len(show2_value)

        if len(show2_value) != 1:
            offset = address
            test = 1
            print "test 1"
            s.write("reset halt\n") # first command to openocd
            #time.sleep(0.5)
            s.read_until(">")
            break
        
        

        s.write("step\n")
        s.read_until(">")
        time.sleep(0.5)


        print "========= show content of pc  "
        s.write("reg pc\n")
        show = s.read_until(">")
        print "show ",show 
        #time.sleep(0.5)
        pc_value = re.findall(r'0x[0-9afA-F]+', show)
        #print "pc-->" + pc_value[0]
        print "[+] pc = ",pc_value 

        if pc_value != ['0x000006DE']:
            offset = address
            test = 1
            print "test 1"
            s.write("reset halt\n") # first command to openocd
            #time.sleep(0.5)
            s.read_until(">")
            break

        test = 0
        print "test 0"
        s.write("reg r3\n")
        data = re.findall(r'0x[0-9afA-F]+', s.read_until(">"))
        print "pc = " ,pc_value ," || "+ "r3 = " ,data
        if data:

            f.write(struct.pack("I",int(data[0],16)))

f.close()
