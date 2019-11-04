#core knows about each and every components of pox
from pox.core import core
#openflow connect POX and Mininet 
import pox.openflow.libopenflow_01 as OF
# through the getlogger method which is in core we can display all result in console 
#we are saving result into variable log
log = core.getLogger()
#this method works when the pox start running
#when we start or controoller POX, event occurs and it start running 
def _handle_EventUp(event):
	log.debug("pox has been started with the hub(mininet)")
#after starting it connectes with the hub/switch and contol all the swithces or hub 
def _handle_Connection(event):
	log.debug("POX(controller) is connected with the hub")
#when someone ping to any other host so event occures in network
#controller control the event and send the packet to its destination
#receiver can check from which port it eceive packet using event 
def _handle_PacketIn(event):
	log.debug("Packet is recvied")
	log.debug("Port informaton %s", event.port)
	msg = OF.ofp_flow_mod()
	#flood data, means pass data to every one
	msg.actions.append(OF.ofp_action_output(port = OF.OFPP_FLOOD))
	event.connection.send(msg)
#this is someting like main method
#we are calling every method from core all are registered in core and we passed parameters in it 
def launch():
	core.addListenerByName("UpEvent", _handle_EventUp)
	core.openflow.addListenerByName("ConnectionUp", _handle_Connection)
	core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
        #----------------------------------------------------#
