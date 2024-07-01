import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._soluzioneBest = []
        self._bestSomma = 0

    def getPercorso(self, N):
        self._soluzioneBest = []
        self._bestSomma = 0


        self.ricorsione([], N)

        return self._soluzioneBest, self._bestSomma

    def ricorsione(self, parziale, N):
        if len(parziale)>= 1 and parziale[0] == parziale[-1] and len(parziale) == (N-1):
            if self.getSomma(parziale) > self._bestSomma:
                self._bestSomma = self.getSomma(parziale)
                self._soluzioneBest = copy.deepcopy(parziale)
                return

        else:
            nodi = self._grafo.nodes
            for n in nodi:
                vicini = list(nx.neighbors(self._grafo, n))
                vicini.sort(key = lambda n: n.weight, reverse=True)
                parziale.append(vicini[0])
                self.ricorsione(parziale, N)
                parziale.pop()

    def getSomma(self, listaNodi):
        if len(listaNodi) == 0:
            return 0
        sommaPesi = 0
        for i in listaNodi:
            sommaPesi += self._grafo[listaNodi[i]][listaNodi[i+1]]["weight"]
        return sommaPesi


    def getNazioni(self):
        return DAO.getNazioni()

    def getAnni(self):
        return DAO.getAnni()

    def buildGraph(self, c, a):
        self._grafo.clear()
        self._nodes = DAO.getRivenditori(c)
        self._grafo.add_nodes_from(self._nodes)
        self._idMap = {}
        for node in self._nodes:
            self._idMap[node.Retailer_code] = node

        nodiCollegati = DAO.getCollegamenti(a, self._idMap)
        for n in nodiCollegati:
            self._grafo.add_edge(n.r1, n.r2, weight=n.peso)
            #print(n.r1.Retailer_name, n.r2.Retailer_name, n.peso)


    def calcolaVolume(self):
        rivenditori = self._grafo.nodes
        tupla = []
        for r in rivenditori:
            volume = 0
            vicini = nx.neighbors(self._grafo, r)
            for v in vicini:
                volume += self._grafo[r][v]["weight"]
            tupla.append((r, volume))
        tupla.sort(key=lambda x:x[1], reverse=True)
        return tupla



    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def getPeso(self, p1, p2):
        return self._grafo[p1][p2]["weight"]
