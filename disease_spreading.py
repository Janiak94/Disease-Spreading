#!/usr/bin/python

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse as ap

length, num_agents, grid = 0, 0, 0
agents = []
susceptible_agents = []
recovered_agents = []
infected_agents = []
fig = plt.figure(figsize=(14,6),dpi=80, facecolor="w", edgecolor="k")
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)
num_infected = []
num_susceptible = []
num_recovered = []
time = []

class Agent:
	global length, grid
	def __init__(self, d, beta, gamma, is_infected, xpos = None, ypos = None):
		self.d, self.beta, self.gamma = d, beta, gamma
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
		if not self.is_infected and not self.is_recovered:
			grid[self.xpos][self.ypos].append(self)

	def move(self):
		if not self.d >= np.random.rand(1): return
		if not self.is_infected and not self.is_recovered:
			grid[self.xpos][self.ypos].remove(self)
		has_moved = False
		while not has_moved:
			dx = int(np.random.randint(-1,2,1))
			if dx == 0:
				dy = int(np.random.randint(0,2,1))
				if dy == 0:
					dy = -1
				else:
					dy = 1;
			else:
				dy = 0
			if np.abs(dx) == np.abs(dy):
				continue
			if self.xpos + dx < length and self.xpos + dx >= 0 and self.ypos + dy < length and self.ypos + dy >= 0:
				self.xpos = self.xpos + dx
				self.ypos = self.ypos + dy
				has_moved = True
		if not self.is_infected and not self.is_recovered:
			grid[self.xpos][self.ypos].append(self)
		if self.is_infected:
			self.infect()
			self.recover()

	def infect(self):
		for a in grid[self.xpos][self.ypos]:
			if not a.is_recovered and not a.is_infected:
				if self.beta >= np.random.rand(1):
					a.is_infected = True
					infected_agents.append(a)
					susceptible_agents.remove(a)

	def recover(self):
		if self.gamma >= np.random.rand(1):
			self.is_infected = False
			self.is_recovered = True
			recovered_agents.append(self)
			infected_agents.remove(self)

def on_click(event):
	global pause
	pause ^= True
	if pause:
		print "pausing"
	else:
		print "resuming"

def animate(i):
	if pause: return
	fig.canvas.mpl_connect('button_press_event', on_click)
	ax1.clear()
	ax2.clear()
	ax1.set_title("t=%i"%i, fontsize=20)
	ax1.set_xticklabels("")
	ax1.set_yticklabels("")
	ax1.set_xlabel("x", fontsize=30)
	ax1.set_ylabel("y", fontsize=30)
	ax2.set_title(r"d=%.2f, $\gamma=%.2f$, $\beta$=%.2f"%(d,gamma,beta), fontsize=20)
	ax2.set_xlabel("Time steps", fontsize=20)
	ax2.set_ylabel("Number of agents", fontsize=20)
	ax2.tick_params(axis='both', which='major', labelsize=12)
	x, y = [], []
	for a in susceptible_agents:
		x.append(a.xpos)
		y.append(a.ypos)
	ax1.scatter(x,y,c="b")
	x, y = [], []
	for a in infected_agents:
		x.append(a.xpos)
		y.append(a.ypos)
	ax1.scatter(x,y,c="r")
	x, y = [], []
	for a in recovered_agents:
		x.append(a.xpos)
		y.append(a.ypos)
	ax1.scatter(x,y,c="g")
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

def static(num_steps):
	ax1.clear()
	ax2.clear()
	ax1.set_title("t=%i"%num_steps, fontsize=20)
	ax1.set_xticklabels("")
	ax1.set_yticklabels("")
	ax1.set_xlabel("x", fontsize=30)
	ax1.set_ylabel("y", fontsize=30)
	ax2.set_title(r"d=%.2f, $\gamma=%.2f$, $\beta$=%.2f"%(d,gamma,beta), fontsize=20)
	ax2.set_xlabel("Time steps", fontsize=20)
	ax2.set_ylabel("Number of agents", fontsize=20)
	ax2.tick_params(axis='both', which='major', labelsize=12)
	for i in gen(num_steps):
		time.append(i)
		num_susceptible.append(len(susceptible_agents))
		num_infected.append(len(infected_agents))
		num_recovered.append(len(recovered_agents))
		for a in agents:
			a.move()
	x, y = [], []
	for a in susceptible_agents:
		x.append(a.xpos)
		y.append(a.ypos)
	ax1.scatter(x,y,c="b")
	x, y = [], []
	for a in infected_agents:
		x.append(a.xpos)
		y.append(a.ypos)
	ax1.scatter(x,y,c="r")
	x, y = [], []
	for a in recovered_agents:
		x.append(a.xpos)
		y.append(a.ypos)
	ax1.scatter(x,y,c="g")
	ax1.set_xlim([0,length])
	ax1.set_ylim([0,length])
	ax2.plot(time,num_susceptible)
	ax2.plot(time,num_infected)
	ax2.plot(time,num_recovered)

pause = False
def gen(num_steps = 1e6):
	i = 0
	while len(infected_agents) > 0 and i < num_steps:
		if not pause:
			i += 1
		yield i
	yield i
	print "no more infected, or asked number of steps"

def main():
	global length, num_agents, grid
	print "disease spreading, -h or --help for help message"
	parser = ap.ArgumentParser(description="disease spreading simulator")
	parser.add_argument("-d", metavar="d", required=True, help="move probability", type=float)
	parser.add_argument("-g", metavar="gamma", required=True, help="recovery rate", type=float)
	parser.add_argument("-b", metavar="beta", required=True, help="infection rate", type=float)
	parser.add_argument("-N", metavar="agents", required=True, help="number of agents", type=int)
	parser.add_argument("-l", metavar="length", required=True, help="grid size, lxl", type=int)
	parser.add_argument("-n", metavar="num_steps", help="number of time steps, if left out will animate", type=int, default="1000000")
	args = parser.parse_args()
	global d, gamma, beta
	d = args.d
	gamma = args.g
	beta = args.b
	num_steps = args.n
	num_agents = args.N
	length = args.l
	if d < 0 or d > 1:
		print "invalid value of -d arg"
		return
	if gamma < 0 or gamma > 1:
		print "invalid value of -g arg"
		return
	if beta < 0 or beta > 1:
		print "invalid value of -b arg"
		return
	if num_steps < 0:
		print "invalid value of -n arg"
		return
	if num_agents <= 0:
		print "invalid value of -N arg"
		return
	if length <= 0:
		print "invalid value of -l arg"
		return
	grid = [[0 for i in range(length)] for i in range(length)]
	for i in range(length):
		for j in range(length):
			grid[i][j] = []
	for i in range(1,num_agents):
		agents.append(Agent(d, beta, gamma, False))
	agents.append(Agent(d, beta, gamma, True, int(length/2), int(length/2)))

	if num_steps == 1e6:
		ani = animation.FuncAnimation(fig, animate,frames=gen, interval=10, repeat=False)
	else:
		static(num_steps)
	plt.show()

if __name__ == "__main__": main()