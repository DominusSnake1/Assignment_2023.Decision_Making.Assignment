import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import pandas as pd
import math


def test():
    community_graph = nx.barabasi_albert_graph(20, 3)
    nx.draw(community_graph, with_labels=True)
    plt.show()
