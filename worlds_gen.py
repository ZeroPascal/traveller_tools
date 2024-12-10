import json
import random


def roll(dice=1,type=6, mods=0,stat_mod=0,stat_type=0):
    min=dice+mods+stat_mod*stat_type
    if(min<0):
        min=0
    max=dice*type+mods+stat_mod*stat_type
    #print("Rolling",dice,'d',type, "Min",min,"Max",max)
    return(random.randint(min,max))

def getHex(number):
    return f'{number:x}'.upper()
def printClass(name,number,ignoreHex=False):
    if(not ignoreHex):
        number = getHex(number)
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

world['atmosphereClass']= roll(2,6,world['sizeClass']-7)
atmo_table=tables['ATMOSPHERE'][str(world['atmosphereClass'])]
world['atmospherePressure']= round(random.uniform(atmo_table['PRESSURE_MIN'],atmo_table['PRESSURE_MAX']),2)
world['atmopshereType']=atmo_table['COMP']
world['atmopsherTainted']=atmo_table['TAINTED']
printClass("atmosphere",world['atmosphereClass'])
print(' Pressure',world['atmospherePressure'],)
print(' Type:',world['atmopshereType'], '\033[91m Tainted \033[0m' if world['atmopsherTainted'] else '\033[92m Safe \033[0m ')
#Temperature

temp_mod= 0

match world['atmosphereClass']:
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

temp_type= tables['TEMPERATURE'][str(world['temperatureClass'])]
world['temperatureAverage'] = random.randint(temp_type["MIN"],temp_type["MAX"])

printClass('Temperature', world['temperatureClass'])
#print(" Temprate Zone:", world['temperatureType']
print(" Average Temperature:",world['temperatureAverage'])
    
#Hydrographics

min_viable_atmo_tickeness=.5
#Starts at Zero, Changes if Size is greater than 1
world['hydrographicsClass']=0
#Size Exclusion
if(world['sizeClass']>1):
    hydro_mod=-7
    #Atmo Exclusion
    try:
        if([0,1,10,15].index(world['atmosphereClass'])):
            hydro_mod+=-4
    except:
        pass
    #Pressure 
        if(world['atmosphereClass']!=15 or world['atmosphereClass']!=13 and world['atmospherePressure']>=min_viable_atmo_tickeness):
            match world['atmosphereClass']:
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

printClass('Population',world['populationClass'])

world['populationNumber']= 0 if world['populationClass']==0 else random.randint(1,9)*10**world['populationClass']
    
print(' Population',f'{world['populationNumber']:,}')

world['governmentClass']= roll(2,6,world['populationClass']-7)
gov_table = tables['GOVERNMENT'][str(world['governmentClass'])]
printClass('Government',world['governmentClass'])

def getGovType(gov_table):
    gov_type = gov_table['TYPE'].split(',')
    return str(gov_type[len(gov_type)-1])

world['governmentType']= getGovType(gov_table)
print(' Type:',world['governmentType'])

fraction_mod=0
if(world['governmentClass']==0 or world['governmentClass']==7):
    fraction_mod+=1
if(world['governmentClass']>=10):
    fraction_mod+=-1

world['fractionCount']=roll(1,3,fraction_mod)

print(' Fractions',world['fractionCount'])

fractions = []
for f in range(world['fractionCount']):
    fGov = tables['GOVERNMENT'][str(roll(2,6))]
    fractions.append(
        tables['FRACTIONS'][str(roll(2,6))]+" "+getGovType(fGov)

    )
world['fractions']= fractions
for f in fractions:
    print("     ",f)
world['lawClass']=roll(2,6,world['governmentClass']-7)

printClass('Law Level',world['lawClass'])

law_table=tables['LAW'][str(world['lawClass']) if world['lawClass']<=9 else str(9)]
print(' Banned Weaponds:',law_table['WEAPONS'])
print('  Banned Armour:', law_table['ARMOUR'])
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




#Starports
world['starportClass'] = tables['STARPORT_CLASS'][str(roll(2,6,starport_mod))]

#Tech Level
tech_table=tables['TECH_MODS']
tech_mod= 0
for o in tech_table:
    tech_mod+=tech_table[o][world[o]]

world['techClass']=roll(1,6,tech_mod)

#Enviromental Limits
match world['atmosphereClass']:
    case 0,1,10,15:
        if(world['techClass']<8):
            world['techClass']=8 
    case 2,3,13,14:
          if(world['techClass']<5):
            world['techClass']=5
    case 4,7,9:
          if(world['techClass']<3):
            world['techClass']=3
    case 11:
        if(world['techClass']<9):
            world['techClass']=9
    case 12:
        if(world['techClass']<10):
            world['techClass']=10

printClass('Tech Level',world['techClass'])
starport_table=tables['STARPORTS'][str(world['starportClass'])]
printClass('Starport',world['starportClass'],True)


#Starport Faclities
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

#Starport Bases
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

if(4<= world['atmosphereClass'] >=9 and 4<=world['hydrographicsClass']>=8 and 5<=world['populationClass']>=7):
    trade_code.append('Ag')
if(world['sizeClass']==0 and world['atmosphereClass']==0 and world['hydrographicsClass']==0):
    trade_code.append('As')
if(world['populationClass']==0 and world['governmentClass']==0 and world['lawClass']==0):
    trade_code.append('Ba')
if(2<=world['atmosphereClass']>=9 and world['hydrographicsClass']==0):
    trade_code.append('De')
if(world['atmosphereClass']>=10 and world['hydrographicsClass']>=1):
    trade_code.append('Fl')
if(6<=world['sizeClass']>=8 and (5<world['atmosphereClass']>=6 or world['atmosphereClass']==8) and 5<=world['hydrographicsClass']>=7):
    trade_code.append('Ga')
if(world['populationClass']>=9):
    trade_code.append('Hi')
if(world['techClass']>=12):
    trade_code.append('Ht')
##Added temperatureClass <9
if(0<=world['atmosphereClass']>=1 and world['hydrographicsClass']>=1 and world['temperatureClass']<=9):
    trade_code.append('Ic')
if(world['populationClass']>=9 and (0<=world['atmosphereClass']>=2 or world['atmosphereClass']==4 or world['atmosphereClass']==7 or 9<=world['atmosphereClass']>=12)):
    trade_code.append('In')
if(1<=world['populationClass']>=3):
    trade_code.append('Lo')
if(world['techClass']<=5):
    trade_code.append('Lt')
if(0<=world['atmosphereClass']>=3 and 0<=world['hydrographicsClass']>=3 and world['populationClass']>=6):
    trade_code.append('Na')
if(2<=world['atmosphereClass']>=5 and 0<=world['hydrographicsClass']>=3):
    trade_code.append('Po')
if((world['atmosphereClass']==6 or world['atmosphereClass']==8) and 6<=world['populationClass']>=8 and 4<=world['governmentClass']>=9):
    trade_code.append('Ri')
if(world['atmosphereClass']==0):
    trade_code.append('Va')
if((3<=world['atmosphereClass']>=9 or world['atmosphereClass']>=13) and world['hydrographicsClass']>=-0):
    trade_code.append('Wa')

trade_table=tables['TRADE CODES']
world['tradeCodes']= []
for t in trade_code:
    world['tradeCodes'].append(trade_table[t])
print('Trade Codes')
for t in world['tradeCodes']:
    print(' ',t)


print('-------')
code= world['starportClass']+getHex(world['sizeClass'])+getHex(world['atmosphereClass'])+getHex(world['hydrographicsClass'])+getHex(world['populationClass'])+getHex(world['governmentClass'])+getHex(world['lawClass'])+getHex(world['techClass'])
code+='-'

for n in world['starportBases']:
    code+= n[0]

print(code)




