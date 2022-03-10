from fileinput import filename
from ckan import *
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import networkx as nx

#read csv from local directory with pandas
dataset1 = pd.read_csv("dataset1.csv", delimiter=";")
dataset2 = pd.read_csv("dataset2.csv", delimiter=";")

#function that counts the number of identical columns in two datasets


def countIdenticalColumns(dataset1, dataset2):
	#definir o número de colunas nos 2 datasets
	#comparar as colunas
	identicalColumns = 0
	print(dataset1)
	columns1 = list(dataset1)
	columns2 = list(dataset2)
	for element1 in columns1:
		for element2 in columns2:
			if element1 == element2:
				identicalColumns = identicalColumns + 1
	return identicalColumns


def getRelationshipPercentage(dataset1, dataset2):
	columns1 = list(dataset1)
	columns2 = list(dataset2)
	return countIdenticalColumns(dataset1, dataset2) / min(len(columns1), len(columns2))

#print(countIdenticalColumns(dataset1, dataset2))
#print(getRelationshipPercentage(dataset1, dataset2))


lista = [dataset1, dataset2]

datasetQueryResults = [{"name": "dataset1", "csv": dataset1}, {
	"name": "dataset2", "csv": dataset2}]
#print(datasetQueryResults)
#create graph


def createGraph(datasets):

	G = nx.Graph()
	i = 0

	#TODO: nomear os nos com os nomes dos datasets

	for dataset in datasets:
		G.add_node(dataset["name"])
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
			weight = countIdenticalColumns(node["csv"], neighbor["csv"])
			if weight > 0:
				G.add_edge(node["name"], neighbor["name"], weight=weight)

	return G


G = createGraph(datasetQueryResults)
nx.draw(G)
plt.show()

print(G.nodes)
print(G.edges)

print(G.number_of_nodes())
print(G.number_of_edges())
