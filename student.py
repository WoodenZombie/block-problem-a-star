from blockworld import BlockWorld
import math
from queue import PriorityQueue

class BlockWorldHeuristic(BlockWorld):
	def __init__(self, num_blocks=5, state=None):
		BlockWorld.__init__(self, num_blocks, state)

	def heuristic(self, goal):
		self_state = list(self.get_state())
		goal_state = list(goal.get_state())

		val = 0

		for i, self_item in enumerate(self_state):
			for g, goal_item in enumerate(goal_state):
				min_len = min(len(self_item), len(goal_item))
				for k in range(min_len):
					if self_item[-(k + 1)] == goal_item[-(k + 1)]:
						val -= (k + 1)
					else:
						break
		return val

class AStar():
	def search(self, start, goal):
		open_list = [{"node": start, "action": None, "parent": None, "h": start.heuristic(goal)}] 
		closed_list = []
		current_node = None
		while open_list:
			if current_node == None:
				parent = None
			open_list = sorted(open_list, key=lambda node: node['h']) 
			current_node = open_list.pop(0)
			closed_list.append(current_node)
			if(current_node["node"] == goal):
				path = []
				while(current_node["action"] != None):
					path.append(current_node["action"])
					current_node = current_node["parent"]
				return path[::-1]
			children = current_node["node"].get_neighbors()
			for child in children:
				stop = False
				for node in closed_list:
					if node["node"] == child[1]:
						stop = True
						break
				h = child[1].heuristic(goal)
				for node in open_list:
					if stop == True:
						break
					elif node["node"] == child[1]:
						if current_node["h"] < h:
							stop == True
							break
				if (stop == False):
					open_list.append({"node":child[1], "action":child[0],"parent":current_node,"h":h})

if __name__ == '__main__':
	# Here you can test your algorithm. You can try different N values, e.g. 6, 7.
	N = 5

	start = BlockWorldHeuristic(N)
	goal = BlockWorldHeuristic(N)

	print("Searching for a path:")
	print(f"{start} -> {goal}")
	print()
	#print("Neighbours: " + str(start.get_neighbors()))
	#print("Actions " + str(start.get_actions()))
	astar = AStar()
	path = astar.search(start, goal)

	if path is not None:
		print("Found a path:")
		print(path)

		print("\nHere's how it goes:")

		s = start.clone()
		print(s)

		for a in path:
			s.apply(a)
			print(s)

	else:
		print("No path exists.")

	print("Total expanded nodes:", BlockWorld.expanded)
