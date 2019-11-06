#core is very import lib through this we can use multiple module in our code
#multiple modules is registered in the core, no need to add futher lib in our code
from pox.core import core
import pox.openflow.libopenflow_01 as of
#initilize object of getLogger, through this we can show our output to console
log = core.getLogger()

#my builden switch class 
class LearningSwitch(object):

    #initilize a dict, to store mac,dpid(switch unique id) and the port no.
    #listen the event, openflow is class addLister is it's method and class is reg in the core 
    def __init__ (self):
        self.mac_to_port = {}
        core.openflow.addListeners(self)


    #method for flood packet
    #msg is obeject of ofp_packet_out class
    #we made an action and append it into actions
    #dn't send packet into in_port  
    def flood(self,event):
        msg = of.ofp_packet_out()
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        msg.buffer_id = event.ofp.buffer_id
        msg.data = event.ofp
        msg.in_port = event.port
        event.connection.send(msg)

    #method for drop the packets
    #msg is object of ofp_flow_mod
    #similar packets ll be drop match..

    def drop(self,event):
        packet = event.parsed
        msg = of.ofp_flow_mod()
        msg.buffer_id = event.buffer_id
        msg.match = of.ofp_match.from_packet(packet)
        event.connection.send(msg)



    #this method handles all the receving packets and take decision on the behalf of packet information
    #parse the event(comming packet), and save the mac of src,dst in it
    #save mac,dpid,port into our dict
    #check packet.dst is multi-cast flood it to everyone
    #check packet is not in dict flood it to everyone
    #check packet src port and the dst port is same drop it
    #make the path src to dst 
    def _handle_PacketIn(self, event):
        packet = event.parsed
        self.mac_to_port[(packet.src,event.dpid)] = event.port

        if packet.dst.is_multicast:
            log.debug("packet is multi-cast")
            self.flood(event)
            
        elif (packet.dst,event.dpid) not in self.mac_to_port:
            self.flood(event)
            log.debug("dest in not in table, flood packet")

        elif self.mac_to_port[(packet.dst,event.dpid)] == event.port:
            self.drop(event)
            log.debug("incoming and out going port is same drop it")
        else:
            outport = self.mac_to_port[(packet.dst,event.dpid)]
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet)
            msg.data = event.ofp
            msg.actions.append(of.ofp_action_output(port = outport))
            event.connection.send(msg)



#handle the event when the pox controller start working 
#display the message in the console "hello................"
def _handle_EventUp(self):
    log.debug("Hello Network Pox is connected and start working with the topology")

#when POX start working it check the launch method in given file 
#we can listen the event through this and event handle method handles the event
#we should register self made class into core
def launch():
    core.addListenerByName("UpEvent", _handle_EventUp)
    core.registerNew(LearningSwitch)
