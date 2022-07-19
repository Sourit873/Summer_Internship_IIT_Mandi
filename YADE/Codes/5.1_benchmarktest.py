## user input for restitution coefficient
import math
Vt=float(input("Tangential Velocity: "))

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
	NewtonIntegrator(damping=0.0,gravity=(0,0,0)),
	###
	### NOTE this extra engine is not required here:
	###
	##PyRunner(iterPeriod=1,command='myAddPlotData()')
]

## define and append material

mat1=FrictMat(young=2.08e11,poisson=0.3,density=7850,frictionAngle=radians(16.699244),label='Steel')
#mat2=FrictMat(young=1.00e09,poisson=0.4,density=1400,frictionAngle=radians(16.699244),label='Polyethylene')
O.materials.append(mat1)
#O.materials.append(mat2)

## create a sphere and a wall and append them
## while running simulation of Steel, comment on the Polyethylene sphere and vice versa
s0=sphere([0,0,2.00e-04],1.00e-05,color=[1,0,1],fixed=False,wire=False,material='Steel')
#s0=sphere([0,0,2.00e-04],1.00e-05,color=[1,0,1],fixed=False,wire=False,material='Polyethylene')

w=wall([0,0,0],axis=2,sense=0,color=[1,1,0])
O.bodies.append(s0)
O.bodies.append(w)

#Imposing Initial Linear Velocity
O.bodies[0].state.vel=Vector3(0,Vt,-5)
print(Vt/1.5)

## using: "utils.setBodyAngularVelocity"
#utils.setBodyAngularVelocity(0,5*Vector3(1,1,1))
#utils.setBodyAngularVelocity(1,5*Vector3(1,1,1))
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

## time step
O.dt=.5*PWaveTimeStep()
O.saveTmp()

'''from yade import qt
qt.View()
qt.Controller()'''

#####################

##to print desired values, write the following commands in the terminal after running the code
'''print(O.bodies[0].state.vel[1]/(0.3*O.bodies[0].state.vel[2]))
print(O.bodies[0].state.angVel[0]*O.bodies[0].shape.radius/(0.3*O.bodies[0].state.vel[2]))'''
#print(O.bodies[0].state.vel[1]/(0.3*O.bodies[0].state.vel[2]),',',O.bodies[0].state.angVel[0]*O.bodies[0].shape.radius/(0.3*O.bodies[0].state.vel[2]))


