import networkx as nx
import torch


def normalize(A , symmetric=True):
	# A = A+I
	A = A + torch.eye(A.size(0))
	# 所有节点的度
	d = A.sum(1)
	if symmetric:
		#D = D^-1/2
		D = torch.diag(torch.pow(d , -0.5))
		return D.mm(A).mm(D)
	else:
		# D=D^-1
		D = torch.diag(torch.pow(d,-1))
		return D.mm(A)

G = nx.karate_club_graph()
A = nx.adjacency_matrix(G).todense() # dense matrix? not so freaking good.
#A需要正规化
A_normed = normalize(torch.FloatTensor(A),True)
print(A_normed.shape)

from torch_geometric.nn import GCN
# how to generate graph?
# breakpoint() # 34,34