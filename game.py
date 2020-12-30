
#colors: pink capitals, (216, 97, 194), purple countries, (112, 0, 169), green selected, (46, 223, 102)

#possibly slow down blocks
#winning screen
#start over loop
 


import graphicsPlus as gr
import random
import collision2 as coll
import math
import time
import physics_objects as pho



#two dimensional list serving as dictionary with all pairs of countries/capitals being used for game (not all countries included)
matches=[["Algeria", "Algiers"],['Argentina', 'Buenos Aires'],['Austria', 'Vienna'],['Bangladesh', 'Dhaka'],['Belarus', 'Minsk'],['Belgium', 'Brussels'],['Bhutan', 'Thimphu'],['Botswana', 'Gaborone'],['Bulgaria', 'Sofia'],['Canada', 'Ottawa'],['China', 'Beijing'],['Colombia', 'Bogota'],['Denmark', 'Copenhagen'],['Egypt', 'Cairo'],['Finland', 'Helsinki'],['France', 'Paris'],['Germany', 'Berlin'],['Greece', 'Athens'],['India', 'New Delhi'],['Indonesia', 'Jakarta'],['Iraq', 'Baghdad'],['Ireland', 'Dublin'],['Israel', 'Jerusalem'],['Jamaica', 'Kingston'],['Japan', 'Tokyo'],['Kazakhstan', 'Astana'],['Kenya', 'Nairobi'],['Latvia', 'Riga'],['Lebanon', 'Beirut'],['Morocco', 'Rabat'],['Nepal', 'Kathmandu'],['Netherlands', 'Amsterdam'],['Pakistan', 'Islamabad'],['Peru', 'Lima'],['Poland', 'Warsaw'],['Qatar', 'Doha'],['Russia', 'Moscow'],['Rwanda', 'Kigali'],['Senegal', 'Dakar'],['Serbia', 'Belgrade'],['Spain', 'Madrid'],['Syria', 'Damascus'],['Taiwan', 'Taipei'],['Tajikistan', 'Dushanbe'],['Thailand', 'Bangkok'],['Tunisia', 'Tunis'],['Turkey', 'Ankara'],['Venezuela','Caracas'],['Vietnam','Hanoi']]


#function including everything that happens in a game, including setup
def playgame(win, level):
	#initializing score count
	score=0
	#making scoreboard in corner
	scoreboard=gr.Text(gr.Point(450,460), "Score: " + str(score))
	scoreboard.setTextColor('white')
	scoreboard.draw(win)
	#barriers surrounding visualization space so blocks can't leave
	barrier1=pho.Block(win,dx=2,dy=50, x0=1,y0=25)
	barrier2=pho.Block(win,dx=2,dy=50, x0=49,y0=25)
	barrier3=pho.Block(win, 50,2, 25,1)
	barrier4=pho.Block(win,50,2,25,49)
	barriers=[barrier1, barrier2, barrier3, barrier4]
	for object in barriers:
		object.setColor((0,0,0))
		object.draw()
	countries=[]
	capitals=[]
	#creating list of six random index values for deciding which country capital pairs to use in the game
	pairs=random.sample(range(len(matches)), 6)
	#creating 6 country rectangle objects and 6 capital rectangle objects
	for i in range(len(pairs)):
		country=pho.Rectangle(win, Text=matches[pairs[i]][0], color=(216, 97, 194), blocktype='country')
		countries.append(country)
		capital=pho.Rectangle(win, Text=matches[pairs[i]][1], color=(112, 0, 169), blocktype='capital')
		capitals.append(capital)
	#giving capitals and countries random positions and velocities and drawing them
	for i in capitals:
		i.setPosition(random.randint(5,45), random.randint(5,45))
		i.setVelocity(random.randint(-10-5*level,1+5*level), random.randint(-10-5*level,10+5*level))
		i.draw()
	for i in countries:
		i.setPosition(random.randint(5,45), random.randint(5,45))
		i.setVelocity(random.randint(-10-10*level,10+10*level), random.randint(-10-10*level,10+10*level))
		i.draw()

	#while loop for continuous motion
	dt=0.02
	while True:
		#checking for collisions between two countries, two capitals,a country and a capital, a country and a barrier, and a capital and a barrier
		for i in countries:
			collided=False
			for j in countries:
				 if i != j and coll.collision(i,j,dt):
				 	collided=True
			for k in capitals:
				 if coll.collision(i,k,dt):
				 	collided=True
			for l in barriers:
				a=coll.collision(i,l,dt)
				if a==True:
					collided=True
			if collided==False:
				i.update(dt)
		for i in capitals:
			collided=False
			for j in countries:
				 if coll.collision(i,j,dt):
				 	collided=True
			for k in capitals:
				 if i !=k and coll.collision(i,k,dt):
				 	collided=True
			for l in barriers:
				a=coll.collision(i,l,dt)
				if a==True:
					collided=True
			if collided==False:
				i.update(dt)
 		
 		#checking if a click hits a country or capital. If it does, setSelected is called.
		click = win.checkMouse()
		if click!=None:
			for i in countries:
				xmin=i.position[0]-0.5*i.width
				xmax=i.position[0]+0.5*i.width
				ymin=i.position[1]-0.5*i.width
				ymax=i.position[1]+0.5*i.width
				if click.getX()>=xmin*i.scale and click.getX()<=xmax*i.scale:
					if click.getY()<=500-(ymin*i.scale) and click.getY()>=500-ymax*i.scale:
						i.setSelected()
 
			for i in capitals:
				xmin=i.position[0]-0.5*i.width
				xmax=i.position[0]+0.5*i.width
				ymin=i.position[1]-0.5*i.width
				ymax=i.position[1]+0.5*i.width
				if click.getX()>=xmin*i.scale and click.getX()<=xmax*i.scale:
					if click.getY()<=500-ymin*i.scale and click.getY()>=500-ymax*i.scale:
						i.setSelected()
		#check if a country and its capital are both selected
		for i in range(6):
			if countries[i].selected==True and capitals[i].selected==True:
				#undraw both
				countries[i].undraw()
				capitals[i].undraw()
				#undo set selected so this isn't true when the while loop runs through again
				capitals[i].selected=False
				countries[i].selected=False
				scoreboard.undraw()
				#increment scoreboard as match was made, and update it
				score+=1
				scoreboard=gr.Text(gr.Point(450,460), "Score: "+ str(score))
				scoreboard.setTextColor('white')
				scoreboard.draw(win)
		#winning the game because all the matches have been made
		if score==6:
			scoreboard.undraw()
			score=0
			endbox=pho.Block(win, 30,30,25,25)
			endbox.setColor((0,0,0))
			endbox.draw()
			endtext=gr.Text(gr.Point(250,250),"""Nice work!
You've learned 6 new capitals.
You're on your way to being 
a master of geography!
			""")
			endtext.setTextColor("white")
			endtext.setSize(18)
			endtext.draw(win)
 			

		if True:
			win.update()
			time.sleep(0.01)
	return

 

#main loop
def main():
	#open window, create box and text for instructions
	win = gr.GraphWin('Game', 500, 500, False) 
	b = gr.Image(gr.Point(250,250),"map.gif")
	b.draw(win)
	level1box=pho.Rectangle(win, x0=15, y0=12, width= 10, height=4, Text="Level 1")
	level2box=pho.Rectangle(win, x0=25, y0=12, width=10, height=4, Text="Level 2")
	level3box=pho.Rectangle(win, x0=35, y0=12, width=10, height=4, Text="Level 3")
	levelboxes=[level1box, level2box, level3box]
	startbox=pho.Block(win, 30,30,25,25)
	startbox.setColor((0,0,0))
	startbox.draw()
	starttext=gr.Text(gr.Point(250,250),"""LEARN THE CAPITALS

choose a level to start""")
	starttext.setTextColor("white")
	starttext.setSize(18)
	starttext.draw(win)
	#choosing level (3 levels, each level the blocks move faster)
	for i in levelboxes:
		i.vis[1].setTextColor('white')
		i.vis[0].setOutline('white')
		i.draw()
	while True:
		#wait for mouse click to start the game
		choice=win.getMouse()
		#check if mouse clicks is in any of the three level boxes and if it is, calls paygame with respective level input
		if choice.getY()<=400 and choice.getY()>=360:
			if choice.getX()>=100 and choice.getX()<=200:
				startbox.undraw()
				starttext.undraw()
				for i in levelboxes:
					i.undraw()
				playgame(win, 1)
			elif choice.getX()>=200 and choice.getX()<=300:
				startbox.undraw()
				starttext.undraw()
				for i in levelboxes:
					i.undraw()
				playgame(win, 2)	
			elif choice.getX()>=300 and choice.getX()<=400:
				startbox.undraw()
				starttext.undraw()
				for i in levelboxes:
					i.undraw()
				playgame(win, 3)
 			 
 
	win.getMouse()
	win.close()
	 


if __name__ == "__main__":
	main()

