import tornado.web
import logging
import requests
import json
import re
import socket
import struct
import time

from dateutil.relativedelta import relativedelta
from alchemy.setup import *
from alchemy.base_handlers import BaseHandler

logger = logging.getLogger("pyserver")

slaveID = 11
unitId = 1
TCP_IP = '192.168.0.211'
TCP_PORT = 502
BUFFER_SIZE = 41
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "connecting"
sock.connect((TCP_IP, TCP_PORT))
print "success"

def presetMultipleRegisters(start, val):
    print("\nWriting registers...")
    '''if end < start:
        end = start'''
    end = start
    coilId1 = start
    coilId2 = 0
    length1 = end - start + 1
    length2 = 0
    val2 = 0

    while coilId1 > 255:
        coilId1 = coilId1 - 256
        coilId2 = coilId2 + 1

    while length1 > 255:
        length1 = length1 - 256
        length2 = length2 + 1

    while val > 255:
        val2 = val2 +1
        val = val-256

    req = struct.pack('15B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x09, int(unitId), 0x10, int(coilId2), int(coilId1), int(length2), int(length1), 0x02, val2, val)
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
    return

def ReadCoil(coil):
    '''Check to make sure the end coild comes after the start coil'''
    start = coil
    end = coil
    coilId1 = start
    coilId2 = 0
    length1 = end - start + 1
    length2 = 0
    '''If the coil is located after 255 it takes 2 bytes'''
    while coilId1 > 255:
        coilId1 = coilId1 - 256
        coilId2 = coilId2 + 1
    '''If it is requesting more that 255 coils at a time it takes 2 bytes'''
    while length1 > 255:
        length1 = length1 - 256
        length2 = length2 + 1

    req = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, int(unitId), 0x01, int(coilId2), int(coilId1), int(length2), int(length1))
    sock.send(req)
    '''a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12 = struct.unpack('12B',req)
    print("TX: ", hex(a1), hex(a2), hex(a3), hex(a4), hex(a5), hex(a6), hex(a7), hex(a8), hex(a9), hex(a10), hex(a11), hex(a12))'''
    rec = sock.recv(BUFFER_SIZE)
    numBytes = len(rec)

    '''this is to sort the information sent back into the bits of the coils read'''
    a = []
    b = []
    for x in range(9, numBytes):
        a = struct.unpack('B', rec[x])
        b.append('{0:08b}'.format(int(a[0])))

    '''print(b)'''
    '''this is to output the state of each coil read '''
    for x in range(0, len(b)):
        for i in range(0, 8):
            if start+i+8*x <= end:
                '''print("Coil #{} is a {}".format(start+i+8*x, b[x][7-i]))'''
                return b[x][7-i]


    '''print("RX: ",  b, len(b))'''

def readRegister(register):
    start = register
    end = start
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

    '''this is to sort the information sent back into the bits of the coils read'''
    a = []
    b = []
    for x in range(9, numBytes):
        a = struct.unpack('B', rec[x])
        b.append(a)
    b = 256*b[0][0]+b[1][0]
    '''this is to output the state of each coil read '''
    '''for x in range(0, len(b)):'''
    '''print("register #{} is a {}".format(start+i+8*x, b[x][7-i]))'''

    '''print("RX: ",  b, len(b))'''
    return b

def readContact(contact):
    '''Check to make sure the end coild comes after the start coil'''
    start = contact
    end = contact
    coilId1 = start
    coilId2 = 0
    length1 = end - start + 1
    length2 = 0
    '''If the coil is located after 255 it takes 2 bytes'''
    while coilId1 > 255:
        coilId1 = coilId1 - 256
        coilId2 = coilId2 + 1
    '''If it is requesting more that 255 coils at a time it takes 2 bytes'''
    while length1 > 255:
        length1 = length1 - 256
        length2 = length2 + 1

    req = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, int(unitId), 0x02, int(coilId2), int(coilId1), int(length2), int(length1))
    sock.send(req)
    '''a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12 = struct.unpack('12B',req)
    print("TX: ", hex(a1), hex(a2), hex(a3), hex(a4), hex(a5), hex(a6), hex(a7), hex(a8), hex(a9), hex(a10), hex(a11), hex(a12))'''
    rec = sock.recv(BUFFER_SIZE)
    numBytes = len(rec)

    '''this is to sort the information sent back into the bits of the coils read'''
    a = []
    b = []
    for x in range(9, numBytes):
        a = struct.unpack('B', rec[x])
        b.append('{0:08b}'.format(int(a[0])))

    '''print(b)'''
    '''this is to output the state of each coil read '''
    for x in range(0, len(b)):
        for i in range(0, 8):
            if start+i+8*x <= end:
                '''print("Coil #{} is a {}".format(start+i+8*x, b[x][7-i]))'''
                return b[x][7-i]


    '''print("RX: ",  b, len(b))'''

class ReadCoilHandler(BaseHandler):
    def get(self, coil, id):
        coilRead = ReadCoil(int(coil))

        self.write(json.dumps({'coil':coilRead, 'id':id}))

class ReadContactHandler(BaseHandler):
    def get(self, contact, id):
        contactRead = readContact(int(contact))
        '''presetMultipleRegisters(25,550)'''

        self.write(json.dumps({'contact':contactRead, 'id':id}))

class ReadRegisterHandler(BaseHandler):
    def get(self, register, id):
        registerRead = readRegister(int(register))
        '''presetMultipleRegisters(25,550)'''

        self.write(json.dumps({'register':registerRead, 'id':id}))

class PresetRegisterHandler(BaseHandler):
    def get(self, register, val):
        presetMultipleRegisters(int(register), int(val))
        self.write(json.dumps({'value':val}))

class ElementHandler(BaseHandler):
    def get(self, id):
        element = query_by_id(Element, id)
        if not element:
            return self.write({'error':'feed does not exist'})
        self.write({'element':element.to_json()})

    def post(self):
        screen_id = self.get_argument("screen_id", None)
        left = self.get_argument("left", None)
        top = self.get_argument("top", None)
        type = self.get_argument("type", None)
        border = self.get_argument("border", None)
        plc = self.get_argument("plc", None)
        color = self.get_argument("color", None)
        width = self.get_argument("width", None)
        height = self.get_argument("height", None)
        unit1 = self.get_argument("unit1", None)
        unit2 = self.get_argument("unit2", None)
        unit3 = self.get_argument("unit3", None)
        unit4 = self.get_argument("unit4", None)
        level = self.get_argument("level", None)
        label = self.get_argument("label", None)
        value = self.get_argument("value", None)
        register = self.get_argument("register", None)
        coil = self.get_argument("coil", None)
        contact = self.get_argument("contact", None)
        element = Element(screen_id = screen_id, left = left, top = top, type = type, border = border, plc = plc, color = color, width = width, height = height, unit1 = unit1, unit2 = unit2, unit3 = unit3, unit4 = unit4, level = level, label = label, value = value, register = register, coil = coil, contact = contact)
        element = addOrUpdate(element)
        self.write({'element': element.to_json()})

class ScreenHandler(BaseHandler):
    def get(self, id):
        #item = query_by_id(Item, id)
        elements = query_by_field(Element, "screen_id", id)
        if not elements:
            return self.write({'error':'feed does not exist'})

        self.write(json.dumps([i.to_json() for i in elements]))
        #self.write({'item':item.to_json()})


    def put(self):
        title = self.get_argument("title", None)
        description = self.get_argument("description", None)
        private = self.get_argument("private", True)
        if not title:
            return self.write({'error':'you must give us a title'})
        administrators = self.get_argument("administrators", None)
        feed = Feed(title=title,administrators=administrators,description=description,private=private)
        feed = addOrUpdate(feed)
        self.write({'feed': feed.to_json()})

    def post(self, id):
        title = self.get_argument("title", None)
        description = self.get_argument("description", None)
        private = self.get_argument("private", True)
        user = self.current_user
        if not title:
            return self.write({'error':'you must give us a title'})
        feed = query_by_id(Feed, id)
        if not feed:
            return self.write({'error':'feed does not exist'})
        if feed.owner != user.wwuid and user.wwuid not in feed.administrators.split(","):
            return self.write({'error':'insufficient permissions'})
        administrators = self.get_argument("administrators", None)
        feed.title = title
        feed.description = description
        feed.private = private
        feed.administrators = administrators
        feed = addOrUpdate(feed)
        self.write({'feed': feed.to_json()})

    def delete(self, id):
        user = self.current_user
        feed = query_by_id(Feed, id)
        if not feed:
            return self.write({'error':'feed does not exist'})
        if feed.owner != user.wwuid:
            return self.write({'error':'insufficient permissions'})
        for item in query_by_field(Item, "feed_id", id):
            delete_thing(item)
        delete_thing(feed)
        self.write(json.dumps("success"))
