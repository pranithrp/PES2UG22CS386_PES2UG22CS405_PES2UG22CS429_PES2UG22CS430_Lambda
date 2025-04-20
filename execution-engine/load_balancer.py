import random

class LoadBalancer:
    def __init__(self, nodes):
        self.nodes = nodes  # List of available Docker containers or nodes
        self.current = 0

    def get_next_node(self):
        if not self.nodes:
            raise Exception('No nodes available')
        node = self.nodes[self.current]
        self.current = (self.current + 1) % len(self.nodes)
        return node

    def add_node(self, node):
        self.nodes.append(node)

    def remove_node(self, node):
        self.nodes.remove(node)