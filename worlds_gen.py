import json
import random



def roll(dice=1,type=6, mods=0,stat_mod=0,stat_type=0):
    min=dice+mods+stat_mod*stat_type
    if(min<0):
        min=0
    max=dice*type+mods+stat_mod*stat_type
    #print("Rolling",dice,'d',type, "Min",min,"Max",max)
    return(random.randint(min,max))

def printClass(name,number):
    print(name,'Class',f'{number:x}'.upper()+"-")
#Import Data
input = open("worlds.json", "r")
tables=json.load(input)

#Size
size_table=tables['SIZE']
size= roll(size_table['ROLL'],size_table['ROLL_TYPE'],size_table['ROLL_MOD'])
size_d= random.randint(size_table[str(size)]['DIAMETER_MIN'],size_table[str(size)]['DIAMETER_MAX'])
printClass('Size',size)
print(" ","Diameter",str(size_d)+"Km")

#Atmo, Side Dependat 
atmo_table=tables['ATMOSPHERE']
atmo= roll(atmo_table['ROLL'],atmo_table['ROLL_TYPE'],atmo_table['ROLL_MOD'],size,atmo_table["ROLL_STAT_MOD_TYPE"])
atmo_pressure= round(random.uniform(atmo_table[str(atmo)]['PRESSURE_MIN'],atmo_table[str(atmo)]['PRESSURE_MAX']),2)
printClass("Atmospher",atmo)
print(' Pressure',atmo_pressure)
print(' Type:',atmo_table[str(atmo)]['COMP'], 'Tainted' if atmo_table[str(atmo)]['TAINTED'] else 'Safe')
#Tempature
temp_mod= 0

match atmo:
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

temp= roll(2,6,temp_mod)
printClass('Temperature', temp)
print(" Temprate Zone:","Hot Zone" if hot_edge else "Cold Zone" if cold_edge else "Normal" )
    
#Hydrographics
hydro_table=tables['HYDROGRAPHICS']
min_viable_atmo_tickeness=.5
#Starts at Zero, Changes if Size is greater than 1
hydro=0
#Size Exclusion
if(size>1):
    hydro_mod=hydro_table["ROLL_MOD"]
    #Atmo Exclusion
    try:
        if([0,1,10,15].index(atmo)):
            hydro_mod+=-4
    except:
        pass
    #Pressure 
        if(atmo!=15 or atmo!=13 and atmo_pressure>=min_viable_atmo_tickeness):
            match temp:
                case 10,11:
                    hydro_mod+=-2
                case 12,13,14,15:
                    hydro_mod+=-6
    hydro=roll(2,6,hydro_mod)

hyrod_percentage= round(random.uniform(hydro_table[str(hydro)]['MIN'],hydro_table[str(hydro)]['MAX'])*100)   
printClass('Hydrographics',hydro)
print(' Percentage',str(hyrod_percentage)+"%")

population=roll(2,6,-2)

printClass('Population Class',population)

goverment= roll(2,6,population-7)

printClass('Goverment',goverment)

fraction_mod=0
if(goverment==0 or goverment==7):
    fraction_mod+=1
if(goverment>=10):
    fraction_mod+=-1

fraction=roll(3,6,fraction_mod)

printClass('Fraction',fraction)

law=roll(2,6,goverment-7)

printClass('Law Level',law)

tech=roll(1,6,0)

trade_code =''

if(4<= atmo >=9 and 4<=hydro>=8 and 5<=population>=7):
    trade_code+='Ag'
if(size==0 and atmo==0 and hydro==0):
    trade_code+='As'
if(population==0 and goverment==0 and law==0):
    trade_code+='Ba'
if(2<=atmo>=9 and hydro==0):
    trade_code+='De'
if(atmo>=10 and hydro>=1):
    trade_code+='Fl'
if(6<=size>=8 and (5<=atmo>=6 or atmo==8) and 5<=hydro>=7):
    trade_code+='Ga'
if(population>=9):
    trade_code+='Hi'
if(tech>=12):
    trade_code+='Ht'
if(0<=atmo>=1 and hydro>=1):
    trade_code+='Ic'
if(population>=9 and (0<=atmo>=2 or atmo==4 or atmo==7 or 9<=atmo>=12)):
    trade_code+='In'
if(1<=population>=3):
    trade_code+='Lo'
if(tech<=5):
    trade_code+='Lt'
if(0<=atmo>=3 and 0<=hydro>=3 and population>=6):
    trade_code+='Na'
if(2<=atmo>=5 and 0<=hydro>=3):
    trade_code+='Po'
if((atmo==6 or atmo==8) and 6<=population>=8 and 4<=goverment>=9):
    trade_code+='Ri'
if(atmo==0):
    trade_code+='Va'
if((3<=atmo>=9 or atmo>=13) and hydro>=-0):
    trade_code+='Wa'
    
print('Trade Code',trade_code)

