from pox.core import core
form pox.lib.addresses import EthAddr
import pox.openflow.libopenflow_01 as of

#show the output to console 
log = core.getLogger()


#my switch class have funtionality to flood,drop packet and send src to dst 
class mySwitch(object):
    
    #initilize the MAC table as dict
    #call addlisteners	
    def __init__ (self):
        self.mac_to_port = {}
        #....?
        core.openflow.addListeners(self)
    
    #drop the packets 
    def drop(self, event):
        #...?
        msg = of.ofp_flow_mod()
        #duration of packet arrive, is set 100 if not arrive so remove flow
        msg.idle_timeout = 100
        #...?
        msg.match = of.ofp_match.from_packet(packet)
        event.connection.send(msg)

    #flood the packet to everyone		
    def flood(self, event):
        #...?
        msg = of.ofp_packet_out()
        #add action and flood packet
        action = msg.actions(of.ofp_action_ouput(port = of.OFPP_FLOOD)
        #apppend action into action list
        msg.append(action)
        #...?
        event.connection.send(msg)
	 
    #ping to someone, method works on it
    def _handle_PacketIn(self, event):
        #parse/save packet(event) into packet variable
        packet = event.parsed
        #save packet source and it's port into dict
        self.mac_to_port[packet.src] = packet.port
        #if destination is multicast flood it
        #...?
        if packet.dst.is_multicast:
            log.debug("destination is multi-cast")
            self.flood(event)
        #if destination if not in MAC flood 
        elif packet.dst not in self.mac_to_port:
            log.debug("not in mac table")
            self.flood(event)

        #it may same in multiple switch
        elif self.mac_to_port[packet.dst] == packet.port:
            log.debug("ports are same")
            self.drop()
        #install flow entry to switch and send packet to proper port
        else:
            outgoingport = self.mac_to_port[packet.dst]
            log.debug("installing flow for: %s-->%i %s-->%i", packet.src, packet.port, packet.dst, outgoingport)
            #...?
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = 100
            msg.hard_timeout = 1000
            action = msg.actions(of.ofp_action_output(port = outgoingport))
            event.connection.send(msg)


#handle the event pox start with my switch    
def _handle_UpEvent(event):
    log.debug("Pox start with mySwitch")

#just lis=ke main function
def launch():
    core.addListenerByName("UpEvent", _handle_UpEvent)
    #register the class in core to use it
    core.registerNew(mySwitch)

