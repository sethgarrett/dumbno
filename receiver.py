#!/usr/bin/python
import sys
import pika
import socket
import time


while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', int(sys.argv[3])))
        sock.settimeout(5)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,1024)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=sys.argv[2]))
        channel = connection.channel()
        channel.queue_declare(queue=sys.argv[1])
        print 'Listening for Bro Shunts'

        while True:

            try :
                data = sock.recv(1024)
            except socket.timeout:
                continue
            except Exception,e:
                print e
                print 'error'
                pass

            channel.basic_publish(exchange='',
                              routing_key=sys.argv[1],
                              body=data)

    except:
        print 'crashed'
	connection.close()
	time.sleep(10)
