from utility import TravianUtility as tu
import networkx as nx
import pickle
import matplotlib.pyplot as plt
import numpy as np

"""
Test merge of two weighted Graph in a labeled and weighted MultiGraph (used for merge trades and raids)
"""
print("Test merge graphs")
G = nx.MultiDiGraph()
G.add_edges_from([
    ('0','20'),
    ('0','20'),
    ('20','0'),
    ('10','20'),
    ('10','30'),
    ('20','40'),
    ('30','50'),
])

weighted_undirected_prova = nx.Graph()
weighted_undirected_prova.add_nodes_from(G.nodes(data=True))

for u,v in G.edges():
    if weighted_undirected_prova.has_edge(u,v):
        weighted_undirected_prova[u][v]['weight'] += 1
    else:
        weighted_undirected_prova.add_edge(u, v, weight=1)

G2 = nx.MultiDiGraph()
G2.add_edges_from([
    ('0','20'),
    ('0','20'),
    ('20','0'),
    ('10','20'),
    ('10','30'),
    ('20','40'),
    ('30','50'),
])

weighted_undirected_prova2 = nx.Graph()
weighted_undirected_prova2.add_nodes_from(G.nodes(data=True))

for u,v in G2.edges():
    if weighted_undirected_prova2.has_edge(u,v):
        weighted_undirected_prova2[u][v]['weight'] += 1
    else:
        weighted_undirected_prova2.add_edge(u, v, weight=1)

prova_prova2 = nx.MultiGraph()
prova_prova2.add_nodes_from(weighted_undirected_prova.nodes(data=True))
prova_prova2.add_nodes_from(weighted_undirected_prova2.nodes(data=True))
for u,v,data in weighted_undirected_prova.edges(data=True):
    prova_prova2.add_edge(u, v, weight=data['weight'], type="trade")
for u,v,data in weighted_undirected_prova2.edges(data=True):
    prova_prova2.add_edge(u, v, weight=data['weight'], type="raid")

"""
Test merge of two nodes
"""
print("Test merge nodes")
tu.merge(G,'20','30', '', '')

"""
Creazione del grafo delle alleanze:
Unione dei nodi appartenenti alla stessa alleanza mantenendo gli archi
"""
print("Allys graphs creation")
MGs, TDs, RDs, allies_per_day = tu.read_all()
for day, allies_per_day in enumerate(allies_per_day):    
    for ally in allies_per_day:
        nodes = []
        for node in ally:
            nodes.append(str(node))
        contractor = nodes[0]
        id_ally = MGs[day].nodes[contractor]['ally']
        if len(nodes) > 1:
            for i in range(1, len(nodes)):
                #MGs[day] = nx.contracted_nodes(MGs[day], contractor, nodes[i], self_loops=False)
                _ = tu.merge(MGs[day], contractor, nodes[i], id_ally, len(nodes))
                _ = tu.merge(TDs[day], contractor, nodes[i], id_ally, len(nodes))
                contractor = tu.merge(RDs[day], contractor, nodes[i], id_ally, len(nodes))
        #while MGs[day].has_edge(contractor,contractor):
        #    MGs[day].remove_edge(contractor,contractor)     
    """
    Decommentare per salvare i risultati
    """
    """
    if day < 10:
        nx.write_gexf(MGs[day],'resources/messages_contracted_by_ally_gefx/message_contracted_0' + str(day+1) + '.gexf')
        nx.write_gpickle(MGs[day], "resources/messages_contracted_by_ally/message_contracted_0"+ str(day+1) )
        nx.write_gexf(TDs[day],'resources/trades_contracted_by_ally_gefx/trades_contracted_0' + str(day+1) + '.gexf')
        nx.write_gpickle(TDs[day], "resources/trades_contracted_by_ally/trades_contracted_0"+ str(day+1) )
        nx.write_gexf(RDs[day],'resources/raids_contracted_by_ally_gefx/raids_contracted_0' + str(day+1) + '.gexf')
        nx.write_gpickle(RDs[day], "resources/raids_contracted_by_ally/raids_contracted_0"+ str(day+1) )
    else:
        nx.write_gexf(MGs[day],'resources/messages_contracted_by_ally_gefx/message_contracted_' + str(day+1) + '.gexf')        
        nx.write_gpickle(MGs[day], "resources/messages_contracted_by_ally/message_contracted_" + str(day+1) )
        nx.write_gexf(TDs[day],'resources/trades_contracted_by_ally_gefx/trades_contracted_' + str(day+1) + '.gexf')
        nx.write_gpickle(TDs[day], "resources/trades_contracted_by_ally/trades_contracted_"+ str(day+1) )
        nx.write_gexf(RDs[day],'resources/raids_contracted_by_ally_gefx/raids_contracted_' + str(day+1) + '.gexf')
        nx.write_gpickle(RDs[day], "resources/raids_contracted_by_ally/raids_contracted_"+ str(day+1) )
    """
    print('Day '+str(day)+' contracted')

"""
Lettura da file pickle dei grafi complessivi dei 30 giorni
"""

#tu.all_day_graphs() # decommentrare per creare i grafi completi dei 30 giorni
mg_complete, td_complete, rd_complete = tu.read_all_complete()
print("Messages frequency: " + str(mg_complete.size()))
#print("Utente 1 degree: " + str(mg_complete.degree['1'])) # 0
#print("Utente 2 degree: " + str(mg_complete.degree['2'])) # 0
print("Raids frequency: %d" % rd_complete.size())
#print("Utente 1 degree: " + str(rd_complete.degree['1'])) # 0
#print("Utente 2 degree: " + str(rd_complete.degree['2'])) # 0
print("Trades frequency: %d" % td_complete.size())
#print("Utente 1 degree: " + str(td_complete.degree['1'])) # 5
#print("Utente 2 degree: " + str(td_complete.degree['2'])) # 0
"""
Creazione grafo senza amministratori per analisi in gephi
"""
mg_complete.remove_node('1')
mg_complete.remove_node('2')
#nx.write_gpickle(mg_complete, "resources/messages_all_whitout_admin")
#nx.write_gexf(mg_complete, "resources/messages_all_without_admin.gexf")

"""
Creazione del grafo dei rapporti tra alleanze e giocatori singoli come nel capitolo 4 della relazione
E' un operazione fatta su un singolo giorno. Impostare day al valore desiderato
"""
#MGs, TDs, RDs, allies_per_day = tu.read_all()
MGs, TDs, RDs = tu.read_all_contracted(mg = False, td = True, rd = True)
day = 20
# create weighted graph from first day of trades
weighted_undirected_trade = nx.Graph()

weighted_undirected_trade.add_nodes_from(TDs[day].nodes(data=True))

for u,v in TDs[day].edges():
    
    if weighted_undirected_trade.has_edge(u,v):
        weighted_undirected_trade[u][v]['weight'] += 1
    else:
        weighted_undirected_trade.add_edge(u, v, weight=1)

#nx.write_gexf(weighted_undirected_trade,'resources/trade_weighted_day_'+str(day+1)+'.gexf')

# create weighted graph from first day of raids
weighted_undirected_raid = nx.Graph()

weighted_undirected_raid.add_nodes_from(RDs[day].nodes(data=True))

for u,v in RDs[day].edges():
    if weighted_undirected_raid.has_edge(u,v):
        weighted_undirected_raid[u][v]['weight'] += 1
    else:
        weighted_undirected_raid.add_edge(u, v, weight=1)

#nx.write_gexf(weighted_undirected_raid,'resources/raid_weighted_day_'+str(day+1)+'.gexf')

td_rd = nx.MultiGraph()

td_rd.add_nodes_from(weighted_undirected_raid.nodes(data=True))
td_rd.add_nodes_from(weighted_undirected_trade.nodes(data=True))
for u,v,data in weighted_undirected_trade.edges(data=True):
    td_rd.add_edge(u, v, weight=data['weight'], type="trade")
for u,v,data in weighted_undirected_raid.edges(data=True):
    td_rd.add_edge(u, v, weight=data['weight'], type="raid")

#nx.write_gexf(td_rd,'resources/td_rd.gexf')

relationship = nx.Graph()
relationship.add_nodes_from(td_rd.nodes(data = True))

for u,v,data in td_rd.edges(data = True):
    trade = 0
    raid = 0
    ratio = 0
    
    if not(relationship.has_edge(u,v)):
        for e in td_rd[u][v]:
            if data["type"] == "trade":
                trade = data["weight"]
            else:
                raid = data["weight"]

        if trade == 0 and raid == 0:
            pass
        elif trade == 0:
            relationship.add_edge(u,v,relation="conflictual")
        elif raid == 0:
            relationship.add_edge(u,v,relation="friend")
        else:
            ratio = raid/(raid+trade)
            if ratio <= 0.3:
                relationship.add_edge(u,v,relation="friend")
            elif ratio >= 0.7:
                relationship.add_edge(u,v,relation="conflictual")
            else:
                relationship.add_edge(u,v,relation="caotic")

#nx.write_gexf(relationship,'resources/relationship_day_'+str(day+1)+'.gexf') # Decommentare per salvare il grafo


"""
Estrazione singola alleanza da visualizzare in gephi
"""
nodes = []
for node in allies_per_day[0][2]:
    nodes.append(int(node))
sub_mg = MGs[0].subgraph(nodes)

nx.write_gexf(sub_mg,'mg_community_4people.gexf')

"""
Rimozione messaggi in broadcast

edge_to_remove = [[],[],[]]
for n, nbrsdict in sub_mg.adjacency():
    times = []
    for nbr, keydict in nbrsdict.items():
        for key, eattr in keydict.items():
            if 'time' in eattr:
                times.append(eattr['time'])
    
    for index in range(len(times) - 1, -1, -1):
        if times.count(times[index]) == 1:
            del times[index]

    for nbr, keydict in nbrsdict.items():
        for key, eattr in keydict.items():
            if eattr['time'] in times:
                edge_to_remove[0].append(n)
                edge_to_remove[1].append(nbr)
                edge_to_remove[2].append(key)

unfrozen_graph = nx.MultiDiGraph(sub_mg)
for n, nbr, key in zip(edge_to_remove[0],edge_to_remove[1], edge_to_remove[2]):
    unfrozen_graph.remove_edge(n, nbr, key=key)

nx.write_gexf(unfrozen_graph,'mg_community_no_broadcast.gexf')

"""


"""
Andamento della popolosità delle alleanze nel corso dei 30 giorni
"""
#[{"day": 1, "allies_members":[[1,2],[3,4,5]], "allies_population":[2,3]}
bins = [1,2,5,10,20,40,61]
populations = []
hists = []
categories = [[],[],[],[],[],[]]
for day in allies_per_day:
    population = []
    for a in day:
        population.append(len(a))
    hist, bin_edges = np.histogram(population,bins)
    for idx, h in enumerate(hist):
        categories[idx].append(h)
    populations.append(population)
    hists.append(hist)


x = np.arange(1,31)
for idx, cat in enumerate(categories):
    #plt.plot( x, cat, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4, label = str(bins[idx]))
    plt.plot( x, cat, marker='o', markersize=4, linewidth=2, label = 'from ' + str(bins[idx]) +' to ' + str(bins[idx+1]-1))
    plt.title("Number of community day by day")
    plt.xlabel("days")
    plt.ylabel("frequency")
    

plt.legend()
plt.show()