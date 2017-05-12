#!/usr/bin/python

"""
Create a network where different switches are connected to
different controllers, by creating a custom Switch() subclass.
"""

from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.topolib import TreeTopo
from mininet.log import setLogLevel
from mininet.cli import CLI
from time import sleep
from mininet.log import output, warn
from random import randint
import time
setLogLevel( 'info' )
# 4 sub-controllers and 1 root controller
c0 = RemoteController( 'c0', ip='192.168.56.101', port=6633 )
c1 = RemoteController( 'c1', ip='192.168.56.102', port=6634 )
c2 = RemoteController( 'c2', ip='192.168.56.103', port=6635 )
c3 = RemoteController( 'c3', ip='192.168.56.104', port=6636 )
c4 = RemoteController( 'c4', ip='127.0.0.1', port=6637 )

#mapping the switch with its controller
cmap = { 's1': c0, 's2': c0, 's3': c0, 's4': c0, 
         's5': c1, 's6': c1, 's7': c1, 's8': c1,
         's9': c2, 's10': c2, 's11': c2, 's12': c2,
         's13':c3, 's14':c3, 's15':c3, 's16':c3, 's17':c3 }

#creating additional methods for host mobility
class MultiSwitch( OVSSwitch ):
    "Custom Switch() subclass that connects to different controllers"
    def start( self, controllers ):
        return OVSSwitch.start( self, [ cmap[ self.name ] ] )

    def delIntf( self, intf ):
        "Remove (and detach) an interface"
        port = self.ports[ intf ]
        del self.ports[ intf ]
        del self.intfs[ port ]
        del self.nameToIntf[ intf.name ]

    def addIntf( self, intf, rename=False, **kwargs ):
        "Add (and reparent) an interface"
        print 'add interface **',intf
        OVSSwitch.addIntf( self, intf, **kwargs )
        intf.node = self
        if rename:
            self.renameIntf( intf )

    def attach( self, intf ):
        "Attach an interface and set its port"
        port = self.ports[ intf ]
        if port:
            if self.isOldOVS():
                self.cmd( 'ovs-vsctl add-port', self, intf )
            else:
                self.cmd( 'ovs-vsctl add-port', self, intf,
                          '-- set Interface', intf,
                          'ofport_request=%s' % port )
            self.validatePort( intf )

    def validatePort( self, intf ):
        "Validate intf's OF port number"
        ofport = int( self.cmd( 'ovs-vsctl get Interface', intf,
                                'ofport' ) )
        if ofport != self.ports[ intf ]:
            warn( 'WARNING: ofport for', intf, 'is actually', ofport,
                  '\n' )

    def renameIntf( self, intf, newname='' ):
        "Rename an interface (to its canonical name)"
        intf.ifconfig( 'down' )
        if not newname:
            newname = '%s-eth%d' % ( self.name, self.ports[ intf ] )
        intf.cmd( 'ip link set', intf, 'name', newname )
        del self.nameToIntf[ intf.name ]
        intf.name = newname
        self.nameToIntf[ intf.name ] = intf
        intf.ifconfig( 'up' )

    def moveIntf( self, intf, switch, port=None, rename=True ):
        print intf, switch, port, rename
        "Move one of our interfaces to another switch"
        self.detach( intf )
        self.delIntf( intf )
        switch.addIntf( intf, port=port, rename=rename )
        switch.attach( intf )

def printConnections( switches ):
    "Compactly print connected nodes to each switch"
    for sw in switches:
        output( '%s: ' % sw )
        for intf in sw.intfList():
            link = intf.link
            if link:
                intf1, intf2 = link.intf1, link.intf2
                remote = intf1 if intf1.node != sw else intf2
                output( '%s(%s) ' % ( remote.node, sw.ports[ intf ] ) )
        output( '\n' )


def moveHost( host, oldSwitch, newSwitch, newPort=None ):
    "Move a host from old switch to new switch"
    hintf, sintf = host.connectionsTo( oldSwitch )[ 0 ]
    oldSwitch.moveIntf( sintf, newSwitch, port=newPort )
    return hintf, sintf
 
   
def mobilityTest(): 
 net = Mininet( controller=RemoteController, switch=MultiSwitch, build=False )
 #Adding controllers
 for c in [ c0, c1, c2, c3, c4 ]:
    net.addController(c)

 #Adding switches 
 s1 = net.addSwitch( 's1' )
 s2 = net.addSwitch( 's2' )
 s3 = net.addSwitch( 's3' )
 s4 = net.addSwitch( 's4' )

 s5 = net.addSwitch( 's5' )
 s6 = net.addSwitch( 's6' )
 s7 = net.addSwitch( 's7' )
 s8 = net.addSwitch( 's8' )
 
 s9 = net.addSwitch( 's9' )
 s10 = net.addSwitch( 's10' )
 s11 = net.addSwitch( 's11' )
 s12 = net.addSwitch( 's12' )
 
 s13 = net.addSwitch( 's13' )
 s14 = net.addSwitch( 's14' )
 s15 = net.addSwitch( 's15' )
 s16 = net.addSwitch( 's16' )
 s17 = net.addSwitch( 's17' )
  
 #Adding hosts
 h1 = net.addHost( 'h1' )
 h2 = net.addHost( 'h2' )
 h3 = net.addHost( 'h3' )
 h4 = net.addHost( 'h4' )

 h5 = net.addHost( 'h5' )
 h6 = net.addHost( 'h6' )
 h7 = net.addHost( 'h7' ) 
 h8 = net.addHost( 'h8' )

 h9 = net.addHost( 'h9' )
 h10 = net.addHost( 'h10' )
 h11 = net.addHost( 'h11' )
 h12 = net.addHost( 'h12' )
 
 h13 = net.addHost( 'h13' )
 h14 = net.addHost( 'h14' )
 h15 = net.addHost( 'h15' )
 h16 = net.addHost( 'h16' )
 h17 = net.addHost( 'h17' )

 #adding link between switches and hosts
 net.addLink( s1, h1 )
 net.addLink( s2, h2 )
 net.addLink( s3, h3 )
 net.addLink( s4, h4 )
 
 net.addLink( s5, h5 )
 net.addLink( s6, h6 )
 net.addLink( s7, h7 )
 net.addLink( s8, h8 )

 net.addLink( s9, h9 )
 net.addLink( s10, h10 )
 net.addLink( s11, h11 )
 net.addLink( s12, h12 )

 net.addLink( s13, h13 )
 net.addLink( s14, h14 )
 net.addLink( s15, h15 )
 net.addLink( s16, h16 ) 
 net.addLink( s17, h17 )
 
 #Adding links between switches
 net.addLink( s1, s2 )
 net.addLink( s2, s3 )
 net.addLink( s3, s4 )
 net.addLink( s4, s5 )

 net.addLink( s5, s6 )
 net.addLink( s6, s7 )
 net.addLink( s7, s8 )
 net.addLink( s8, s9 )

 net.addLink( s9, s10 )
 net.addLink( s10, s11 )
 net.addLink( s11, s12 )
 net.addLink( s12, s13 )


 net.addLink( s13, s14 )
 net.addLink( s14, s15 )
 net.addLink( s15, s16 )
 net.addLink( s16, s17 )
 net.build()
 net.start()

 net.pingAll()
 
 #start communication between two hosts
 h1.cmd('iperf -s & > s.txt')
 h16.cmd('iperf -c h1 > c.txt ')


 #Code for moving host to another domain
 printConnections( net.switches )
 h1, old = net.get( 'h1', 's1' )
 # If you want to increase the mobility frequency, add for loop 
 # and call the functions for moving the hosts between multiple domains
 new = net[ 's7' ] 
 port = randint( 10, 20 )
 #port = 4
 print '* Moving', h1, 'from', old, 'to', new, 'port', port
 hintf, sintf = moveHost( h1, old, new, newPort=port )
 print '*', hintf, 'is now connected to', sintf
 print '* Clearing out old flows'
 for sw in net.switches:
     sw.dpctl( 'del-flows' )
 t2 = time.clock()
 print 'end time:', t2
 time1 = t2 - t1
 print 'time taken:', time1
 print '* New network:'
 printConnections( net.switches )
 print '* Testing connectivity:'
 h1.cmd('kill %while')
 
 CLI( net )
 
 

 net.stop()

if __name__ == '__main__':
 mobilityTest()

