from transitions import *
from transitions.extensions import GraphMachine
from transitions.extensions.states import add_state_features, Tags, Timeout


@add_state_features(Tags, Timeout)
class KTS(GraphMachine):
    style_attributes = {
        "node": {
            "": {},
            "default": {
                "style": "rounded, filled",
                "shape": "rectangle",
                "fillcolor": "white",
                "color": "black",
                "peripheries": "1",
            },
            "inactive": {"fillcolor": "white", "color": "black", "peripheries": "1"},
            "parallel": {
                "shape": "rectangle",
                "color": "black",
                "fillcolor": "white",
                "style": "dashed, rounded, filled",
                "peripheries": "1",
            },
            "active": {"color": "black", "fillcolor": "white", "peripheries": "1"},
            "previous": {"color": "blue", "fillcolor": "azure2", "peripheries": "1"},
            "sat": {"color": "green", "fillcolor": "lightgreen", "peripheries": "1"}, #add style for sat/unsat formula
            "unsat": {"color": "red", "fillcolor": "darksalmon", "peripheries": "1"},
        },
        "edge": {"": {}, "default": {"color": "black"}, "previous": {"color": "blue"}},
        "graph": {
            "": {},
            "default": {"color": "black", "fillcolor": "white", "style": "solid"},
            "previous": {"color": "blue", "fillcolor": "azure2", "style": "filled"},
            "active": {"color": "red", "fillcolor": "darksalmon", "style": "filled"},
            "parallel": {"color": "black", "fillcolor": "white", "style": "dotted"},
        },
    }
    
    def generate_image(self, model):
        self.model_graphs[id(model)].get_graph().draw('kts.png', prog='dot')

class KTS_model():
    pass


