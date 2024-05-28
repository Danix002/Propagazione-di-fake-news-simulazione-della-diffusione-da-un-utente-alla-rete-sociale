import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as cpm
import random

class stochastic_attribute_model(cpm.NodeStochastic): 
    def init (self, ratio, attribute, triggering_status = None):
        super().__init__(ratio, triggering_status)
        self.attribute = attribute
    
    def execute(self, model, state, node, pos, status_map):
        if state[node] == status_map[self.status]:
            if self.triggering_status is not None:
                neighbors = model.graph.neighbors(node)
                if not any(state[n] == status_map[self.triggering_status] for n in neighbors):
                    return False

            b = random.random()
            node_infection_risk = model.graph.nodes[node].get(self.attribute, 1.0)  # Default to 1.0 if attribute not set
            if b <= self.ratio * node_infection_risk:
                return True
        return False

