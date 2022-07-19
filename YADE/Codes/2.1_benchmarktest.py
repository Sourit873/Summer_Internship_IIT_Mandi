##
## SCRIPT TO TEST IMPACT BETWEEN A SPHERE AND A WALL (MINDLIN - nonlinear elastic model)

## list of engines
O.engines=[
	ForceResetter(),
	InsertionSortCollider([Bo1_Sphere_Aabb(),Bo1_Box_Aabb(),Bo1_Wall_Aabb()]),
	InteractionLoop(
		[Ig2_Sphere_Sphere_ScGeom(),Ig2_Box_Sphere_ScGeom(),Ig2_Wall_Sphere_ScGeom()],
		[Ip2_FrictMat_FrictMat_MindlinPhys()],
		[Law2_ScGeom_MindlinPhys_Mindlin()]
	),
	NewtonIntegrator(damping=0.0,gravity=(15,0,0)),
	###
	### NOTE this extra engine:
	###
	PyRunner(iterPeriod=1,command='myAddPlotData()')
]

## define and append material
mat1=FrictMat(young=7.0e10,poisson=0.30,density=2699,frictionAngle=radians(0),label='Al.alloy')
#mat2=FrictMat(young=4.0e10,poisson=0.35,density=1800,frictionAngle=radians(0),label='Mg.alloy')
O.materials.append(mat1)
#O.materials.append(mat2)

## create a sphere and a wall and append them
## while running simulation of Al alloy, comment on the Mg alloy sphere and vice versa
s0=sphere([0,0,0],0.1,color=[0,1,0],fixed=False,wire=False,material='Al.alloy')
#s0=sphere([0,0,0],0.1,color=[0,1,0],fixed=False,wire=False,material='Mg.alloy')

w=wall([0.2,0,0],axis=0,sense=0,color=[1,0,0])
O.bodies.append(s0)
O.bodies.append(w)

## time step
O.dt=.5*PWaveTimeStep()
O.saveTmp('Mindlin')

from yade import qt
qt.View()
qt.Controller()

############################################
##### now the part pertaining to plots #####
############################################

from yade import plot

def myAddPlotData():
	#if O.interactions[0,1].isReal:
	#	i=O.interactions[0,1]
		## O.interactions[0,1] is not able to detect the interactions between sphere and wall
		## error is throwing here stating "No such interaction" 
		## but while running the test, it is clearly visible that the sphere is colliding with wall and bouncing back
		## rest of the code is working good. PLEASE HELP!!!
		#plot.addData(fn=i.phys.normalForce[0],step=O.iter,un=s0.shape.radius-w.state.pos[0]+s0.state.pos[0],kn=i.phys.kn)
	##data mining
	fn=0-O.forces.f(0)[0]
	un=s0.shape.radius-w.state.pos[0]+s0.state.pos[0]
	if O.forces.f(0)!=Vector3(0,0,0) and un>=0:
		##printing force (fn) and displacement (un) values
		print(f"{fn},{un}")
		##collect these values from the terminal output, create a csv file, plot using MATLAB/Matplotlib
O.run(100,True)

## make one plot: step as function of fn

plot.plots={'un':('fn')}

## this function is called by plotDataCollector
## it should add data with the labels that we will plot
## if a datum is not specified (but exists), it will be NaN and will not be plotted

plot.plot()

