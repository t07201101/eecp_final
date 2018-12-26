from    vpython import*
G=6.673E-11

#set inital parameters
mass    =   {'jupiter':   1.898E27,    'asteroid': 9.6E20,    'sun':1.99E30}
radius  =   {'jupiter':   6.371E8*100, 'asteroid': 1.317E8*10, 'sun':6.95E8*100}                    
jupiter_orbit =   {'r':   7.78E11,   'v':    1.3E4}
T_jupiter = 2 * pi * sqrt(jupiter_orbit['r']**3/G/mass['sun'])


###### CHOOSE NUMBER OF ASTEROIDS ######
N=200
Res_start=1.5
Res_end=5
##################################################

# create functions to calculate impact of graviational force by each object
def G_force_jupiter(m,  pos_vec):
    return  -G  *   mass['jupiter'] *   m   /   mag2(pos_vec)   *   norm(pos_vec)
def G_force_asteroid(m,  pos_vec):
    return  -G  *   mass['asteroid'] *   m   /   mag2(pos_vec)   *   norm(pos_vec)
def G_force_sun(m,  pos_vec):
    return  -G  *   mass['sun'] *   m   /   mag2(pos_vec)   *   norm(pos_vec)

# create objects to simulate
class   as_obj(sphere):
    def kinetic_energy(self):
        return  0.5 *   self.m  *   mag2(self.v)
    def potential_energy(self):
        return  - G *   mass['sun'] *   self.m  /   mag(self.pos)
scene   =   canvas(width=800,   height=800, background=vector(0.5,0.5,0))
scene.forward   =   vector(0,  1, 0)

# calculate corresponding orbital radius for asteroid
orb_res = [Res_start+i*(Res_end-Res_start)/N for i in range(1,N+1)]
asteroid_orbit=[]
for i in orb_res:
    T_a = T_jupiter/i
    r_a = (G*mass['sun']*T_a**2/(4*pi**2))**(1/3)
    asteroid_orbit.append ( {'r': r_a  , 'v':2*pi*r_a/T_a})

# initialise objects
jupiter   =   as_obj(pos  =   vector(jupiter_orbit['r'],0,0),  radius  =   radius['jupiter'], m   =   mass['jupiter'],  color = color.blue, make_trail  =   False)
jupiter.v =   vector(0,   0,    -jupiter_orbit['v'])


asteroids=[as_obj(pos  = vector(asteroid_orbit[i]['r'], 0 ,0) ,v= vector(0, 0,- asteroid_orbit[i]['v']),
                  radius=radius['asteroid'], m=mass['asteroid'],color =color.white,
                  make_trail =True,retain=300,trail_radius=1.317E8/2) for i in range(len(asteroid_orbit))]

sun   =   as_obj(pos  =   vector(0,0,0),  radius  =   radius['sun'], m   =   mass['sun'],	color	=	color.orange,	emissive=True)
sun.v =   vector(0,   0,    0)
local_light(pos=vector(0,0,0))

#initalise graph for orbital radius of asteroid over time
distance = graph(width = 400, align = 'left', xtitle='t',ytitle='x',background=vec(0.5,0.5,0))
x=gcurve(color=color.red,graph = distance)

#set time and period parameters
dt=60*60*12
t = 0
prev_y = 1
first = 1
period = 0

while t<1.0E10:
    #rate(1000)
    
    #calculate new acceleration, velocity and position for asteorid
    for ast in asteroids:
        ast.a  =   (G_force_jupiter(ast.m, ast.pos - jupiter.pos) + G_force_sun(ast.m, ast.pos - sun.pos))   /   ast.m
        ast.v  =   ast.v  +   ast.a  *   dt
        ast.pos    =   ast.pos    +   ast.v  *   dt
    
    #calculate new acceleration, velocity and position for jupiter
    jupiter.a  =    G_force_sun(jupiter.m, jupiter.pos - sun.pos)    /   jupiter.m
    jupiter.v  =   jupiter.v  +   jupiter.a  *   dt
    jupiter.pos    =   jupiter.pos    +   jupiter.v  *   dt
    '''
    period += dt
    
    #check if asteroid just passes y-axis, and if so, plot the orbital radius onto the graph
    if asteroid.pos.x >= 0 and prev_y <= 0:
        if first == 0:
            semi_major_axis = (period**2 * G * mass['sun'] / 4 / pi**2)**(1/3)
            x.plot(pos=(t,semi_major_axis))
        period = 0
        first = 0
    prev_y = asteroid.pos.x
    '''
    t += dt
    
print(f'''Reports:
Time: {t/(60*60*24*365)} years
Number of asteroids: {N}
Ratio of period to Jupiter: From {Res_start} to {Res_end}''')
  
