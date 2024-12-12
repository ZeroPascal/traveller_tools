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
        main_type= random.uniform(0,1)
       # sun['luminosityClass']='V'
        #https://en.wikipedia.org/wiki/Stellar_classification
        if(main_type<=.76):
            sun['class'] = 'M'
            min_mass=.34
            max_mass=.45
        elif(main_type<=.88):
            sun['class'] = 'K'
            min_mass=.46
            max_mass=.8
        elif(main_type<=.8876):
            sun['class'] = 'G'
            min_mass=.8
            max_mass=1.04
        elif(main_type<=.9176):
            sun['class'] = 'F'
            min_mass=1.04
            max_mass=1.4
        elif(main_type<=.9786):
            sun['class'] = 'A'
            min_mass= 1.4
            max_mass=2.1
        elif(main_type<=.9906):
            sun['class'] = 'B'
            min_mass=2.1
            max_mass=16
        else:
            sun['class'] = 'O'
            min_mass=16
            max_mass=20

    case 'Giant':
        min_mass=21
        max_mass=200

sun['mass'] =round(random.uniform(min_mass, max_mass),2)

#Age in Millions
sun['age']= random.randint(5,11000)

#Still A Star
if(sun['mass']<=.33):
    sun['type']='Red Dwarf'
elif(sun['age']<=10000):
    sun['type']='Main Sequence'
    if(sun['mass']>20):
        sun['type']='Giant'
elif(20000<=sun['age']<=30000):
    if(.33<sun['mass']<=8):
        sun['type']='Red Giant'
    if(8<sun['mass']<=20):
        sun['type']='Neutron'
        sun['mass']= sun['mass']*0.1  ##Blowoff
    if(sun['mass']>20):
        sun['type']='Blackhole'
elif(sun['age']>=30000):
    if(.33<sun['mass']<=1.44): #Chandrasekhar limit
        sun['type']='White Dwarf'
    if(1.44<=sun['mass']>8):
        sun['type']= 'Neutron'
        sun['mass']= sun['mass']*0.1  ##Blowoff
    if(8<=sun['mass']<=20):
        sun['type']='Superdense Neutron/ Nebula'
        sun['mass']= sun['mass']*0.1 ##Blowoff
    if(sun['mass']>20):
        sun['type']='Blackhole'


min_r=.15
max_r=18000

match sun['type']:
    case 'Giant':
        ratio_r= 3.6
        sun['radius']=round(sun['mass']*ratio_r-(ratio_r-2),2)
    case 'Red Dwarf' | 'White Dwarf':
        ratio_r=1.2
        sun['radius']=round(sun['mass']*ratio_r,2)
    case 'Red Giant':
        ratio_r=303.6
        sun['radius']=round(sun['mass']*ratio_r)
    case 'Neutron' | 'Superdense Neutron/ Nebula':
        ratio_r= 0.00001437401179
        sun['radius']=round(sun['mass']*ratio_r,6)
    case 'Blackhole':
        sun['radius'] = 0
    case 'Main Sequence':
        match sun['class']:
            case 'M':
                min_r=.2
                max_r= .7
            case 'K':
                min_r=.701
                max_r=.96
            case 'G':
                min_r=.961
                max_r=1.15
            case 'F':
                min_r=1.151
                max_r=1.4
            case 'A':
                min_r=1.401
                max_r=1.8
            case 'B':
                min_r=1.801
                max_r=6.6
            case 'O':
                min_r=6.601
                max_r=sun['mass']*3.6
        sun['radius']= round(random.uniform(min_r,max_r),4)
    case _:
        print('radius')
    


    
    




print(sun['type'])
try:
    print(' Luminosity Class',sun['class'])
except:
    pass
print(' Mass',str(sun['mass'])+'M')
print(' Radius',str(sun['radius'])+'M')
print(' Age',f'{sun['age']*1000000:,}')