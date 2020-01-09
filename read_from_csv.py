import os
import pandas as pd
import networkx as nx
import pickle
from utility import TravianUtility as tu

"""
Lettura da csv delle alleanze e scrittura nel file pickle
"""
tu.communities_csv_to_pickle()
PATH_Allies = 'resources/communities/allies.pickle'
with open(PATH_Allies, 'rb') as handle:
    Day_ALs = pickle.load(handle)

"""
Pulizia messaggi doppi
"""
messages_directory_path = "resources/messages-network-csv/"
messages_directory = os.listdir(messages_directory_path)

count = 1
for file_name in messages_directory:
    lines_seen = set() # holds lines already seen
    if(count < 10):
        outfile = open("resources/messages-network-csv-clean/msg_clean_0"+str(count), "w")
    else:
        outfile = open("resources/messages-network-csv-clean/msg_clean_"+str(count), "w")
    for line in open("resources/messages-network-csv/"+file_name, "r"):
        if line not in lines_seen: # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    count+=1

"""
Lettura da csv dei messaggi e conversione in grafi numerati per giorno
"""
messages_directory_path = "resources/messages-network-csv-clean/"
messages_directory = os.listdir(messages_directory_path)

MGs = []

counter = 1
for file_name, allies_per_day in zip(messages_directory, Day_ALs):
    MG = nx.MultiDiGraph(day=counter)
    network_df = pd.read_csv(messages_directory_path + file_name)
    network_df.columns = ['timestamp', 'sourceid', 'destinationid']
    id_ally = 0
    for ally in allies_per_day:
        for player in ally:
            MG.add_node(str(player), ally=id_ally)
        id_ally += 1
    for index, data in network_df.iterrows():
        MG.add_edge(str(data['sourceid']), str(data['destinationid']), time=str(data['timestamp']))
    MGs.append(MG)
    if counter < 10:
        nx.write_gpickle(MG, "resources/messages/messages_0" + str(counter))
    else:
        nx.write_gpickle(MG, "resources/messages/messages_" + str(counter))
    counter = counter + 1

#counter = 1
for mg in MGs:
    print(mg.graph)


"""
Lettura da csv dei commerci e conversione in grafi numerati per giorno
"""
trades_directory_path = "resources/trades-network-csv/"
trades_directory = os.listdir(trades_directory_path)

MGs = []

counter = 1
for file_name, allies_per_day in zip(trades_directory, Day_ALs):
    MG = nx.MultiDiGraph(day=counter)
    network_df = pd.read_csv(trades_directory_path + file_name)
    network_df.columns = ['timestamp', 'sourceid', 'destinationid']
    id_ally = 0
    for ally in allies_per_day:
        for player in ally:
            MG.add_node(str(player), ally=id_ally)
        id_ally += 1
    for index, data in network_df.iterrows():
        MG.add_edge(str(data['sourceid']), str(data['destinationid']), time=str(data['timestamp']))
    MGs.append(MG)
    if counter < 10:
        nx.write_gpickle(MG, "resources/trades/trades_0" + str(counter))
    else:
        nx.write_gpickle(MG, "resources/trades/trades_" + str(counter))
    counter = counter + 1

#counter = 1
for mg in MGs:
    print(mg.graph)

"""
Lettura da csv dei saccheggi e conversione in grafi numerati per giorno
"""
raids_directory_path = "resources/attacks-network-csv/"
raids_directory = os.listdir(raids_directory_path)

MGs = []

counter = 1
for file_name, allies_per_day in zip(raids_directory, Day_ALs):
    MG = nx.MultiDiGraph(day=counter)
    network_df = pd.read_csv(raids_directory_path + file_name)
    network_df.columns = ['timestamp', 'sourceid', 'destinationid']
    id_ally = 0
    for ally in allies_per_day:
        for player in ally:
            MG.add_node(str(player), ally=id_ally)
        id_ally += 1
    for index, data in network_df.iterrows():
        MG.add_edge(str(data['sourceid']), str(data['destinationid']), time=str(data['timestamp']))
    MGs.append(MG)
    if counter < 10:
        nx.write_gpickle(MG, "resources/attacks/raids_0" + str(counter))
    else:
        nx.write_gpickle(MG, "resources/attacks/raids_" + str(counter))
    counter = counter + 1

#counter = 1
for mg in MGs:
    print(mg.graph)