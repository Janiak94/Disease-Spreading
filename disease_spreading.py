import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

beta = 0.6
gamma = 0.01
d = 0.8
length = 100
num_agents = 1000

grid = np.ndarray((length,length), dtype=list,order='C')
for i in range(length):
	for j in range(length):
		grid[i,j] = []
agents = []
susceptible_agents = []
recovered_agents = []
infected_agents = []
fig = plt.figure()
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)
num_infected = []
num_susceptible = []
num_recovered = []
time = []

class Agent:
	def __init__(self,is_infected, xpos = None, ypos = None):
		if is_infected:
			self.is_infected = True
			self.is_recovered = False
			infected_agents.append(self)
			self.xpos = xpos
			self.ypos = ypos
		else:
			self.is_infected = False
			self.is_recovered = False
			susceptible_agents.append(self)
			self.xpos = np.random.randint(0,length-1)
			self.ypos = np.random.randint(0,length-1)
		grid[self.xpos, self.ypos].append(self)

	def move(self):
		if not d >= np.random.rand(1): return
		grid[self.xpos, self.ypos].remove(self)
		has_moved = False
		while not has_moved:
			dx = int(np.random.randint(-1,2,1))
			dy = int(np.random.randint(-1,2,1))
			if np.abs(dx) == np.abs(dy):
				continue
			for a in agents:
				if self.xpos + dx == a.xpos and self.ypos + dy == a.ypos:
					continue
			if self.xpos + dx < length and self.xpos + dx >= 0 and self.ypos + dy < length and self.ypos + dy >= 0:
				self.xpos = self.xpos + dx
				self.ypos = self.ypos + dy
				has_moved = True
		grid[self.xpos, self.ypos].append(self)
		if self.is_infected:
			self.infect()
			self.recover()

	def infect(self):
		for a in grid[self.xpos, self.ypos]:
			if not a.is_recovered and not a.is_infected:
				if beta >= np.random.rand(1):
					a.is_infected = True
					try:
						infected_agents.append(a)
						susceptible_agents.remove(a)
					except ValueError:
						print len(susceptible_agents)
						pass

	def recover(self):
		if gamma >= np.random.rand(1):
			self.is_infected = False
			self.is_recovered = True
			recovered_agents.append(self)
			infected_agents.remove(self)

def animate(i):
	ax1.clear()
	ax2.clear()
	x = []
	y = []
	for a in susceptible_agents:
		x.append(a.xpos)
		y.append(a.ypos)
	ax1.scatter(x,y,c='b')
	x = []
	y = []
	for a in infected_agents:
		x.append(a.xpos)
		y.append(a.ypos)
	ax1.scatter(x,y,c='r')
	x = []
	y = []
	for a in recovered_agents:
		x.append(a.xpos)
		y.append(a.ypos)
	ax1.scatter(x,y,c='g')
	ax1.set_xlim([0,length])
	ax1.set_ylim([0,length])
	for a in agents:
		a.move()
	time.append(i)
	num_susceptible.append(len(susceptible_agents))
	num_infected.append(len(infected_agents))
	num_recovered.append(len(recovered_agents))
	ax2.plot(time,num_susceptible)
	ax2.plot(time,num_infected)
	ax2.plot(time,num_recovered)

def gen():
	i = 0
	while len(infected_agents) > 0:
		i += 1
		yield i



def main():
	for i in range(1,num_agents):
		agents.append(Agent(False))
	agents.append(Agent(True, int(length/2), int(length/2)))

	ani = animation.FuncAnimation(fig, animate,frames=gen, interval=10, repeat=False)
	plt.show()

if __name__ == "__main__": main()