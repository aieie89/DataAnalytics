import networkx as nx
import os
import pickle
import matplotlib.pyplot as plt

PATH_MGs = "resources/messages/"
PATH_TDs = "resources/trades/"
PATH_RDs = "resources/attacks/"
PATH_Allies = 'resources/communities/allies.pickle'

PATH_MGs_contracted = "resources/messages_contracted_by_ally/"
PATH_TDs_contracted = "resources/trades_contracted_by_ally/"
PATH_RDs_contracted = "resources/raids_contracted_by_ally/"

PATH_COMPLETE_MG = "resources/messages_all"
PATH_COMPLETE_TD = "resources/trades_all"
PATH_COMPLETE_RD = "resources/raids_all"

def read_multigraph(path):
    messages_directory_path = path
    messages_directory = os.listdir(messages_directory_path)

    MGs = []

    for file_name in messages_directory:
        MG = nx.read_gpickle(messages_directory_path + file_name)
        MGs.append(MG)

    return MGs

class TravianUtility(object):

    @staticmethod
    def merge(G, n1, n2, ally, ally_pop):
        # Get all predecessors and successors of two nodes
        pre = set(G.predecessors(n1)) | set(G.predecessors(n2))
        suc = set(G.successors(n1)) | set(G.successors(n2))
        # Create the new node with combined name
        name = str(n1) + '/' + str(n2)
        G.add_node(name)
        G.nodes[name]['ally'] = ally
        G.nodes[name]['ally_pop'] = ally_pop
        n = 0
        for p in pre:
            n = G.number_of_edges(p,n1)
            for _ in range(n):
                G.add_edge(p,name)
            n = G.number_of_edges(p,n2)
            for _ in range(n):
                G.add_edge(p,name)
        for s in suc:
            n = G.number_of_edges(n1,s)
            for _ in range(n):
                G.add_edge(name,s)
            n = G.number_of_edges(n2,s)
            for _ in range(n):
                G.add_edge(name,s)
        # Remove old nodes
        G.remove_nodes_from([n1, n2])
        return name

    @staticmethod
    def communities_csv_to_pickle():
        communities_directory_path = "resources/communities_raw/"
        communities_directory = os.listdir(communities_directory_path)
        days = []
        for file_name in communities_directory:
            
            with open(communities_directory_path+file_name) as fp:
                alliances_single_day = []
                for line in fp:
                    ally = line.strip().split(' ')
                    alliances_single_day.append(ally)
                days.append(alliances_single_day)

        with open('resources/communities/allies.pickle', 'wb') as handle:
            pickle.dump(days, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    @staticmethod
    def read_all():
        MGs = read_multigraph(PATH_MGs)
        TDs = read_multigraph(PATH_TDs)
        RDs = read_multigraph(PATH_RDs)

        with open(PATH_Allies, 'rb') as handle:
            Day_ALs = pickle.load(handle)

        return MGs,TDs,RDs,Day_ALs

    @staticmethod
    def read_all_complete():
        mg_complete = nx.read_gpickle(PATH_COMPLETE_MG)
        td_complete = nx.read_gpickle(PATH_COMPLETE_TD)
        rd_complete = nx.read_gpickle(PATH_COMPLETE_RD)

        return mg_complete,td_complete,rd_complete

    @staticmethod
    def all_day_graphs():
        MGs = read_multigraph(PATH_MGs)
        TDs = read_multigraph(PATH_TDs)
        RDs = read_multigraph(PATH_RDs)

        mg_all = nx.MultiDiGraph()
        for mg in MGs:
            for u,v,data in mg.edges(data=True):
                mg_all.add_edge(u,v,time=data["time"])

        td_all = nx.MultiDiGraph()
        for td in TDs:
            for u,v,data in td.edges(data=True):
                td_all.add_edge(u,v,time=data["time"])
        
        rd_all = nx.MultiDiGraph()
        for rd in RDs:
            for u,v,data in rd.edges(data=True):
                rd_all.add_edge(u,v,time=data["time"])
        
        nx.write_gpickle(mg_all, "resources/messages_all")
        nx.write_gexf(mg_all, "resources/messages_all.gexf")
        nx.write_gpickle(rd_all, "resources/raids_all")
        nx.write_gexf(rd_all, "resources/raids_all.gefx")
        nx.write_gpickle(td_all, "resources/trades_all")
        nx.write_gexf(td_all, "resources/trades_all.gexf")
        

    @staticmethod
    def read_all_contracted(mg = True, td = True, rd = True):
        MGs = None
        TDs = None
        RDs = None
        if mg:
            MGs = read_multigraph(PATH_MGs_contracted)
        if td:
            TDs = read_multigraph(PATH_TDs_contracted)
        if rd:
            RDs = read_multigraph(PATH_RDs_contracted)
        
        return MGs,TDs,RDs

    @staticmethod
    def clean_msg_csv(mg):
        lines_seen = set() # holds lines already seen
        outfile = open("out.txt", "w")
        for line in open("input.txt", "r"):
            if line not in lines_seen: # not a duplicate
                outfile.write(line)
                lines_seen.add(line)
        outfile.close()
        

    @staticmethod
    def remove_broadcast(mg):
        edge_to_remove = [[],[],[]]
        for n, nbrsdict in mg.adjacency():
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

        unfrozen_graph = nx.MultiDiGraph(mg)
        for n, nbr, key in zip(edge_to_remove[0],edge_to_remove[1], edge_to_remove[2]):
            unfrozen_graph.nodes[n]['broadcast'] = True
            unfrozen_graph.remove_edge(n, nbr, key=key)

        return unfrozen_graph

    