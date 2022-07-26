## user input for restitution coefficient
import math
wv=float(input("Angular Velocity: "))

## SCRIPT TO TEST IMPACT BETWEEN TWO SPHERES (MINDLIN - nonlinear elastic model)

## list of engines
O.engines=[
	ForceResetter(),
	InsertionSortCollider([Bo1_Sphere_Aabb(),Bo1_Box_Aabb(),Bo1_Wall_Aabb()]),
	InteractionLoop(
		[Ig2_Sphere_Sphere_ScGeom(),Ig2_Box_Sphere_ScGeom(),Ig2_Wall_Sphere_ScGeom()],
		[Ip2_FrictMat_FrictMat_MindlinPhys()],
		[Law2_ScGeom_MindlinPhys_Mindlin()]
	),
	NewtonIntegrator(damping=0.50,gravity=(0,0,0)),
	###
	### NOTE this extra engine is not required here:
	###
	##PyRunner(iterPeriod=1,command='myAddPlotData()')
]

## define and append material

#mat1_1=FrictMat(young=7.00e10,poisson=0.33,density=2700,frictionAngle=radians(21.801409),label='Al.alloy.1')
mat2_1=FrictMat(young=2.50e09,poisson=0.40,density=1000,frictionAngle=radians(21.801409),label='Nylon.1')
#mat1_2=FrictMat(young=7.00e10,poisson=0.33,density=2700*1000,frictionAngle=radians(21.801409),label='Al.alloy.2')
mat2_2=FrictMat(young=2.50e09,poisson=0.40,density=1000*1000,frictionAngle=radians(21.801409),label='Nylon.2')

#O.materials.append(mat1_1)
O.materials.append(mat2_1)
#O.materials.append(mat1_2)
O.materials.append(mat2_2)

## create a sphere and a wall and append them
## while running simulation of Al alloy, comment on the Nylon spheres and vice versa
#s0=sphere([0,0,1],0.1,color=[1,2,0],fixed=False,wire=False,material='Al.alloy.1')
#s1=sphere([0,0,0],0.5,color=[2,0,1],fixed=False,wire=False,material='Al.alloy.2')
s0=sphere([0,0,1],0.1,color=[1,2,0],fixed=False,wire=False,material='Nylon.1')
s1=sphere([0,0,0],0.5,color=[2,0,1],fixed=False,wire=False,material='Nylon.2')

O.bodies.append(s0)
O.bodies.append(s1)

#Imposing Initial Linear Velocity
O.bodies[0].state.vel=Vector3(0,0,-0.2)
O.bodies[1].state.vel=Vector3(0,0,0)

#Imposing Initial Angular Velocity
O.bodies[0].state.angVel=Vector3(wv,0,0)
O.bodies[1].state.angVel=Vector3(0,0,0)

print(f"Vs/Vn= {O.bodies[0].shape.radius*O.bodies[0].state.angVel[0]/(0-O.bodies[0].state.vel[2])}")

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

#print((O.bodies[0].state.angVel[0]*O.bodies[0].shape.radius+O.bodies[0].state.vel[1])/O.bodies[0].state.vel[2])

