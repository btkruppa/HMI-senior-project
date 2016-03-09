import socket
import struct
import time

slaveID = 11
'''this is the function for reading coil(s), send it the start coil and end coil
    there is a limit where you can only do within 254 coils at a time currently'''
def readCoil(start, end):
    print("\nReading coil...")
    if end < start:
        end = start
    coilId1 = start
    coilId2 = 0
    length1 = end - start + 1
    length2 = 0
    while coilId1 > 255:
        coilId1 = coilId1 - 256
        coilId2 = coilId2 + 1

    while length1 > 255:
        length1 = length1 - 256
        length2 = length2 + 1

    req = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, int(unitId), 0x01, int(coilId2), int(coilId1), int(length2), int(length1))
    sock.send(req)
    '''a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12 = struct.unpack('12B',req)
    print("TX: ", hex(a1), hex(a2), hex(a3), hex(a4), hex(a5), hex(a6), hex(a7), hex(a8), hex(a9), hex(a10), hex(a11), hex(a12))'''
    rec = sock.recv(BUFFER_SIZE)
    numBytes = len(rec)
    print("numBytes ", numBytes)

    '''this is to sort the information sent back into the bits of the coils read'''
    a = []
    b = []
    for x in range(9, numBytes):
        a = struct.unpack('B', rec[x])
        b.append('{0:08b}'.format(int(a[0])))

    print(b)
    '''this is to output the state of each coil read '''
    for x in range(0, len(b)):
        for i in range(0, 8):
            if start+i+8*x <= end:
                print("Coil #{} is a {}".format(start+i+8*x, b[x][7-i]))

    '''print("RX: ",  b, len(b))'''


'''this is the function to set multiple registers '''
def presetMultipleRegisters(start, end):
    print("\nWriting registers...")
    if end < start:
        end = start
    coilId1 = start
    coilId2 = 0
    length1 = end - start + 1
    length2 = 0

    while coilId1 > 255:
        coilId1 = coilId1 - 256
        coilId2 = coilId2 + 1

    while length1 > 255:
        length1 = length1 - 256
        length2 = length2 + 1

    req = struct.pack('17B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x0B, int(unitId), 0x10, int(coilId2), int(coilId1), int(length2), int(length1), 0x04, 0x07, 0x03, 0x15,0x0A)
    sock.send(req)
    '''a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12 = struct.unpack('12B',req)
    print("TX: ", hex(a1), hex(a2), hex(a3), hex(a4), hex(a5), hex(a6), hex(a7), hex(a8), hex(a9), hex(a10), hex(a11), hex(a12))'''
    rec = sock.recv(BUFFER_SIZE)
    numBytes = len(rec)
    print("numBytes ", numBytes)

    '''this is to sort the information sent back into the bits of the coils read'''
    a = []
    b = []
    for x in range(0, numBytes):
        a = struct.unpack('B', rec[x])
        b.append(a)

    print(b)
    '''this is to output the state of each coil read
    for x in range(0, len(b)):
        for i in range(0, 8):
            if start+i+8*x <= end:
                print("Coil #{} is a {}".format(start+i+8*x, b[x][7-i]))

    print("RX: ",  b, len(b))'''

'''this is a function for reading registers '''
def readHoldingRegisters(start, end):
    print("\nReading registers...")
    if end < start:
        end = start
    coilId1 = start
    coilId2 = 0
    length1 = end - start + 1
    length2 = 0
    while coilId1 > 255:
        coilId1 = coilId1 - 256
        coilId2 = coilId2 + 1

    while length1 > 255:
        length1 = length1 - 256
        length2 = length2 + 1

    req = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, int(unitId), 0x03, int(coilId2), int(coilId1), int(length2), int(length1))
    sock.send(req)
    '''a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12 = struct.unpack('12B',req)
    print("TX: ", hex(a1), hex(a2), hex(a3), hex(a4), hex(a5), hex(a6), hex(a7), hex(a8), hex(a9), hex(a10), hex(a11), hex(a12))'''
    rec = sock.recv(BUFFER_SIZE)
    numBytes = len(rec)
    print("numBytes ", numBytes)

    '''this is to sort the information sent back into the bits of the coils read'''
    a = []
    b = []
    for x in range(0, numBytes):
        a = struct.unpack('B', rec[x])
        b.append(a)

    print(b)
    '''this is to output the state of each coil read '''
    for x in range(0, len(b)):
        '''print("Coil #{} is a {}".format(start+i+8*x, b[x][7-i]))'''

    '''print("RX: ",  b, len(b))'''

#create the TCP/IP socket
TCP_IP = '192.168.0.211'
TCP_PORT = 502
BUFFER_SIZE = 41
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "connecting"
sock.connect((TCP_IP, TCP_PORT))
print "success"


'''self note: this is how you comment in python'''
try:
    # Switch Plug On then Off
    unitId = 1 # Plug Socket
    functionCode = 5 # Write coil

    print("\nSwitching Plug ON...")
    coilId = 14
    req = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, int(unitId), int(functionCode), 0x00, int(coilId), 0xff, 0x00)
    sock.send(req)
    print("TX: (%s)" %req)
    rec = sock.recv(BUFFER_SIZE)
    print("RX: (%s)" %rec)
    '''time.sleep(2)'''

    print("\nSwitching Plug OFF...")
    coilId = 15
    req = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, int(unitId), int(functionCode), 0x00, int(coilId), 0xff, 0x00)
    sock.send(req)
    a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12 = struct.unpack('12B',req)
    print("TX: ", a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12)
    rec = sock.recv(BUFFER_SIZE)

    a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12 = struct.unpack('12B',rec)
    print("RX: ", a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12)

    readCoil(start = 0, end = 0 )
    presetMultipleRegisters(start = 2, end = 3)
    readHoldingRegisters(start = 2, end = 3)

finally:
    print('\nCLOSING SOCKET')
    sock.close()
