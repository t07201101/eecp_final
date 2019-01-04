from    vpython import*
import numpy as np
G=6.673E-11

#set inital parameters
mass    =   {'jupiter':   1.898E27,    'asteroid': 9.6E20,    'sun':1.99E30}
radius  =   {'jupiter':   6.371E8*100, 'asteroid': 1.317E8*100, 'sun':6.95E8*100}                    
jupiter_orbit =   {'r':   7.78E11,   'v':    1.3E4}
T_jupiter = 2 * pi * sqrt(jupiter_orbit['r']**3/G/mass['sun'])


###### CHOOSE RATIO FOR ORBITAL RESONANCE ######
low_orb_res = 1.9
high_orb_res = 2.1
increment = 0.01
##################################################

resonances = np.arange(low_orb_res, high_orb_res, increment)



# create functions to calculate impact of graviational force by each object
def G_force_jupiter(m,  pos_vec):
    return  -G  *   mass['jupiter'] *   m   /   mag2(pos_vec)   *   norm(pos_vec)
def G_force_asteroid(m,  pos_vec):
    return  -G  *   mass['asteroid'] *   m   /   mag2(pos_vec)   *   norm(pos_vec)
def G_force_sun(m,  pos_vec):
    return  -G  *   mass['sun'] *   m   /   mag2(pos_vec)   *   norm(pos_vec)

class as_obj:
    def __init__(self, pos, radius, m):
        self.pos = pos
        self.radius = radius
        self.m = m
        
# initialise objects
jupiter   =   as_obj(pos  =   vector(jupiter_orbit['r'],0,0),  radius  =   radius['jupiter'], m   =   mass['jupiter'])
jupiter.v =   vector(0,   0,    -jupiter_orbit['v'])

sun   =   as_obj(pos  =   vector(0,0,0),  radius  =   radius['sun'], m   =   mass['sun'])
sun.v =   vector(0,   0,    0)

#initalise graph for orbital radius of asteroid over time
distance = graph(width = 400, align = 'left', xtitle='t',ytitle='x',background=vec(0.5,0.5,0))
x=gdots(color=color.red,graph = distance)

#set time and period parameters
dt=60*60*3

times = 0

for orb_res in resonances:
    # calculate corresponding orbital radius for asteroid
    T_a = T_jupiter/orb_res
    r_a = (G*mass['sun']*T_a**2/(4*pi**2))**(1.0/3)
    asteroid_orbit  =   {'r': r_a  , 'v': 2*pi*r_a/T_a}  
    
    #intialise asteroid
    asteroid    =   as_obj(pos  =   vector(asteroid_orbit['r'],0,0),    radius  =   radius['asteroid'], m   =   mass['asteroid'])
    asteroid.v  =   vector(0,   0,  - asteroid_orbit['v'])

    # reset parameters for while loop
    prev_x = 1
    period = 0
    first = 1
    t = 0
    
    
    while   t < 1.0E9:

        #calculate new acceleration, velocity and position for asteorid
        asteroid.a  =   (G_force_jupiter(asteroid.m, asteroid.pos - jupiter.pos) + G_force_sun(asteroid.m, asteroid.pos - sun.pos))   /   asteroid.m
        asteroid.v  =   asteroid.v  +   asteroid.a  *   dt
        asteroid.pos    =   asteroid.pos    +   asteroid.v  *   dt
    
        #calculate new acceleration, velocity and position for jupiter
        jupiter.a  =   (G_force_asteroid(jupiter.m, asteroid.pos - jupiter.pos) + G_force_sun(jupiter.m, jupiter.pos - sun.pos))    /   jupiter.m
        jupiter.v  =   jupiter.v  +   jupiter.a  *   dt
        jupiter.pos    =   jupiter.pos    +   jupiter.v  *   dt
    
        period += dt
    
        #check if asteroid just passes x-axis, and if so, plot the orbital radius onto the graph
        if asteroid.pos.x >= 0 and prev_x <= 0:
            if first == 0:
                semi_major_axis = (period**2 * G * mass['sun'] / 4 / pi**2)**(1/3)
            period = 0
            first = 0
        prev_x = asteroid.pos.x
    
        t += dt

    x.plot(pos=(orb_res,semi_major_axis))
    times += 1
    print("progress = ", times, "/", len(resonances))
