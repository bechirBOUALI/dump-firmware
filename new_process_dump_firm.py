import telnetlib
import re
import struct
import time
import pykush
import subprocess

HOST = "127.0.0.1"
PORT = "4444"

confUsbPort = pykush.YKUSH()

offset = 0
address = 0
while address < 4096:

    print "[+] Waiting for USB to be UP" 
    confUsbPort.set_port_state(1, pykush.YKUSH_PORT_STATE_UP)
    time.sleep(3)

    p = subprocess.Popen('openocd -f /usr/share/openocd/scripts/interface/stlink-v2-1.cfg -f /usr/share/openocd/scripts/target/nrf51.cfg', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    time.sleep(1)

    print "[+] telnet connected"
    s = telnetlib.Telnet(HOST , PORT)

    s.set_debuglevel(0)
    s.read_until(">")

    print "[+] first reset halt"
    s.write("reset halt\n") # first command to openocd
    reset = s.read_until(">")
    print "reset",reset    
    time.sleep(2)

    f = open("firm.bin","a+")
    #print "reset halt"
    print "====the file opened====" 

    time.sleep(0.1)



    for address in xrange(offset,int("0x1000",16),4):

        print "[+] reset halt"
        s.write("reset halt\n") # first command to openocd
        see = s.read_until(">")

        print "see",see 
        print "[+]" + hex(address)

        time.sleep(3)

        s.write("reg pc 0x6DC\n")
        s.read_until(">")


        s.write("reg r3 " + hex(address) + "\n")
        s.read_until(">")


        s.write("step\n")
        s.read_until(">")

        s.write("reg pc\n")
        pc_value = re.findall(r'0x[0-9afA-F]+', s.read_until(">"))
        #print "pc-->" + pc_value[0]
        print pc_value 

        if pc_value != ['0x000006DE']:
            offset = address
            print "offset = ",offset
            subprocess.Popen('kill -9 p.pid', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            time.sleep(0.5)
            confUsbPort.set_port_state(1, pykush.YKUSH_PORT_STATE_DOWN)
            time.sleep(1)
            s.close()
            break

        s.write("reg r3\n")
        data = re.findall(r'0x[0-9afA-F]+', s.read_until(">"))
        print "pc = " ,pc_value ," || "+ "r3 = " ,data
        if data:

            f.write(struct.pack("I",int(data[0],16)))

    if address == 4090:
        print "max reached"
        f.close()
        break
#last address 4092 0xffc
