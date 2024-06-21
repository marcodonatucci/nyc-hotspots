import copy
from database.DAO import DAO
import networkx as nx
from geopy.distance import distance
import random


class Model:
    def __init__(self):
        self._bestComp = []
        self.graph = nx.Graph()
        self.locations = []

    def get_providers(self):
        return DAO.get_providers()

    def buildGraph(self, provider, soglia):
        self.graph.clear()
        nodes = DAO.get_locations(provider)
        self.graph.add_nodes_from(nodes)
        for node1 in self.graph.nodes:
            for node2 in self.graph.nodes:
                if node1 != node2:
                    peso = distance((node1.Latitude, node1.Longitude), (node2.Latitude, node2.Longitude)).km
                    if peso <= soglia:
                        self.graph.add_edge(node1, node2, weight=peso)
        return True

    def getGraphDetails(self):
        return f"Grafo creato con {len(self.graph.nodes)} nodi e {len(self.graph.edges)} archi."

    def analyze(self):
        vicini = []
        for node in self.graph.nodes:
            v = self.graph.neighbors(node)
            l = 0
            for point in v:
                l += 1
            vicini.append((node, l))
        vicini.sort(key=lambda x: x[1],
                    reverse=True)
        result = []
        i = 0
        while True:
            if vicini[i][1] == vicini[i + 1][1]:
                result.append(vicini[i])
                self.locations.append(vicini[i][0])
                i += 1
            else:
                result.append(vicini[i])
                self.locations.append(vicini[i][0])
                break
        return result

    def get_nodes(self):
        return self.graph.nodes

    def getPath(self, l0, s):
        # caching con variabili della classe (percorso migliore e peso maggiore)
        self._bestComp = []
        start = self.locations[random.randint(0, len(self.locations)-1)]
        # inizializzo il parziale con il nodo iniziale
        parziale = [start]
        self._ricorsionev2(parziale, l0, s)
        return self._bestComp

    def _ricorsionev2(self, parziale, l0, s):
        # verifico se soluzione è migliore di quella salvata in cache
        if parziale[-1] == l0:
            if len(parziale) > len(self._bestComp):

                self._bestComp = copy.deepcopy(parziale)
            return
        for l in self.graph.neighbors(parziale[-1]):
            if l not in parziale and s.lower() not in l.Location.lower():
                parziale.append(l)
                self._ricorsionev2(parziale, l0, s)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking
