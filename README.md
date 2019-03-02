# dump-firmware
Bypass security features to dump firmware of remote control copier

### Taregt 
nRF51822-QFAC is an ultra-low power 2.4 GHz .It is built
around the 32-bit ARM® CortexTM-M0 CPU with 256 KB flash and 32 KB
RAM

### For Debugging 
For debugging I used the STLINK-V2 as adapter debugger and openOCD as software debugger

### Description about script functionalities

1. debug_firm.py
This script used to find a load instruction used by CPU

2. dump_firm.py
This script used to load data(firmware) from main memory to a file

3. new_process_dump_firm.py
This script used to automate the hole process of dumping when the device crash using a ykush card. 
