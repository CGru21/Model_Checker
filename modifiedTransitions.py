from transitions import Machine
from transitions.extensions import GraphMachine
from transitions.extensions.states import add_state_features, Tags, Timeout


@add_state_features(Tags, Timeout)
class KTS(GraphMachine):
    pass

class KTS_model(object):
    pass


