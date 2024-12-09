import json
import random


def roll(dice=1,type=6, mods=0,stat_mod=0,stat_type=0):
    min=dice+mods+stat_mod*stat_type
    if(min<0):
        min=0
    max=dice*type+mods+stat_mod*stat_type
    #print("Rolling",dice,'d',type, "Min",min,"Max",max)
    return(random.randint(min,max))

def printClass(name,number,ignoreHex=False):
    if(not ignoreHex):
        number = f'{number:x}'.upper()
    print('\033[1m'+str(name),'Class',str(number)+"-",'\033[0m')
#Import Data
input = open("worlds.json", "r")
tables=json.load(input)

world= {}

#Size

world['sizeClass'] = roll(2,6,-2)
size_table=tables['SIZE'][str(world['sizeClass'])]
world['sizeDiameter'] = random.randint(size_table['DIAMETER_MIN'],size_table['DIAMETER_MAX'])
world['sizeMass']=round(random.uniform(size_table['MASS_MIN'],size_table['MASS_MAX']),4)

printClass('Size',world['sizeClass'])
print(" Diameter",str(world['sizeDiameter'] )+" Km")
print(" Mass",str(world['sizeMass'])+' Mₑ')

g=6.6743e-11
e=5.97219 * 10**24
g_force= (((g*(world['sizeMass']*(e)))/(world['sizeDiameter'] *1000/2)**2))
world['sizeGraity']= round(g_force/9.8,2)

print(" Gravity",str(world['sizeGraity'])+' Gs')

#Atmo, Side Dependat 

world['atmospherClass']= roll(2,6,world['sizeClass']-7)
atmo_table=tables['ATMOSPHERE'][str(world['atmospherClass'])]
world['atmospherPressure']= round(random.uniform(atmo_table['PRESSURE_MIN'],atmo_table['PRESSURE_MAX']),2)
world['atmopshereType']=atmo_table['COMP']
world['atmopsherTainted']=atmo_table['TAINTED']
printClass("Atmospher",world['atmospherClass'])
print(' Pressure',world['atmospherPressure'],)
print(' Type:',world['atmopshereType'], '\033[91m Tainted \033[0m' if world['atmopsherTainted'] else '\033[92m Safe \033[0m ')
#Tempature

temp_mod= 0

match world['atmospherClass']:
    case 0,1:
        temp_mod=0
    case 2,3:
        temp_mod=-2
    case 4,5,14:
        temp_mod=-1
    case 6,7:
        temp_mod=0
    case 8,9:
        temp_mod=1
    case 10,13,15:
        temp_mod=2
    case 11,12:
        temp_mod=6

hot_edge = False
cold_edge = False
match random.randint(0,2):
    case 1:
        temp_mod+=4
        hot_edge= True
    case 2:
        temp_mod+=-4
        cold_edge= True
world['temperatureZone']= 'Cold' if cold_edge else 'Hot' if hot_edge else 'Normal'


world['temperatureClass']= roll(2,6,temp_mod)
if(world['temperatureClass']<12):
    temp_table = tables['TEMPERATURE'][str(world['temperatureClass'])]
else:
    temp_table = tables['TEMPERATURE']["12"] 
                                

world['temperatureType']= 'Boiling' if world['temperatureClass']>=12 else temp_table['TYPE']

temp_type= tables['TEMPERATURE']['TYPES'][world['temperatureType']]
world['temperatureAverage'] = random.randint(temp_type["MIN"],temp_type["MAX"])

printClass('Temperature', world['temperatureClass'])
print(" Temprate Zone:", world['temperatureType'])
print(" Average Tempature:",world['temperatureAverage'])
    
#Hydrographics

min_viable_atmo_tickeness=.5
#Starts at Zero, Changes if Size is greater than 1
world['hydrographicsClass']=0
#Size Exclusion
if(world['sizeClass']>1):
    hydro_mod=-7
    #Atmo Exclusion
    try:
        if([0,1,10,15].index(world['atmospherClass'])):
            hydro_mod+=-4
    except:
        pass
    #Pressure 
        if(world['atmospherClass']!=15 or world['atmospherClass']!=13 and world['atmospherPressure']>=min_viable_atmo_tickeness):
            match world['atmospherClass']:
                case 10,11:
                    hydro_mod+=-2
                case 12,13,14,15:
                    hydro_mod+=-6
    world['hydrographicsClass']=roll(2,6,hydro_mod)

hydro_table=tables['HYDROGRAPHICS'][str(world['hydrographicsClass'])]
world['hydrographicsCoverage']= round(random.uniform(hydro_table['MIN'],hydro_table['MAX'])*100)   
printClass('Hydrographics',world['hydrographicsClass'])
print(' Type:',hydro_table["DESCRIPTION"])
print(' Percentage:',f'{world['hydrographicsCoverage']}'+"%")


world['populationClass']=roll(2,6,-2)

printClass('Population Class',world['populationClass'])

world['populationNumber']= 0 if world['populationClass']==0 else random.randint(1,9)*10**world['populationClass']
    
print(' Population',f'{world['populationNumber']:,}')

world['govermentClass']= roll(2,6,world['populationClass']-7)
gov_table = tables['GOVERMENT'][str(world['govermentClass'])]
printClass('Goverment',world['govermentClass'])

def getGovType(gov_table):
    gov_type = gov_table['TYPE'].split(',')
    return str(gov_type[len(gov_type)-1])

world['govermentType']= getGovType(gov_table)
print(' Type:',world['govermentType'])

fraction_mod=0
if(world['govermentClass']==0 or world['govermentClass']==7):
    fraction_mod+=1
if(world['govermentClass']>=10):
    fraction_mod+=-1

world['fractionCount']=roll(1,3,fraction_mod)

print(' Fractions',world['fractionCount'])

fractions = []
for f in range(world['fractionCount']):
    fGov = tables['GOVERMENT'][str(roll(2,6))]
    fractions.append(
        tables['FRACTIONS'][str(roll(2,6))]+" "+getGovType(fGov)

    )
world['fractions']= fractions
for f in fractions:
    print("     ",f)
world['lawClass']=roll(2,6,world['govermentClass']-7)

printClass('Law Level',world['lawClass'])

starport_mod =0
if world['populationClass']==10:
    starport_mod=2
elif world['populationClass']<=2:
    starport_mod=-2
else:
    match world['populationClass']:
        case 8,9:
            starport_mod=1
        case 3,4:
            starport_mod=-1

#Tech Level
world['techClass']=roll(1,6,0)
#Starports
world['starportClass'] = tables['STARPORT_CLASS'][str(roll(2,6,starport_mod))]
starport_table=tables['STARPORTS'][str(world['starportClass'])]
printClass('Starport',world['starportClass'],True)

world['starportCost']=roll(1,6,0)*starport_table["COST"]
world['starportFaclilites']=starport_table['FACILITIES']

highportDM= starport_table['HIGHPORT']
if(highportDM>0):
    highport_mod =0
    if(9<=world['techClass']>=11):
        highport_mod+=1
    elif world['techClass']>=12:
        highport_mod+=2
    
    if(world['populationClass']>=9):
        highport_mod+=1
    if(world['populationClass']<=6):
        highport_mod+=-1
    
    if(roll(2,6,highport_mod)>=highportDM):
        world['starportFaclilites'].append('Highport')

print(" Berthing Cost",world['starportCost'])
print(" Facliites:")
if(len(world['starportFaclilites'])>0):
    for f in world['starportFaclilites']:
        print('     ',f)
else:
    print('     None')

world['starportBases']=[]
for b in starport_table['BASES']:
    if(starport_table['BASES'][b]>0 and roll(2,6,0)>=starport_table['BASES'][b]):
       world['starportBases'].append(b)
print(' Bases:')
if(len(world['starportBases'])>0):
    for b in world['starportBases']:
        print('     ',b)
else:
    print('     None')
trade_code =[]

if(4<= world['atmospherClass'] >=9 and 4<=world['hydrographicsClass']>=8 and 5<=world['populationClass']>=7):
    trade_code.append('Ag')
if(world['sizeClass']==0 and world['atmospherClass']==0 and world['hydrographicsClass']==0):
    trade_code.append('As')
if(world['populationClass']==0 and world['govermentClass']==0 and world['lawClass']==0):
    trade_code.append('Ba')
if(2<=world['atmospherClass']>=9 and world['hydrographicsClass']==0):
    trade_code.append('De')
if(world['atmospherClass']>=10 and world['hydrographicsClass']>=1):
    trade_code.append('Fl')
if(6<=world['sizeClass']>=8 and (5<world['atmospherClass']>=6 or world['atmospherClass']==8) and 5<=world['hydrographicsClass']>=7):
    trade_code.append('Ga')
if(world['populationClass']>=9):
    trade_code.append('Hi')
if(world['techClass']>=12):
    trade_code.append('Ht')
if(0<=world['atmospherClass']>=1 and world['hydrographicsClass']>=1):
    trade_code.append('Ic')
if(world['populationClass']>=9 and (0<=world['atmospherClass']>=2 or world['atmospherClass']==4 or world['atmospherClass']==7 or 9<=world['atmospherClass']>=12)):
    trade_code.append('In')
if(1<=world['populationClass']>=3):
    trade_code.append('Lo')
if(world['techClass']<=5):
    trade_code.append('Lt')
if(0<=world['atmospherClass']>=3 and 0<=world['hydrographicsClass']>=3 and world['populationClass']>=6):
    trade_code.append('Na')
if(2<=world['atmospherClass']>=5 and 0<=world['hydrographicsClass']>=3):
    trade_code.append('Po')
if((world['atmospherClass']==6 or world['atmospherClass']==8) and 6<=world['populationClass']>=8 and 4<=world['govermentClass']>=9):
    trade_code.append('Ri')
if(world['atmospherClass']==0):
    trade_code.append('Va')
if((3<=world['atmospherClass']>=9 or world['atmospherClass']>=13) and world['hydrographicsClass']>=-0):
    trade_code.append('Wa')
    
print('Trade Codes',trade_code)

