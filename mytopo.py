from mininet.topo import Topo


#simple topology class with employee,manager,finance as host
#and their switches
class MyTopo( Topo ):
    
    def __init__( self ):
        
        Topo.__init__( self )
        
        #add hosts
        Emp1Host = self.addHost( 'emp1' )
        Emp2Host = self.addHost( 'emp2' )
        
        M1Host = self.addHost( 'm1' )
        M2Host = self.addHost( 'm2' )
        
        F1Host = self.addHost( 'f1' )
        F2Host = self.addHost( 'f2' )
        
        #add switch
        ESwitch = self.addSwitch( 's1' )
        FSwitch = self.addSwitch( 's2' )
        MSwitch = self.addSwitch( 's3' )
        
        
        #add links
        self.addLink( Emp1Host, ESwitch )
        self.addLink( Emp2Host, ESwitch )
        
        self.addLink( M1Host, MSwitch )
        self.addLink( M2Host, MSwitch )
        
        self.addLink( F1Host, FSwitch )
        self.addLink( F2Host, FSwitch )
        
        self.addLink( ESwitch, MSwitch )
        self.addLink( MSwitch, FSwitch )

#give name customTopology        
topos = { 'customTopology': ( lambda: MyTopo() ) }
        
        
        
        
    

