## user input for restitution coefficient
import math
en=float(input("en: "))
'''pi=math.pi
l=0-math.log(en)
denom=math.sqrt(pi**2+l**2)
d=l/denom
print(d)'''
dp=1.151-1.151*en
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
	### NOTE we have to change damping values to test the impacts at different restitution coefficients
    NewtonIntegrator(damping=dp,gravity=(0,0,0)),
	###
	### this extra engine is not needed in this test:
	###
	## PyRunner(iterPeriod=1,command='myAddPlotData()')
]

## define and append material
mat1=FrictMat(young=3.8e11,poisson=0.23,density=4000,frictionAngle=radians(0),label='Al.oxide')
#mat2=FrictMat(young=1.0e11,poisson=0.25,density=7000,frictionAngle=radians(0),label='cast iron')
O.materials.append(mat1)
#O.materials.append(mat2)

## create a sphere and a wall and append them
## while running simulation of Al oxide, comment on the cast iron sphere and vice versa
s0=sphere([0,0,0.05],0.0025,color=[0,1,1],fixed=False,wire=False,material='Al.oxide')
#s0=sphere([0,0,0.005],0.0025,color=[0,1,1],fixed=False,wire=False,material='cast iron')

w=wall([0,0,0],axis=2,sense=0,color=[1,1,1])
O.bodies.append(s0)
O.bodies.append(w)

#Imposing Initial Linear Velocity
O.bodies[0].state.vel=Vector3(0,0,-3.9)

#Imposing Initial Angular Velocity
O.bodies[0].state.angVel=Vector3(0,0,0)

## using: "utils.setBodyAngularVelocity"
#utils.setBodyAngularVelocity(0,5*Vector3(1,1,1))
#utils.setBodyAngularVelocity(1,5*Vector3(1,1,1))
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

## time step
O.dt=.5*PWaveTimeStep()
O.saveTmp('Mindlin')

#####################

##to print vel and angvel, write the following commands in the terminal after running the code
#print(O.bodies[0].state.vel)
#print(O.bodies[0].state.angVel)
