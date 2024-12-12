import random
import json
import math
def getLuminosity(mass):
    #https://en.wikipedia.org/wiki/Mass%E2%80%93luminosity_relation
    power= 2.3 if mass<0.43 else 4 if mass<2 else 3.5 if mass < 55 else 1
    multiplier = 1.4 if 2<=mass<=55 else 320000 if mass > 55 else .23 if mass<.43 else 1
   # print(multiplier,'*',(mass/1),'^',power)
    return (multiplier*((mass/1)**power))/1

input = open("stars.json", "r")
tables=json.load(input)

def getDistributed(min,max):
    return random.triangular(min,max)

star = {}
prob = 0.0
main_type= random.uniform(0,1)
for star_class in tables['Main Sequence']:
    star_table = tables['Main Sequence'][star_class]
    prob+=star_table["DISTRIBUTION"]
   # print(main_type, 1-star_table["DISTRIBUTION"])
    if(1-star_table["DISTRIBUTION"]>=main_type):
        star['type']= star_class
        break

star_table= tables['Main Sequence'][star['type']]

star['mass']= getDistributed(star_table['MIN_M'],star_table['MAX_M'])
star['radius']= getDistributed(star_table['MIN_R'],star_table['MAX_R'])
star['temp'] =getDistributed(star_table['MIN_T'],star_table['MAX_T'])
star['luminosity']= getLuminosity(star['mass'])
star['lifespan']= round(star['mass']/star['luminosity']*10**10) #Trillions


#Modify the 'base' age of star if temp or radius is in the upper bounds, typical of late-stage
star['age']= 1
if(star['radius']>=star_table['MAX_R']*.9):
    star['age']+= 2
elif(star['radius']>=star_table['MAX_R']*.8):
    star['age']+= 1

if(star['temp']>=star_table['MAX_T']*.9):
    star['age']+= 2
elif(star['temp']>=star_table['MAX_T']*.8):
    star['age']+=1

#The age_distribution here puts the star closer or further from it's average age. 
# While multipling by the 'base' age allows the star to be past its lifespan!

#age_distribution= random.triangular(1,1) #Quick Age for testing
age_distribution= random.triangular(1,4)
minium_star_age=(star['lifespan']/age_distribution)*star['age']
star['age']=  round(random.triangular(minium_star_age,tables['AGE_OF_UNIVERSE']))

#Dead Stars!
def makeNeutron(s):
    s['type']='Neutron'
    s['mass']= star['mass']*0.1 #Blowoff
    s['radius'] =round(s['radius']*0.00001437401179) 
    s['luminosity']=getLuminosity(s['mass'])
    return s

def makeBlackhole(s):
    s['type']='Blackhole'
    s['radius']=0
    return s
#print(star)
if(star['age']>=star['lifespan']):
    age_past_dead = star['age']-star['lifespan']
 #   print(age_past_dead)
    if(star['mass']>20):
        star['type']='Blackhole'
        star['radius']=0
        star['luminosity']=0

    elif(age_past_dead<star['lifespan']*.1):
     #   print('Early Stage Dead')
        if(.33<star['mass']<=8):
            star['type']='Red Giant'
            star['radius']=star['radius']*random.triangular(100,200)
            star['luminosity']=star['luminosity']*random.triangular(100,3000)
            star['temp']=getDistributed(2000,5000)
        elif(8<star['mass']<=20):
            star= makeNeutron(star)
    else:
       # print('Late Stage Dead')
        if(.33<star['mass']<=1.44): #Chandrasekhar limit
            star['type']='White Dwarf'
            star['mass']=star['mass']*.01 #Blowoff
            star['radius']=star['radius']*0.00001437401179
            star['luminosity']=getLuminosity(star['mass'])

        elif (1.44<=star['mass']>8):
            star=makeNeutron(star)
        else:
            star=makeNeutron(star)
            star['type']='Nebula'

#https://pressbooks.cuny.edu/astrobiology/chapter/the-habitable-zone/#:~:text=The%20outer%20boundary%20of%20the,the%20freezing%20point%20of%20water.
star['innerHZ']= 0.95*math.sqrt(star['luminosity']/1)
star['outerHZ']= 1.35*math.sqrt(star['luminosity']/1)


print('\033[1m','Class '+ star['type'], '\033[0m')
print(' Mass',str(round(star['mass'],4))+"M⊙")
print(' Radius',str(round(star['radius'],6))+"R⊙")
print(' Temperature',str(round(star['temp']))+"K")
print(' Luminosity',str(round(star['luminosity'],4))+"L☉")
print(' Age',f'{star["age"]:,}')
print(' Lifespan',f'{star["lifespan"]:,}')
print(' Inner HZ',str(star['innerHZ'])+"AU")
print(' Outer HZ',str(star['outerHZ'])+"AU")

print()
print(star)