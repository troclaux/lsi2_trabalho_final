from dataclasses import asdict
from fileinput import filename
from ckan import *
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import networkx as nx
from io import StringIO
import ssl

#read csv from local directory with pandas

datasetQueryResults = get_data_from_repository()
for item in datasetQueryResults:
	try:
		item["csv"] = item["csv"].replace("\r", "")
		#print(item["csv"])
		item["csv"] = StringIO(item["csv"])
		item["csv"] = pd.read_csv(item["csv"], delimiter=";")
	#print("dataquery")
	#print(item["csv"])
	#except OSError: datasetQueryResults.remove(item)
	except ValueError: datasetQueryResults.remove(item)
	except pd.errors.ParserError: datasetQueryResults.remove(item)
	except TypeError: datasetQueryResults.remove(item)
	#print(type(item["csv"]))
	#print(item["csv"])
		


#datas♣♣etQueryResults =[{"name": "dataset1", "csv": dataset1}, {"name": "dataset2", "csv": dataset2}, {"name":"dataset3", "csv": dataset3}]

#function that counts the number of identical columns in two datasets


def countIdenticalColumns(dataset1, dataset2):
	#definir o número de colunas nos 2 datasets
	#comparar as colunas
	identicalColumns = 0
	#print(dataset1)
	columns1 = list(dataset1)
	columns2 = list(dataset2)
	#print("spahgtti")
	#print(columns1)
	#print(columns2)
	for element1 in columns1:
		for element2 in columns2:
			if element1 == element2:
				identicalColumns = identicalColumns + 1
	return identicalColumns


def getRelationshipPercentage(dataset1, dataset2):
	columns1 = list(dataset1)
	columns2 = list(dataset2)
	razao = countIdenticalColumns(dataset1, dataset2) / min(len(columns1), len(columns2))
	#print("tamanhos: "+ len(columns1)+ "," + len(columns2))
	arredondamento = round(razao, 2)
	return arredondamento

#print(countIdenticalColumns(dataset1, dataset2))
#print(getRelationshipPercentage(dataset1, dataset2))



#print(datasetQueryResults)
#create graph


def createGraph(datasets):

	G = nx.Graph()
	i = 0

	#TODO: nomear os nos com os nomes dos datasets

	for dataset in datasets:
		G.add_node(dataset["name"]) #, pos = (i,i)
		i = i+1

	#for node in G:
	#	for neighbor in G:
	#		if node == neighbor:
	#			continue
	#		weight = countIdenticalColumns(node, neighbor)
	#		if weight > 0:
	#			G.add_edge(node, neighbor, weight=weight)

	for node in datasets:
		for neighbor in datasets:
			if node == neighbor:
				continue
			#print("node e vizinho")
			#print(node["csv"])
			#print(neighbor["csv"])
			weight = getRelationshipPercentage(node["csv"], neighbor["csv"])
			if weight > 0:
				G.add_edge(node["name"], neighbor["name"], weight=weight)

	return G

#declaracao do grafo
G = createGraph(datasetQueryResults)
#define posicao dos nos em um grafo circular
pos = nx.circular_layout(G, scale=1, center=None, dim=2)
#constroi conexoes entre os nos
nx.draw(G, pos)
#atribui pesos nas arestas
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
#mostra o grafo na janela
plt.show()

#print(G.nodes)
#print(G.edges)

#print(G.number_of_nodes())
#print(G.number_of_edges())
