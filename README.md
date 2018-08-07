This version adds the following to the ncsa:master:
1) RabbitMQ 
----Requires RabbitMQ to be installed.  See .cfg and receiver examples for queue,host, and port mapping.
----Makes the process handle shunts coming in at a higher rate
----You will need to install RabbitMQ prior to this working.
2) Updates are batched
----Updating the ACL per line is slower than feeding a larger batch of lines at once.
----It will wait for 100 lines or 5 seconds.
----The fewer ACLs you have to update the quicker this is as well.
3) Lowered limit of rules
----I found the Arista 9504 to max out around 7100 acl lines.
----When the limit is hit, dumbno will stop adding lines until some have aged out


No elephant flows!

Usage
=====

Copy examples/example\_dumbno.cfg and edit to match your environment.

Run initial setup and start:

    ./dumbno.py dumbno.cfg setup

Later runs:

    ./dumbno.py dumbno.cfg


Shunting a flow
===============

    >>> import dumbno
    >>> d = dumbno.ACLClient('localhost')
    >>> d.add_acl(src="192.168.1.1", dst="192.168.1.2")
    'ok'
    >>> d.add_acl(src="192.168.1.1", dst="192.168.1.2", proto='tcp', sport='123', dport='456')
    'ok'

The log will show the rule being added, and after a minute or so you will see
the per-port rules get auto purged from all access groups:

    2014-04-28 11:21:11,539 INFO op=ADD seq=501 rule=u'ip host 192.168.1.1  host 192.168.1.2 '

    2014-04-28 11:21:32,982 INFO op=REMOVE acl=bulk_8 seq=501 rule="ip host 192.168.1.1 host 192.168.1.2" matches=None ago=None
    2014-04-28 11:21:32,982 INFO op=REMOVE acl=bulk_7 seq=501 rule="ip host 192.168.1.1 host 192.168.1.2" matches=None ago=None
    2014-04-28 11:21:32,983 INFO op=REMOVE acl=bulk_6 seq=501 rule="ip host 192.168.1.1 host 192.168.1.2" matches=None ago=None
    2014-04-28 11:21:32,983 INFO op=REMOVE acl=bulk_5 seq=501 rule="ip host 192.168.1.1 host 192.168.1.2" matches=None ago=None
    2014-04-28 11:21:32,983 INFO op=REMOVE acl=bulk_4 seq=501 rule="ip host 192.168.1.1 host 192.168.1.2" matches=None ago=None
    2014-04-28 11:21:32,983 INFO op=REMOVE acl=bulk_3 seq=501 rule="ip host 192.168.1.1 host 192.168.1.2" matches=None ago=None
    2014-04-28 11:21:32,983 INFO op=REMOVE acl=bulk_2 seq=501 rule="ip host 192.168.1.1 host 192.168.1.2" matches=None ago=None

A rule that had activity will look like this:

    2014-04-28 11:21:32,983 INFO op=REMOVE acl=bulk_2 seq=729 rule="tcp host 192.168.1.2 eq 39329 host 192.168.1.1 eq 39032" matches=359 ago=0:01:22

IPv6 Support
============

If you are using conn-bulk.bro, you also need to make sure the IPv6 ranges
are included in the 'hosts' table:

    const hosts: table[subnet] of PortRange = {[0.0.0.0/0] = PortRange(),
                                               [[::]/0] = PortRange()} &redef;


