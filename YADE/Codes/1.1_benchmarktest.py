# SCRIPT TO TEST BENCHMARK TEST 1 Material 1
##
##  CONSTITUTIVE LAW: MINDLIN - (nonlinear elastic model)

## list of engines
O.engines=[
	ForceResetter(),
	InsertionSortCollider([Bo1_Sphere_Aabb(),Bo1_Box_Aabb()]),
	InteractionLoop(
		[Ig2_Sphere_Sphere_ScGeom(),Ig2_Box_Sphere_ScGeom()],
		[Ip2_FrictMat_FrictMat_MindlinPhys()],
		[Law2_ScGeom_MindlinPhys_Mindlin()]
	),
	NewtonIntegrator(damping=0.0,gravity=(00,0,0)),
	###
	### NOTE this extra engine:
	###
	### You want snapshot to be taken every 1 sec (realTimeLim) or every 50 iterations (iterLim),
	### whichever comes soones. virtTimeLim attribute is unset, hence virtual time period is not taken into account.
	PyRunner(iterPeriod=1,command='myAddPlotData()')
]

## define and append material
mat1=FrictMat(young=4.80e10,poisson=0.20,density=2800,frictionAngle=radians(19.29),label='Glass')
#mat2=FrictMat(young=2.00e10,poisson=0.25,density=2500,frictionAngle=radians(19.29),label='Limestone')
O.materials.append(mat1)
#O.materials.append(mat2)

## create two spheres and append them

s0=sphere([0.00,0.0,0],0.01,color=[0,1,0],fixed=False,wire=False,material='Glass')
s1=sphere([0.09,0.0,0],0.01,color=[0,2,0],fixed=False,wire=False,material='Glass')
#s0=sphere([0.00,0.1,0],0.01,color=[1,0,0],fixed=False,wire=False,material='Limestone')
#s1=sphere([0.02,0.1,0],0.01,color=[2,0,0],fixed=True,wire=False,material='Limestone')
O.bodies.append(s0)
O.bodies.append(s1)

#Imposing Initial Linear Velocity
O.bodies[0].state.vel=Vector3(10,0,0)
O.bodies[1].state.vel=Vector3(-10,0,0)

## time step
O.dt=.4*PWaveTimeStep()
O.saveTmp('Mindlin')

from yade import qt
qt.View()
qt.Controller()

############################################
##### now the part pertaining to plots #####
############################################

from yade import plot
## make one plot: step as function of fn
plot.plots={'un':('fn')}

## this function is called by plotDataCollector
## it should add data with the labels that we will plot
## if a datum is not specified (but exists), it will be NaN and will not be plotted

def myAddPlotData():
	fn=0-O.forces.f(0)[0]
	un=2*s0.shape.radius-s1.state.pos[0]+s0.state.pos[0]
	if O.forces.f(0)!=Vector3(0,0,0) and un>=0:
		## printing force (fn) and displacement (un) values
		print(f"{fn},{un},{O.time}")
		## collect these values from the terminal output, create a csv file, plot using MATLAB/Matplotlib


### NOTE: IGNORE THE PART UNDER THIS LINE!!!

#O.run(100,True); plot.plot(subPlots=False)

## We will have:
## 1) data in graphs (if you call plot.plot())
## 2) data in file (if you call plot.saveGnuplot('/tmp/a')
## 3) data in memory as plot.data['step'], plot.data['fn'], plot.data['un'], etc. under the labels they were saved
