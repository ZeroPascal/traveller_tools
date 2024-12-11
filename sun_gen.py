import random
sun ={}
#Mass M

star_types={
    'Red Dwarf': 'Red Dwarf',
    'Main Sequence': 'Main Sequence',
    'Giant': 'Giant',
    'Blackhole': 'Blackhole',
    'Neutron': 'Neutron',
    'Superdense Neutron/ Nebula' : 'Superdense Neutron/ Nebula',
    'White Dwarf': 'White Dwarf',
    'Multibody': 'Multibody'
}

primordial_types={
    0: 'Red Dwarf',
    1: 'Main Sequence',
    2: 'Giant',
    3: 'Multibody'
}
type_distribution= [0,0,0,1,1,1,1,1,2,2,2,3]

sun['type']= primordial_types[type_distribution[random.randrange(0,len(type_distribution)-1)]]

min_mass = .33
max_mass = 200
match sun['type']:
    case 'Red Dwarf':
        min_mass=.1
        max_mass= .33
    case 'Main Sequence':
        min_mass=.34
        max_mass=20
    case 'Giant':
        min_mass=21
        max_mass=200

sun['mass'] =round(random.uniform(min_mass, max_mass),2)

#Age in Millions
sun['age']= random.randint(5,40000)

#Still A Star
if(sun['mass']<=.33):
    sun['type']='Red Dwarf'
elif(sun['age']<=10000):
    sun['type']='Main Sequence'
    if(sun['mass']>20):
        sun['type']='Giant'
elif(20000<=sun['age']<=30000):
    if(.33<sun['mass']>=8):
        sun['type']='Red Giant'
    if(8<sun['mass']<=20):
        sun['type']='Neutron'
    if(sun['mass']>20):
        sun['type']='Blackhole'
elif(sun['age']>=30000):
    if(.33<sun['mass']<=8):
        sun['type']='White Dwarf'
    if(8<=sun['mass']<=20):
        sun['type']='Superdense Neutron/ Nebula'
    if(sun['mass']>20):
        sun['type']='Blackhole'


min_r=.15
max_r=18000

match sun['type']:
    case 'Main Sequence' | 'Giant':
        ratio_r= 3.6
        sun['radius']=round(sun['mass']*ratio_r-(ratio_r-2),2)
    case 'Red Dwarf':
        ratio_r=1.2
        sun['radius']=round(sun['mass']*ratio_r,2)
    case 'Red Giant':
        ratio_r=303.6
        sun['radius']=round(sun['mass']*ratio_r)
    case 'Neutron':
        ratio_r=0
        
    case _:
        print('radius')
    
    
    





print(sun)