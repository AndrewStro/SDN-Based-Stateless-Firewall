#!/usr/bin/env python

"""
Create a mininet based topology with 4 container hosts and two controller, and two switches, then run it
"""

from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI

setLogLevel( 'info' )

# Andrew Strong: Deleted one controller and changed another to a Remote Controller
c1 = RemoteController( 'c1', ip='127.0.0.1', port=6633 )
c2 = RemoteController( 'c2', ip='127.0.0.1', port=6655 )

cmap = { 's1': c1, 's2': c2}

class MultiSwitch( OVSSwitch ):
    "Custom Switch() subclass that connects to different controllers"
    def start( self, controllers ):
        return OVSSwitch.start( self, [ cmap[ self.name ] ] )

# Andrew Strong: I created the entirety of MyTopo, the original controllers.py just used a TreeTopo
class MyTopo(Topo):
	def __init__( self ):
		Topo.__init__( self )
		h1 = self.addHost('h1', ip='10.0.2.10',mac='00:00:00:00:00:01', dimage="ubuntu:trusty")
		h2 = self.addHost('h2', ip='10.0.2.20',mac='00:00:00:00:00:02', dimage="ubuntu:trusty")
		h3 = self.addHost('h3', ip='192.168.2.30',mac='00:00:00:00:00:03', dimage="ubuntu:trusty")
		h4 = self.addHost('h4', ip='192.168.2.40',mac='00:00:00:00:00:04', dimage="ubuntu:trusty")
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')

		self.addLink(h1, s1)
		self.addLink(h2, s1)
		self.addLink(h3, s2)
		self.addLink(h4, s2)
		self.addLink(h1, s2,params1={'ip':'192.168.2.10/8'})

# Andrew Strong: previously was topo = TreeTopo(depth=2, fanout=2)
topo = MyTopo()
net = Mininet( topo=topo, switch=MultiSwitch, build=False, waitConnected=True )
for c in [ c1, c2 ]:
    net.addController(c)
net.build()
net.start()
CLI( net )
net.stop()
