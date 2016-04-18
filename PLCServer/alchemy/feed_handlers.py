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

    print(b)
    '''this is to output the state of each coil read '''
    for x in range(0, len(b)):
        for i in range(0, 8):
            if start+i+8*x <= end:
                print("Coil #{} is a {}".format(start+i+8*x, b[x][7-i]))
                return b[x][7-i]


    '''print("RX: ",  b, len(b))'''

class ReadCoilHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, coil, id):
        print(coil)
        coilWrite = ReadCoil(int(coil))
        print("it works")

        self.write(json.dumps({'coil':coilWrite, 'id':id}))

class FeedHandler(BaseHandler):
    def get(self, id):
        feed = query_by_id(Feed, id)
        if not feed:
            return self.write({'error':'feed does not exist'})
        self.write({'feed':feed.to_json()})

    @tornado.web.authenticated
    def put(self):
        title = self.get_argument("title", None)
        description = self.get_argument("description", None)
        private = self.get_argument("private", True)
        user = self.current_user
        if not title:
            return self.write({'error':'you must give us a title'})
        administrators = self.get_argument("administrators", None)
        feed = Feed(title=title,owner=user.wwuid,administrators=administrators,description=description,private=private)
        feed = addOrUpdate(feed)
        self.write({'feed': feed.to_json()})

    @tornado.web.authenticated
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

    @tornado.web.authenticated
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
