import heapq
import util
import random
import copy
import functools
import heapq
import sys


def memoizePoint(f):
	cache = {}
	def g(e, c):
		i = (e, c)
		if i not in cache:
			cache[i] = f(e, c)
		return cache[i]
	return g

def memoizeIso(f):
	cache = {}
	def g(graph, v):
		i = (tuple(graph.V), tuple(graph.E), v)
		if i not in cache:
			cache[i] = f(graph, v)
		return cache[i]
	return g

def memoize2(f):	
	cache = {}
	def a(graph, player, alpha = -1, beta = 2, maximizingPlayer=1):
		
		
		d = (tuple(graph.V), tuple(graph.E), player, alpha, beta, maximizingPlayer)
		if d not in cache:
			cache[d] = f(graph, player, alpha, beta, maximizingPlayer)
			#print (cache)
		return cache[d]
	return a

def memoize(f):	
		cache = {}
		def g(graph, player, depth = 0, alpha = (10000, ), beta = (-10000, )):			
			d = (tuple(graph.V), tuple(graph.E), depth)
			if d not in cache:
				cache[d] = f(graph, player, depth, alpha, beta)
				#print (cache)
			return cache[d]
		return g

class PercolationPlayer:
	
	

	# `graph` is an instance of a Graph, `player` is an integer (0 or 1).
# Should return a vertex `v` from graph.V where v.color == -1
	def ChooseVertexToColor(graph, player):


		heap = []
		for v in graph.V:
			val1 = 0
			val2 = 0
			val3 = 0
			if v.color == -1:
				for e in util.IncidentEdges(graph, v):
					if e.a.color == player or e.b.color == player:
						val1 += -2
					elif e.a.color == 1 - player or e.b.color == player:
						val1 += -1
					val2 -=1
				if val2 == val1:
					val3 = -1
				

				#g = copyGraph(graph)
				#util.GetVertex(g, v.index).color = player
				#onlyColored(g)
				#size = len(graph.V)
				
				'''if size <= 10:
					w = PercolationPlayer.auxwinnable(graph, player)
				#print(w)
				#print (graph.GetVertex(w[1]))
					val0 = -1 * w[0]			
				else:
					val0 = (1000,)
					for v1 in g.V:
						if v1.color == player:				
							val0 = min(val0, PercolationPlayer.heuristic(g, v1, player))'''				
				heapq.heappush(heap, (0, val3, val1, val2, v.index))
		move = util.GetVertex(graph, heapq.heappop(heap)[4])
		#print(move)
		return move

# `graph` is an instance of a Graph, `player` is an integer (0 or 1).
# Should return a vertex `v` from graph.V where v.color == player
# Right now, this is an pretty inefficient way that finds the best move off what vertexes is connected to.
# Essentially, if a vertex is connected to a Vertex that is the same color as itself, it adds one to the value
# on the other hand, if it connected to a Vertex that is a different color, then its subtracts 1
# Then is finds the bestmove(like if I was finding the biggest from a list)
# Winrate against Random is ~60%.
# ignore the rest for now, it doesn't really do anything yet. 
	def ChooseVertexToRemove(graph, player):
		size = len(graph.V)
		if size <= 10:
			w = PercolationPlayer.auxwinnable(graph, player)
		#print(w)
		#print (graph.GetVertex(w[1]))
			return util.GetVertex(graph, w[1])
		elif size <= 18:
			m = PercolationPlayer.vremove(graph, player)
			return util.GetVertex(graph, m[1].index)
		else:
			move = (10000, )
			for v in graph.V:
				if v.color == player:
					

					move = min(move, PercolationPlayer.heuristic(graph, v, player))
			return util.GetVertex(graph, move[4])
			
		
			
	@memoize
	def vremove(graph, player, depth = 0, alpha = (10000, ), beta = (-10000, )):
		#to do

		if PercolationPlayer.isWin1(graph, player) == -1 and not depth % 2:
			return (2, 0, 0, 0), None
		elif PercolationPlayer.isWin1(graph, 1 - player) == -1 and depth % 2:
			return (-2, 0, 0, 0), None	
		elif depth == 2:
			move = (10000, )
			for v in graph.V:
				if v.color == player:
					move = min(move, PercolationPlayer.heuristic2(graph, v, player))
			return move, None
		
		if not depth % 2:
			
			
			best = (10000, )
			vmax = None
					
			for v in graph.V:
				if v.color == player:
					g = copyGraph(graph)
					PercolationPlayer.Percolate(g, v)
					val = PercolationPlayer.vremove(g, player, depth + 1, alpha, beta)[0]
					if val < best:
						best = val
						vmax = v

					if alpha < best:
						alpha = best

					if beta >= alpha:
						break
			return best, vmax
		
		else:

			best = (-10000, )
			vmin = None 
			for v in graph.V:
				if v.color != player:
					g = copyGraph(graph)
					PercolationPlayer.Percolate(g, v)
					val = PercolationPlayer.vremove(g, player, depth + 1, alpha, beta)[0]
					if val > best:
						best = val
						vmax = v
					
					if beta > best:
						beta = best

					if beta >= alpha:
						break
			
			return best, vmin





	@memoize2
	def auxwinnable(graph, player, alpha = -1, beta = 2, maximizingPlayer = 1):
		if PercolationPlayer.isWin(graph, player, maximizingPlayer):
			#print (1 - maximizingPlayer, graph)
			return 1 - maximizingPlayer, None
		vHeap = PercolationPlayer.orderV(graph, player, maximizingPlayer)
		#print (vHeap)
		if maximizingPlayer:
			
			
			best = -1
			vmax = None
			
			while vHeap:

				v = heapq.heappop(vHeap)[4]
				g = copyGraph(graph)
				PercolationPlayer.Percolate(g, util.GetVertex(g, v))
				val = PercolationPlayer.auxwinnable(g, player, alpha, beta, 0)[0]

				if val > best:
					best = val
					vmax = v

				if alpha > best:
					alpha = best

				if beta <= alpha:
					break	

			return best, vmax

		else:

			
			best = 2
			vmin = None

			while vHeap:
				
				v = heapq.heappop(vHeap)
				if len(v) == 5:
					v = v[4]
				else:
					print("error")
					print(v)
				g = copyGraph(graph)
				PercolationPlayer.Percolate(g, util.GetVertex(g, v))
				val = PercolationPlayer.auxwinnable(g, player, alpha, beta, 1)[0]

				if val < best:
					best = val
					vmin = v

				if beta < best:
					beta = best

				if beta <= alpha:
					break

			
			return best, vmin

	@memoize2
	def auxwinnable2(graph, player, alpha = -1, beta = 2, maximizingPlayer = 1):
		if PercolationPlayer.isWin(graph, player, maximizingPlayer):
			return 1 - maximizingPlayer, None
		
		if maximizingPlayer:
						
			best = -1
			vmax = None
			
			for v in graph.V:
				if v.color == player:
					g = copyGraph(graph)
					PercolationPlayer.Percolate(g, util.GetVertex(g, v))
					val = PercolationPlayer.auxwinnable2(g, player, alpha, beta, 0)[0]

					if val > best:
						best = val
						vmax = v

					if alpha > best:
						alpha = best

					if beta <= alpha:
						break	

			return best, vmax

		else:
			
			
			best = 2
			vmin = None

			for v in graph.V:
				if v.color != player:
					g = copyGraph(graph)
					PercolationPlayer.Percolate(g, util.GetVertex(g, v))
					val = PercolationPlayer.auxwinnable2(g, player, alpha, beta, 1)[0]

					if val < best:
						best = val
						vmin = v

					if beta < best:
						beta = best

					if beta <= alpha:
						break

			
			return best, vmin

	#@functools.lru_cache(maxsize=None)
	#@memoize
	def winnable(graph, alpha = (-1, None), beta = (2, None), v = None, maximizingPlayer = 0):
		if PercolationPlayer.isWin2(graph, maximizingPlayer):
			#print("v: " + str(v))
			return (1 - maximizingPlayer, v)

		if maximizingPlayer:

			best = (-1, None)
			
			for v in graph.V:
				if v.color == maximizingPlayer:
					g = copyGraph(graph)
					g.Percolate(v)
					val = PercolationPlayer.winnable(g, alpha, beta, v, 0)
					if val[0] > best[0]:
						best = val

					if alpha[0] > best[0]:
						alpha = best

					if beta[0] <= alpha[0]:
						break		

			return best

		else:

			best = (2, None)

			for v in graph.V:
				if v.color == maximizingPlayer:
					g = copyGraph(graph)
					g.Percolate(v)
					val = PercolationPlayer.winnable(g, alpha, beta, v, 1)

					if val[0] < best[0]:
						best = val

					if beta[0] < best[0]:
						beta = best

					if beta[0] <= alpha[0]:
						break

			
			return best
	def orderV(graph, player, maximizingPlayer):
		if maximizingPlayer:
			p = player
		else:
			p = 1 - player

		vertexHeap = [] 
		for v in graph.V:
			if v.color == p: 
				heapq.heappush(vertexHeap, PercolationPlayer.heuristic(graph, v, p))
		#print(vertexHeap)
		return vertexHeap
	def heuristic(graph, v, player):

		g = copyGraph(graph)
		PercolationPlayer.Percolate(g, v)
		val0 = PercolationPlayer.isWin1(g, 1 - player)
		if val0 == -1:
			return (val0, 0, 0, 0, v.index)
		
		val1 = 0
		val2 = 0
		val3 = 0

		
		seenV = set([])

		c = v.color
		for e in graph.E:
			va = e.a
			vb = e.b
			if va == v or vb == v:
				val3 += 1
				val2 += PercolationPlayer.point(e, c)
			if va not in seenV:
				seenV.add(va)
				if va.color == player:
					val1 -=1
				else:
					val1 +=1
			if vb not in seenV:
				seenV.add(vb)
				if vb.color == player:
					val1 -=1
				else:
					val1 +=1

		return (val0, val1, val2, val3, v.index)

	def heuristic2(graph, v, player):

		g = copyGraph(graph)
		PercolationPlayer.Percolate(g, v)
		val0 = PercolationPlayer.isWin1(g, 1 - player)
		if val0 == -1:
			return (val0, )
		
		val1 = 0
		val2 = 0
		val3 = 0

		
		seenV = set([])

		c = v.color
		for e in graph.E:
			va = e.a
			vb = e.b
			if va == v or vb == v:
				val3 += 1
				val2 += PercolationPlayer.point(e, c)
			if va not in seenV:
				seenV.add(va)
				if va.color == player:
					val1 -=1
				else:
					val1 +=1
			if vb not in seenV:
				seenV.add(vb)
				if vb.color == player:
					val1 -=1
				else:
					val1 +=1

		return (val0, val1, val2, val3)
	
	@memoizePoint
	def point(e, c):
		if e.a.color == c and e.b.color == c:
			return 1
		else:
			return -1 


		return vertexHeap
	def isWin(graph, player, maximizingPlayer):

		if maximizingPlayer:
			p = player
		else:
			p = 1 - player

		return PercolationPlayer.isWin2(graph, p) 


		

	def isWin1(graph, player):
		for v in graph.V:
			if v.color == player:
				return 0
		return -1 

	def isWin2(graph, player):

		for v in graph.V:
			if v.color == player:
				return False
		return True

	@memoizeIso
	def isIsolated(graph, v):
		for e in graph.E:
			if e.a == v or e.b == v:
				return False
		return True

	
	def Percolate(graph, v):
		# Get attached edges to this vertex, remove them.

		VtoCheck = set([])
		E1 = copy.copy(graph.E)
		for e in E1:
			v1 = e.a
			v2 = e.b
			if v1 == v:
				graph.E.remove(e)
				VtoCheck.add(v2)
			elif v2 == v:
				graph.E.remove(e)
				VtoCheck.add(v1)

		for v1 in VtoCheck:
			if PercolationPlayer.isIsolated(graph, v1):
				graph.V.remove(v1)
        # Remove this vertex.
		graph.V.remove(v)

	


def onlyColored(graph):
	E1 = copy.copy(graph.E)
	for e in E1:
		eac = e.a.color == -1
		ebc = e.b.color == -1
		if eac or ebc:
			graph.E.remove(e)
		if eac:
			if e.a in graph.V:
				graph.V.remove(e.a)
		if ebc:
			if e.b in graph.V:
				graph.V.remove(e.b)


	


def copyGraph(graph):
	Vs = copy.copy(graph.V)
	Es = copy.copy(graph.E)
	return util.Graph(Vs, Es)
	



# Feel free to put any personal driver code here.
def main():
	pass





if __name__ == "__main__":
    main()
