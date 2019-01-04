from    vpython import*
G=6.673E-11

#set inital parameters
mass    =   {'jupiter':   1.898E27,    'asteroid': 9.6E20,    'sun':1.99E30}
radius  =   {'jupiter':   6.371E8*100, 'asteroid': 1.317E8*100, 'sun':6.95E8*100}                    
jupiter_orbit =   {'r':   7.78E11,   'v':    1.3E4}
T_jupiter = 2 * pi * sqrt(jupiter_orbit['r']**3/G/mass['sun'])


###### CHOOSE RATIO FOR ORBITAL RESONANCE ######
orb_res = 7/3
##################################################


# calculate corresponding orbital radius for asteroid
T_a = T_jupiter/orb_res
r_a = (G*mass['sun']*T_a**2/(4*pi**2))**(1.0/3)
asteroid_orbit  =   {'r': r_a  , 'v': 2*pi*r_a/T_a}

# create functions to calculate impact of graviational force by each object
def G_force_jupiter(m,  pos_vec):
    return  -G  *   mass['jupiter'] *   m   /   mag2(pos_vec)   *   norm(pos_vec)
def G_force_asteroid(m,  pos_vec):
    return  -G  *   mass['asteroid'] *   m   /   mag2(pos_vec)   *   norm(pos_vec)
def G_force_sun(m,  pos_vec):
    return  -G  *   mass['sun'] *   m   /   mag2(pos_vec)   *   norm(pos_vec)

## create objects to simulate
#class   as_obj(sphere):
#                def kinetic_energy(self):
#                                return  0.5 *   self.m  *   mag2(self.v)
#                def potential_energy(self):
#                                return  - G *   mass['sun'] *   self.m  /   mag(self.pos)
#scene   =   canvas(width=800,   height=800, background=vector(0.5,0.5,0))
#scene.forward   =   vector(0,   -1, 0)


class as_obj:
    def __init__(self, pos, radius, m):
        self.pos = pos
        self.radius = radius
        self.m = m

# initialise objects
#jupiter   =   as_obj(pos  =   vector(jupiter_orbit['r'],0,0),  radius  =   radius['jupiter'], m   =   mass['jupiter'],  color = color.blue, make_trail  =   False)
jupiter   =   as_obj(pos  =   vector(jupiter_orbit['r'],0,0),  radius  =   radius['jupiter'], m   =   mass['jupiter'])
jupiter.v =   vector(0,   0,    -jupiter_orbit['v'])

#asteroid    =   as_obj(pos  =   vector(cos(theta)*asteroid_orbit['r'],sin(theta)*asteroid_orbit['r'],0),    radius  =   radius['asteroid'], m   =   mass['asteroid'],   color   =   color.white,  make_trail  =   True)
asteroid    =   as_obj(pos  =   vector(asteroid_orbit['r'],0,0),    radius  =   radius['asteroid'], m   =   mass['asteroid'])
asteroid.v  =   vector(0,   0,  - asteroid_orbit['v'])

#scene.lights	=	[]
#sun   =   as_obj(pos  =   vector(0,0,0),  radius  =   radius['sun'], m   =   mass['sun'],	color	=	color.orange,	emissive=True)
sun   =   as_obj(pos  =   vector(0,0,0),  radius  =   radius['sun'], m   =   mass['sun'])
sun.v =   vector(0,   0,    0)
#local_light(pos=vector(0,0,0))
#scene.center = sun.pos

#initalise graph for orbital radius of asteroid over time
distance = graph(width = 400, align = 'left', xtitle='t',ytitle='x',background=vec(0.5,0.5,0))
x=gcurve(color=color.red,graph = distance)

#set time and period parameters
dt=60*60*3
t = 0
prev_y = 1
period = 0
first = 1

while   t < 3.0E10:
    rate(10000)

    #calculate new acceleration, velocity and position for asteorid
    asteroid.a  =   (G_force_jupiter(asteroid.m, asteroid.pos - jupiter.pos) + G_force_sun(asteroid.m, asteroid.pos - sun.pos))   /   asteroid.m
    asteroid.v  =   asteroid.v  +   asteroid.a  *   dt
    asteroid.pos    =   asteroid.pos    +   asteroid.v  *   dt
    
    #calculate new acceleration, velocity and position for jupiter
    jupiter.a  =   (G_force_asteroid(jupiter.m, asteroid.pos - jupiter.pos) + G_force_sun(jupiter.m, jupiter.pos - sun.pos))    /   jupiter.m
    jupiter.v  =   jupiter.v  +   jupiter.a  *   dt
    jupiter.pos    =   jupiter.pos    +   jupiter.v  *   dt
    
    period += dt
    
    
    
    #check if asteroid just passes y-axis, and if so, plot the orbital radius onto the graph
    if asteroid.pos.x >= 0 and prev_y <= 0:
        if first == 0:
            semi_major_axis = (period**2 * G * mass['sun'] / 4 / pi**2)**(1/3)
            x.plot(pos=(t,semi_major_axis))
        period = 0
        first = 0
    prev_y = asteroid.pos.x
    
    t += dt
