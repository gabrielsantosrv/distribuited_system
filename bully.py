'''
  Reference: https://isuruuy.medium.com/electing-master-node-in-a-cluster-using-bully-algorithm-b4e4fa30195c
'''

class Bully:
    def __init__(self, node_name, node_id, port_number, election=False, coordinator=False):
        self.node_name = node_name
        self.node_id = node_id
        self.port = port_number
        self.election = election
        self.coordinator = coordinator