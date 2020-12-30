#Rosie Ingmann
#November 6th, 2019
#Project 9

import graphicsPlus as gr
import math

#parent class for simulated objects
class Thing:

	#initiate a thing
	def __init__(self, win, the_type, x0=0, y0=0, color=(0,0,0)):
		self.type= the_type
		self.mass= 0
		self.position=[x0, y0]
		self.velocity=[0,0]
		self.acceleration=[0,0]
		self.elasticity=1
		self.scale=10
		self.win= win
		self.vis=[]
		self.selected=False
		self.matched=False
		self.color=color
		self.drawn=False
	
	#get functions for variables	
	def getType(self):
		return self.type
	def getMass(self): 
		return self.mass
	def getPosition(self): 
		return self.position[:]
	def getVelocity(self):
		return self.velocity[:]
	def getAcceleration(self): 
		return self.acceleration[:]
	def getElasticity(self):
		return self.elasticity
	def getScale(self):
		return self.scale
	def getColor(self):
		return self.color
	
	#draw and undraw functions	
	def draw(self):
		for i in self.vis:
			i.draw(self.win)
		self.drawn=True	
	def undraw(self):
		for i in self.vis:
			i.undraw()
		self.drawn=False
	
	#set functions for variables
	def setPosition(self, px, py):
		dx = px - self.position[0]
		dy = py - self.position[1]

		self.position[0]=px
		self.position[1]=py
		
		dx *= self.scale
		dy *= -self.scale
		for i in self.vis:
			i.move(dx, dy)
	def setColor(self, c): #c is an (r, g, b) tuple
		self.color= c
		if c != None:
			for i in self.vis:
				i.setFill(gr.color_rgb(self.color[0], self.color[1], self.color[2]))
	def setType(self, t):
		self.type= t
	def setMass(self, m): 
		self.mass= m
	def setVelocity(self, vx, vy):
		self.velocity[0]= vx
		self.velocity[1]= vy
	def setAcceleration(self, ax, ay): 
		self.acceleration[0]= ax
		self.acceleration[1]= ay
	def setElasticity(self, e):
		self.elasticity= e
	def setScale(self, s):
		self.scale= s

	#update position, velocity, and acceleration of thing
	def update(self, dt):
		self.position[0]+= (self.velocity[0]*dt + 0.5*self.acceleration[0]*dt*dt)
		self.position[1]+= (self.velocity[1]*dt + 0.5*self.acceleration[1]*dt*dt)
		dx= (self.velocity[0]*dt + 0.5*self.acceleration[0]*dt*dt)*self.scale
		dy= -1*(self.velocity[1]*dt + 0.5*self.acceleration[1]*dt*dt)*self.scale
		for i in self.vis:
			i.move(dx, dy)
		self.velocity[0]+=self.acceleration[0]*dt
		self.velocity[1]+=self.acceleration[1]*dt
	



class Ball(Thing):
	#initiate a ball
	def __init__(self, win, radius=1, x0=25, y0=25, color=(0,0,0)):
		Thing.__init__(self, win, "ball", x0, y0, color)
		self.radius=radius
		self.refresh()
		self.setColor(color)
	
	#makes sure the visual representation of the object is updated 
	def refresh(self):
		if self.drawn:
			self.undraw()
		self.vis= [ gr.Circle( gr.Point(self.position[0]*self.scale, 
								 self.win.getHeight()-self.position[1]*self.scale), 
						self.radius * self.scale ) ]
		if self.drawn:
			self.draw()
	
	#get and set radius functions because radius is a variable exclusive to the ball child class
	def getRadius(self):
		return self.radius
	def setRadius(self):
		self.radius=r
		self.refresh()
	
	
	
class Block(Thing):
	#inititates a block object
	def __init__(self, win, dx=2, dy=1, x0=0, y0=0, color=None):
		Thing.__init__(self, win, "block", x0, y0, color)	
		self.width=dx
		self.height=dy 
		self.reshape()
		self.setColor(color)
	#makes sure the visual representation of the object is updated 
	def reshape(self):
		if self.drawn:
			self.undraw()
		self.vis=[gr.Rectangle(gr.Point(self.scale*(self.position[0]-0.5*self.width),
									  self.win.getHeight()-(self.scale*(self.position[1]-0.5*self.height))),
								gr.Point(self.scale*(self.position[0]+0.5*self.width),
									   self.win.getHeight()-(self.scale*(self.position[1]+0.5*self.height))))]
		if self.drawn:
			self.undraw()
	#get and set width and height functions because they are variables exclusive to the block child class
	def getWidth(self):
		return self.width
	def getHeight(self):
		return self.height
	def setWidth(self, w):
		self.width=w
		self.refresh()
	def setHeight(self, h):
		self.height=h
		self.refresh()

class Triangle(Thing):
	#initiates a triangle object
	def __init__(self, win, dx=1, dy=2, x0=0, y0=0, color=None):
		Thing.__init__(self, win, "triangle", x0, y0, color)
		self.base=dx
		self.height=dy
		self.reshape()
		self.setColor(color)
	
	#makes sure the visual representation of the object is updated 
	def reshape(self):
		if self.drawn:
			self.undraw()
		self.vis=[gr.Polygon(gr.Point(self.scale*(self.position[0]-0.5*self.base), self.win.getHeight()-self.scale*(self.position[1]-0.5*self.height)),
							 gr.Point(self.scale*(self.position[0]+0.5*self.base), self.win.getHeight()-self.scale*(self.position[1]-0.5*self.height)), 
							 gr.Point(self.scale*(self.position[0]), self.win.getHeight()-self.scale*(self.position[1]+0.5*self.height)))]
		if self.drawn:
			self.draw()
	#get and set width and height functions because they are variables exclusive to the triangle child class

	def getWidth(self):
		return self.base
	def setWidth(self, w):
		self.base=w
		self.reshape()
	def getHeight(self):
		return self.height
	def setHeight(self, h):
		self.height=h
		self.reshape()



class Tree(Thing):
	#initiates a christmas tree object
	def __init__(self, win, dx=1, dy=1, x0=0, y0=0):
		Thing.__init__(self, win, "tree", x0, y0)
		self.base=dx
		self.height=dy
		self.radius=dy/2
		self.reshape()
		self.setColor()
	#makes sure the visual representation of the object is updated 
	def reshape(self):
		if self.drawn:
			self.undraw()
		self.vis=[gr.Polygon(gr.Point(self.scale*(self.position[0]-0.5*self.base), self.win.getHeight()-self.scale*(self.position[1]-0.5*self.height)),
							 gr.Point(self.scale*(self.position[0]+0.5*self.base), self.win.getHeight()-self.scale*(self.position[1]-0.5*self.height)), 
							 gr.Point(self.scale*(self.position[0]), self.win.getHeight()-self.scale*(self.position[1]+0.5*self.height))), 
				  gr.Polygon(gr.Point(self.scale*(self.position[0]), self.win.getHeight()-self.scale*(self.position[1])),
							 gr.Point(self.scale*(self.position[0]-0.5*self.base), self.win.getHeight()-self.scale*(self.position[1]-self.height)), 
							 gr.Point(self.scale*(self.position[0]+0.5*self.base), self.win.getHeight()-self.scale*(self.position[1]-self.height))), 
				  gr.Rectangle(gr.Point(self.scale*(self.position[0]-(1/6)*self.base),
									  self.win.getHeight()-(self.scale*(self.position[1]-self.height))),
								gr.Point(self.scale*(self.position[0]+(1/6)*self.base),
									   self.win.getHeight()-(self.scale*(self.position[1]-(4/3)*self.height))))] 
		if self.drawn:
			self.draw()
	#get and set radius functions because radius is a variable exclusive to the tree child class
	def getRadius(self):
		return self.radius
	def setRadius(self):
		self.radius=r
		self.refresh()
	#set color function just for christmas tree object because tree has more complicated coloring 
	def setColor(self):
		for i in range(3):
			if i==0 or i==1:
				self.vis[i].setFill(gr.color_rgb(0,71,0))
				self.vis[i].setOutline(gr.color_rgb(0,71,0))
			else:
				self.vis[i].setFill(gr.color_rgb(58, 32, 0))


class Ornament(Thing):
	#initializes an ornament object
	def __init__(self,win, radius=1, x0=0, y0=0, color=None):
		Thing.__init__(self, win, "ornament", x0, y0, color)
		self.radius=radius
		self.reshape()
		self.setColor()
		self.collided=False
	#makes sure the visual representation of the object is updated 
	def reshape(self):
		if self.drawn:
			self.undraw()
		self.vis=[gr.Circle( gr.Point(self.position[0]*self.scale, 
								 self.win.getHeight()-self.position[1]*self.scale), 
						self.radius * self.scale ), gr.Circle( gr.Point(self.position[0]*self.scale, 
								 self.win.getHeight()-(self.position[1]+self.radius+(1/8)*self.radius)*self.scale), 
						(1/8)*self.radius * self.scale ), gr.Line(gr.Point((self.position[0]+self.radius)*self.scale, self.win.getHeight()-(self.position[1]*self.scale)), gr.Point((self.position[0]-self.radius)*self.scale, self.win.getHeight()-(self.position[1]*self.scale)))]
		if self.drawn:
			self.draw()

	#get and set radius functions because radius is a variable exclusive to the ornament child class
	def getRadius(self):
		return self.radius
	def setRadius(self):
		self.radius=r
		self.refresh()
	#set color function just for ornament object because tree has more complicated coloring 
	def setColor(self):
		self.vis[0].setFill(gr.color_rgb(0,121,0))

	def getCollided(self):
		return self.collided
	def setCollided(self, x):
		self.collided= x

	
	
class RotatingBlock(Thing):

	def __init__(self, win, x0=25, y0=25, width=1, height=1, Ax=None, Ay=None):
		Thing.__init__(self, win, "rotating block", x0, y0)
		self.pos=[x0,y0]
		self.anchor=[x0,y0]
		if Ax!=None and Ay!=None:
			self.anchor[0]=Ax
			self.anchor[1]=Ay
		self.width=width
		self.height=height
		self.angle=0.0
		self.rvel=0.0
		self.drawn=False
		self.points=[[-width/2, -height/2], [width/2, -height/2], [width/2, height/2],[-width/2, height/2]]
		self.refresh()
	def refresh(self):
		drawn=self.drawn
		if drawn==True:
			self.vis[0].undraw()
		self.render()
		if drawn==True:
			self.vis[0].draw(self.win)
	def getAngle(self):
		return self.angle
	def setAngle(self, A):
		self.angle=A
		self.refresh()
	def getAnchor(self):
		return self.anchor
	def setAnchor(self, ax, ay):
		self.anchor[0]=ax
		self.anchor[1]=ay
		self.refresh()
	def getRotVelocity(self):
		return self.rvel
	def setRotVelocity(self, r):
		self.rvel=r

	def render(self):
		theta=self.angle*math.pi*(1/180)
		cth=math.cos(theta)
		sth=math.sin(theta)
		pts=[]
		for v in self.points:
			x=v[0]+self.pos[0]-self.anchor[0]
			y=v[1]+self.pos[1]-self.anchor[1]
			xt=x*cth-y*sth
			yt=x*sth+y*cth
			x=xt+self.anchor[0]
			y=yt+self.anchor[1]
			pts.append(gr.Point(self.scale*x, self.win.getHeight()-self.scale*y))
		self.vis=[gr.Polygon(pts[0], pts[1], pts[2], pts[3])]
	def rotate(self, A):
		self.setAngle(self.getAngle()+A)
	def update(self, dt):
		da=self.rvel*dt
		if da!=0:
			self.rotate(da)
		Thing.update(self,dt)



class RotatingTree(Thing):
	def __init__(self, win, x0=25, y0=25, width=1, height=1, Ax=None, Ay=None):
		Thing.__init__(self, win, "rotating tree", x0, y0)
		self.pos=[x0,y0]
		self.anchor=[x0,y0]
		if Ax!=None and Ay!=None:
			self.anchor[0]=Ax
			self.anchor[1]=Ay
		self.width=width
		self.height=height
		self.angle=0.0
		self.rvel=0.0
		self.drawn=False
		self.points=[[-0.5*self.width, -0.5*self.height],
					[ 0.5*self.width,-0.5*self.height],
					[ 0, 0.5*self.height],
					[ 0, 0],
					[ -0.5*self.width, -self.height],
					[0.5*self.width, -self.height]]
		 
		self.vis=[gr.Polygon(gr.Point(self.points[0][0],self.points[0][1]), gr.Point(self.points[1][0],self.points[1][1]), gr.Point(self.points[2][0],self.points[2][1])), 
					gr.Polygon(gr.Point(self.points[3][0],self.points[3][1]), gr.Point(self.points[4][0],self.points[4][1]), gr.Point(self.points[5][0],self.points[5][1]))]
	def draw(self):				 
		if drawn==True:
			for i in self.vis:
				i.undraw()
		self.render()
		if drawn==True:
			for i in self.vis:
				i.draw(self.win)
	def refresh(self):
		drawn=self.drawn
		if drawn==True:
			self.vis[0].undraw()
		self.render()
		if drawn==True:
			self.vis[0].draw(self.win)
	def getAngle(self):
		return self.angle
	def setAngle(self, A):
		self.angle=A
		self.refresh()
	def getAnchor(self):
		return self.anchor
	def setAnchor(self, ax, ay):
		self.anchor[0]=ax
		self.anchor[1]=ay
		self.refresh()
	def getRotVelocity(self):
		return self.rvel
	def setRotVelocity(self, r):
		self.rvel=r
	def render(self):
		theta=self.angle*math.pi*(1/180)
		cth=math.cos(theta)
		sth=math.sin(theta)
		pts=[]
		for v in self.points:
			x=v[0]+self.pos[0]-self.anchor[0]
			y=v[1]+self.pos[1]-self.anchor[1]
			xt=x*cth-y*sth
			yt=x*sth+y*cth
			x=xt+self.anchor[0]
			y=yt+self.anchor[1]
			pts.append(gr.Point(self.scale*x, self.win.getHeight()-self.scale*y))
		self.vis=[gr.Polygon(pts[0], pts[1], pts[2]), gr.Polygon(pts[3],pts[4],pts[5])]#, gr.Polygon(pts[6],pts[7],pts[8],pts[9])]
		for i in range(2):
			self.vis[i].setFill(gr.color_rgb(0,71,0))
			self.vis[i].setOutline(gr.color_rgb(0,71,0))
	def rotate(self, A):
		self.setAngle(self.getAngle()+A)
	def update(self, dt):
		da=self.rvel*dt
		if da!=0:
			self.rotate(da)
		Thing.update(self,dt)
	def draw(self):
		for i in self.vis:
			i.draw(self.win)
		self.drawn=True
	def undraw(self):
		for i in self.vis:
			i.undraw()
		self.drawn=False
	def setColor(self):
		for i in range(2):
			self.vis[i].setFill(gr.color_rgb(0,71,0))
			self.vis[i].setOutline(gr.color_rgb(0,71,0))
			 
class Snowflake(Thing):
	def __init__(self, win, radius=1, x0=0, y0=0):
		Thing.__init__(self, win, "Snowflake", x0, y0)
		self.radius=radius
		self.reshape()
		self.setColor()
	def reshape(self):
		if self.drawn:
			self.undraw()
		self.vis= [ gr.Line( gr.Point(self.position[0]*self.scale, 
								 self.win.getHeight()-(self.position[1]+self.radius)*self.scale), 
							gr.Point(self.position[0]*self.scale, 
								 self.win.getHeight()-(self.position[1]-self.radius)*self.scale)),
					gr.Line( gr.Point((self.position[0]+self.radius)*self.scale, 
								 self.win.getHeight()-self.position[1]*self.scale), 
							gr.Point((self.position[0]-self.radius)*self.scale, 
								 self.win.getHeight()-self.position[1]*self.scale)),
					gr.Line( gr.Point((self.position[0]-self.radius*math.cos(math.pi/8))*self.scale, 
								 self.win.getHeight()-((self.position[1]+self.radius*math.sin(math.pi/8))+self.radius)*self.scale), 
							gr.Point((self.position[0]+self.radius*math.cos(math.pi/8))*self.scale, 
								 self.win.getHeight()-((self.position[1]-self.radius*math.sin(math.pi/8))-self.radius)*self.scale)), 
					gr.Line( gr.Point((self.position[0]+self.radius*math.cos(math.pi/8))*self.scale, 
								 self.win.getHeight()-((self.position[1]+self.radius*math.sin(math.pi/8))+self.radius)*self.scale), 
							gr.Point((self.position[0]-self.radius*math.cos(math.pi/8))*self.scale, 
								 self.win.getHeight()-((self.position[1]-self.radius*math.sin(math.pi/8))-self.radius)*self.scale)), 
					gr.Circle(gr.Point((self.position[0]*self.scale), 
								 (self.win.getHeight()-self.position[1]*self.scale)), 
								0.1*self.radius*self.scale)]
		if self.drawn:
			self.draw()
		self.setColor()
	
	#get and set radius functions because radius is a variable exclusive to the ball child class
	def getRadius(self):
		return self.radius
	def setRadius(self):
		self.radius=r
		self.reshape()
	def setColor(self):
		self.vis[4].setFill("black")


#similar to block class but has text as a second graphics object in its vis
class Rectangle(Thing):
	def __init__(self, win, x0=25, y0=25, width=6, height=3, Text=None, color=None, blocktype=None):
		Thing.__init__(self, win, "rectangle", x0, y0, color)
		self.position=[x0,y0]
		self.radius=2.5
		self.width=width
		self.height=height
		self.text=Text
		self.blocktype=blocktype
		self.setColor(color)
		self.refresh()
	def refresh(self):
		drawn=self.drawn
		if drawn==True:
			for i in self.vis:
				i.undraw()
		self.vis=[gr.Rectangle(gr.Point(self.scale*(self.position[0]-0.5*self.width),
									  self.win.getHeight()-(self.scale*(self.position[1]-0.5*self.height))),
								gr.Point(self.scale*(self.position[0]+0.5*self.width),
									   self.win.getHeight()-(self.scale*(self.position[1]+0.5*self.height)))), gr.Text(gr.Point(self.position[0]*self.scale,self.win.getHeight()-self.position[1]*self.scale), self.text)]
		if self.color!=None:
			self.vis[0].setFill(gr.color_rgb(self.color[0], self.color[1], self.color[2]))
			self.vis[1].setTextColor('white')
		if drawn==True:
			for i in self.vis:
				i.draw(self.win)
	def getRadius(self):
		return self.radius
	def setRadius(self, r):
		self.radius=r
		self.refresh()
	def getText(self):
		return self.text
	def setText(self, t):
		self.text=t
		self.refresh()
	def setColor(self, c):
		self.color=c
		self.refresh()
	#function for when a block is clicked
	def setSelected(self):
		#for when block isn't already selected, changes its color to green
		if self.selected==False:
			self.selected=True
			self.setColor((46, 223, 121))
		#for when block is already selected, changes its color back to its original
		else:
			self.selected=False
			if self.blocktype=='country':
				self.setColor((216, 97, 194))
			elif self.blocktype=='capital':
				self.setColor((112, 0, 169))

		self.refresh()
 
 
 
 

	
	 
	
	
	