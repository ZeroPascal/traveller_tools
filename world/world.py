import json
import random
import sys

def roll(dice=1,type=6, mods=0, min=None):
    roll = mods
    for i in range(dice):
        roll+=random.randint(1,type)
    if(min != None and roll<min):
        roll = min
    return(roll)

def getHex(number):
    return f'{number:x}'.upper()
def getGovType(gov_table):
            gov_type = gov_table['TYPE'].split(',')
            return str(gov_type[len(gov_type)-1])
def printClass(name,number,ignoreHex=False):
    if(not ignoreHex):
        number = getHex(number)
    print('\033[1m'+str(name),'Class',str(number)+"-",'\033[0m')

def printResults(attr, result, mod):
    print('\033[96m',attr, result,'Rolled', result-mod,'Mod',mod,'\033[0m')

try:
    print_results = True if sys.argv[1] else False
except:
    print_results = False
#Import aiRules
rules = open('aiRules.txt',"r").read()
#print(rules)

#Import Data
input = open("worlds.json", "r")
tables=json.load(input)

class World:
    def __init__(self,table=None):
        self._world={}
        if(table):
            self.table=table
        else:
            t = open("worlds.json", "r")
            self.table=json.load(t)
            t.close()
        self.rollSize()
        self.rollAtmosphere()
        self.rollTemerature()
        self.rollHydrographics()
        self.rollPopulation()
        self.rollGoverment()
        self.rollLaws()
        self.rollStarport()
        self.rollTech()
        self.rollStarportStats()
        self.rollBases()
        self.rollTradeCodes()
    @property
    def sizeMass_MAX(self):
        return self.sizeTable['MASS_MAX']
    @property
    def sizeMass_MIN(self):
        return self.sizeTable['MASS_MIN']
    @property
    def sizeMass(self):
        return self._world['sizeMass']
    
    @property 
    def sizeDiameter_MIN(self):
        return self.sizeTable['DIAMETER_MIN']
    @property
    def sizeDiameter_MAX(self):
        return self.sizeTable['DIAMETER_MAX']
    @property
    def sizeDiameter(self):
        return self._world['sizeDiameter']
    @sizeDiameter.setter
    def sizeDiameter(self,newDiameter:int= None):
        if(newDiameter):
            if(self.sizeDiameter_MIN<=newDiameter<=self.sizeDiameter_MAX):
                self._world['sizeDiameter']=newDiameter
            else:
                raise 'Diameter Error'
        else:
            self._world['sizeDiameter']=random.randint(self.sizeDiameter_MIN,self.sizeDiameter_MAX)

    @sizeMass.setter
    def sizeMass(self,newMass:int=None):
        if(newMass):
            if(self.sizeMass_MIN<=newMass <= self.sizeMass_MAX):
                self._world['sizeMass']=newMass
            else:
                raise 'Mass Error'
        else:
            self._world['sizeMass']= round(random.uniform(self.sizeMass_MIN,self.sizeMass_MAX),5)
    @property
    def sizeTable(self):
        return self.table['SIZE'][str(self._world['sizeClass'])]
    
    @property
    def sizeClass(self):
        return self._world['sizeClass']
    

    @sizeClass.setter
    def sizeClass(self,newClass:int):
        self._world['sizeClass']=newClass

    @property 
    def sizeGravity(self):
        return self._world['sizeGravity']

    @sizeGravity.setter
    def sizeGravity(self,gravity:float):
        self._world['sizeGravity']=gravity

    @property
    def sizeType(self):
        return self._world['sizeType']
    
    def rollSize(self, sizeClass:int =None,sizeDiameter:int=None,sizeMass:int=None):

        self.sizeClass =sizeClass if sizeClass else  roll(2,6,-2)
        self.sizeDiameter= sizeDiameter
        self.sizeMass=  sizeMass 
        size_type = self.sizeTable["EXAMPLE"]
        self._world['sizeType'] = size_type[random.randint(0,len(size_type)-1)]
        G=6.6743e-11
        e=(5.97219 * 10**24)

        g_force= (((G*(self.sizeMass*(e)))/(self.sizeDiameter *1000/2)**2))
        self.sizeGravity= round(g_force/9.8,2)
   
    
    @property
    def atmosphereClass(self):
        return self._world['atmosphereClass']
    @atmosphereClass.setter
    def atmosphereClass(self,newClass:int):
        self._world['atmosphereClass']=newClass
    @property
    def atmosphereTable(self):
        return self.table['ATMOSPHERE'][str(self._world['atmosphereClass'])]
    @property
    def atmospherePressure_MIN(self):
        return self.atmosphereTable['PRESSURE_MIN']
    @property
    def atmospherePressure_MAX(self):
        return self.atmosphereTable['PRESSURE_MAX']
    @property
    def atmospherePressure(self):
        return self._world['atmospherePressure']

    @atmospherePressure.setter
    def atmospherePressure(self,newPressure:int=None):
        if(newPressure):
            if(self.atmospherePressure_MIN<=newPressure<=self.atmospherePressure_MAX):
                self._world['atmospherePressure']=newPressure
            else:
                raise 'Pressure Out of Range'
        else:
            self._world['atmospherePressure']=round(random.uniform(self.atmospherePressure_MIN,self.atmospherePressure_MAX),2)
    @property
    def atmosphereType(self):
        return self._world['atmosphereType']
    def rollAtmosphere(self,atmosphereClass:int=None, atmospherePressure:int=None)->int:
        atmo_mod =self._world['sizeClass']-7
        self.atmosphereClass = atmosphereClass if atmosphereClass else roll(2,6,atmo_mod,0)
        self.atmospherePressure = atmospherePressure
        self._world['atmosphereType']=self.atmosphereTable['COMP']
        self._world['atmosphereTainted']=self.atmosphereTable['TAINTED']
        self._world['atmosphereGear']=self.atmosphereTable['GEAR']
        return atmo_mod
    @property
    def temperatureClass(self):
        return self._world['temperatureClass']
    @property
    def temperatureType(self):
        return self.temperatureTable['TYPE']
    @temperatureClass.setter
    def temperatureClass(self,newClass:int):
        self._world['temperatureClass']=newClass
    @property
    def temperatureZone(self):
        return self._world['temperatureZone']
    
    @temperatureZone.setter
    def temperatureZone(self,newZone:str=None):
        self._world['temperatureZone']='Normal'
        if(newZone):
            match newZone:
                case 'Hot' | 'Cold':
                    self._world['temperatureZone']=newZone
                case _:
                    self._world['temperatureZone']='Normal'
        else:
            match random.randint(0,5):
                case 0:
                    self._world['temperatureZone']='Cold'
                case 1:
                    self._world['temperatureZone']='Hot'
                case _:
                    self._world['temperatureZone']='Normal'
    @property
    def temperatureTable(self):
        return self.table['TEMPERATURE'][str(self.temperatureClass)]
    
    @property
    def temperatureAverage_MIN(self):
        return self.temperatureTable['MIN']
    
    @property 
    def temperatureAverage_MAX(self):
        return self.temperatureTable['MAX']
    
    @property 
    def temperatureAverage(self):
        return self._world['temperatureAverage']
    
    @temperatureAverage.setter
    def temperatureAverage(self,newTemp:int=None):
        if(newTemp):
            if(self.temperatureAverage_MIN<=newTemp<=self.temperatureAverage_MAX):
                self._world['temperatureAverage']=newTemp
            else:
                raise 'Temperature Average Out of Range'
        else:
            self._world['temperatureAverage'] = random.randint(self.temperatureAverage_MIN,self.temperatureAverage_MAX)
    def rollTemerature(self,temperatureClass:int=None, temperatureZone:str=None, temperatureAverage:int=None)->int:
            temp_mod= 0
            match self.atmosphereClass:
                case 0 |1 | 6 |7:
                    temp_mod=0
                case 2 |3:
                    temp_mod=-2
                case 4 |5 |14:
                    temp_mod=-1
                case 8 |9:
                    temp_mod=1
                case 10 |13 |15:
                    temp_mod=2
                case 11 |12:
                    temp_mod=6
            self.temperatureZone = temperatureZone
            temp_mod+=-4 if self.temperatureZone=='Cold' else 4 if self.temperatureZone=='Hot' else 0
            self.temperatureClass= temperatureClass if temperatureClass else  roll(2,6,temp_mod)
            self._world['temperatureType']= self.temperatureTable['TYPE']
            self.temperatureAverage= temperatureAverage
            return temp_mod
    @property
    def hydrogrpahicsClass(self):
        return self._world['hydrographicsClass']
    
    @hydrogrpahicsClass.setter
    def hydrogrpahicsClass(self,newClass:int):
        if(newClass>10):
            newClass =10
        self._world['hydrographicsClass'] = newClass
    @property
    def hydrographicsTable(self):
        return self.table['HYDROGRAPHICS'][str(self.hydrogrpahicsClass)]
    @property
    def hydrographicsCoverage_MIN(self):
        return self.hydrographicsTable['MIN']
    @property
    def hydrographicsCoverage_MAX(self):
        return self.hydrographicsTable['MAX']
    
    @property
    def hydrographicsCoverage(self):
        return self._world['hydrographicsCoverage']
    @property
    def hydrographicsDescription(self):
        return self._world['hydrographicsDescription']
    @hydrographicsCoverage.setter
    def hydrographicsCoverage(self,newCoverage:int=None):
        if(newCoverage):
            if(self.hydrographicsCoverage_MIN<=(newCoverage/100)<=self.hydrographicsCoverage_MAX):
                self._world['hydrographicsCoverage']=newCoverage
            else:
                raise 'Hydrographics Coverage out of range'
        else:
            self._world['hydrographicsCoverage'] =round(random.uniform(self.hydrographicsCoverage_MIN,self.hydrographicsCoverage_MAX)*100)

    def rollHydrographics(self,hydrographicsClass:int=None,hydrographicsCoverage:int=None)->int:
            min_viable_atmo_tickeness=2
            #Default Mod
            hydro_mod=-7
            if(self.sizeClass<2):
                #Requires rollMin 0 to take effect
                hydro_mod=-100
            else:
                #Atmo Exclusion
                match self.atmosphereClass:
                    case 0 | 1 | 10 | 11 | 12| 13| 14| 15:
                        hydro_mod+=-4
                    case _:
                        hydro_mod+=self.atmosphereClass
                #Pressure 
                if(self.atmosphereClass!=13 or (self.atmosphereClass !=15 and self.atmospherePressure>=min_viable_atmo_tickeness)):
                        match self.temperatureType:
                            case 'Hot':
                                hydro_mod+=-2
                            case 'Boiling':
                                hydro_mod+=-6
            self.hydrogrpahicsClass= hydrographicsClass if hydrographicsClass else roll(2,6,hydro_mod,0) 
            self.hydrographicsCoverage = hydrographicsCoverage
            self._world['hydrographicsDescription']=self.hydrographicsTable["DESCRIPTION"]
            return hydro_mod 
    @property
    def populationClass(self):
        return self._world['populationClass']
    
    @populationClass.setter
    def populationClass(self,newClass:int):
        self._world['populationClass']=newClass
    @property
    def populationNumber(self):
        return self._world['populationNumber']
    
    @populationNumber.setter
    def populationNumber(self,newNumber:int=None):
        if(newNumber):
            self._world['populationNumber']=newNumber
        else:
            self._world['populationNumber']= 0 if self.populationClass==0 else random.randint(1,9)*10**self.populationClass
    def rollPopulation(self,populationClass:int=None, populationNumber:int=None):
        self.populationClass=populationClass if populationClass else roll(2,6,-2)
        self.populationNumber= populationNumber

    def rollGoverment(self,govermentClass:int=None):
        if(govermentClass):
            self._world['govermentClass']=govermentClass
        else:
            self._world['governmentClass']= roll(2,6,self._world['populationClass']-7)
        if(self._world['governmentClass']<0):
            self._world['governmentClass']=0
        self._world['governmentType']= getGovType(self.table['GOVERNMENT'][str(self._world['governmentClass'])])
        faction_mod=0
        if(self._world['governmentClass']==0 or self._world['governmentClass']==7):
            faction_mod+=1
        if(self._world['governmentClass']>=10):
            faction_mod+=-1
        self._world['factionCount']=roll(1,3,faction_mod)
    
    def rollLaws(self,lawClass:int=None):
        if(lawClass):
              self._world['lawClass']=lawClass
        else:
            self._world['lawClass']=roll(2,6,self._world['governmentClass']-7,0)
    def rollStarport(self,starportClass:int=None):
        if(starportClass):
            self._world['starportClass']=starportClass
        else:
            starport_mod =0
            if self._world['populationClass']==10:
                starport_mod=2
            elif self._world['populationClass']<=2:
                starport_mod=-2
            else:
                match self._world['populationClass']:
                    case 8 |9:
                        starport_mod=1
                    case 3 |4:
                        starport_mod=-1
            self._world['starportClass']=str(roll(2,6,starport_mod))
        self._world['starportClass'] = tables['STARPORT_CLASS'][self._world['starportClass']]
    def rollTech(self,techClass:int=None):
        if(techClass):
            self._world['techClass']=techClass   
        else:
            tech_table=tables['TECH_MODS']
            tech_mod= 0
            try:
                for o in tech_table:
                    tech_mod+=tech_table[o][self._world[o]]
            except Exception as e:
                print(e)


            self._world['techClass']=roll(1,6,tech_mod)

            #Enviromental Limits
            match self._world['atmosphereClass']:
                case 0 | 1 |10 |15:
                    if(self._world['techClass']<8):
                        self._world['techClass']=8 
                case 2| 3 |13 |14:
                    if(self._world['techClass']<5):
                        self._world['techClass']=5
                case 4| 7 |9:
                    if(self._world['techClass']<3):
                        self._world['techClass']=3
                case 11:
                    if(self._world['techClass']<9):
                        self._world['techClass']=9
                case 12:
                    if(self._world['techClass']<10):
                        self._world['techClass']=10
    def rollStarportStats(self):
        starport_table=self.table['STARPORTS'][str(self._world['starportClass'])]
        self._world['starportCost']=roll(1,6,0)*starport_table["COST"]
        self._world['starportFacilites']=starport_table['FACILITIES']

        highportDM= starport_table['HIGHPORT']
        if(highportDM>0):
            highport_mod =0
            if(9<=self._world['techClass']>=11):
                highport_mod+=1
            elif self._world['techClass']>=12:
                highport_mod+=2
            
            if(self._world['populationClass']>=9):
                highport_mod+=1
            if(self._world['populationClass']<=6):
                highport_mod+=-1
            
            if(roll(2,6,highport_mod)>=highportDM):
                self._world['starportFacilites'].append('Highport')
    def rollBases(self):
        starport_table=self.table['STARPORTS'][str(self._world['starportClass'])]
        self._world['starportBases']=[]
        for b in starport_table['BASES']:
            if(starport_table['BASES'][b]>0 and roll(2,6,0)>=starport_table['BASES'][b]):
                self._world['starportBases'].append(b)
    
    def rollTradeCodes(self):
        trade_code =[]
        if(4<= self._world['atmosphereClass']<=9 and 4<=self._world['hydrographicsClass']<=8 and 5<=self._world['populationClass']>=7):
            trade_code.append('Ag')
        if(self._world['sizeClass']==0 and self._world['atmosphereClass']==0 and self._world['hydrographicsClass']==0):
            trade_code.append('As')
        if(self._world['populationClass']==0 and self._world['governmentClass']==0 and self._world['lawClass']==0):
            trade_code.append('Ba')
        if(2<=self._world['atmosphereClass']>=9 and self._world['hydrographicsClass']==0):
            trade_code.append('De')
        if(self._world['atmosphereClass']>=10 and self._world['hydrographicsClass']>=1):
            trade_code.append('Fl')
        if(6<=self._world['sizeClass']>=8 and (5<self._world['atmosphereClass']>=6 or self._world['atmosphereClass']==8) and 5<=self._world['hydrographicsClass']>=7):
            trade_code.append('Ga')
        if(self._world['populationClass']>=9):
            trade_code.append('Hi')
        if(self._world['techClass']>=12):
            trade_code.append('Ht')
        ##Added temperatureClass <9
        if(0<=self._world['atmosphereClass']<=1 and self._world['hydrographicsClass']>=1 and self._world['temperatureClass']<=9):
            trade_code.append('Ic')
        if(self._world['populationClass']<=9 and (0<=self._world['atmosphereClass']>=2 or self._world['atmosphereClass']==4 or self._world['atmosphereClass']==7 or 9<=self._world['atmosphereClass']>=12)):
            trade_code.append('In')
        if(1<=self._world['populationClass']<=3):
            trade_code.append('Lo')
        if(self._world['techClass']<=5):
            trade_code.append('Lt')
        if(0<=self._world['atmosphereClass']>=3 and 0<=self._world['hydrographicsClass']>=3 and self._world['populationClass']>=6):
            trade_code.append('Na')
        if(2<=self._world['atmosphereClass']>=5 and 0<=self._world['hydrographicsClass']>=3):
            trade_code.append('Po')
        if((self._world['atmosphereClass']==6 or self._world['atmosphereClass']==8) and 6<=self._world['populationClass']>=8 and 4<=self._world['governmentClass']>=9):
            trade_code.append('Ri')
        if(self._world['atmosphereClass']==0):
            trade_code.append('Va')
        if((3<=self._world['atmosphereClass']>=9 or self._world['atmosphereClass']>=13) and self._world['hydrographicsClass']>=-0):
            trade_code.append('Wa')

        self._world['tradeCodes']=trade_code


    def printWiki(self):
        nl ="\n"
        string ="{{World|image={{FULLPAGENAME}}.jpg|type="f'{self.sizeType}' +nl
        string+="|starport="f'{self._world['starportClass']}' +nl
        string+="|size="f'{getHex(self.sizeClass)}'+"|sizeD=&nbsp;|diameter="f'{self.sizeDiameter}'+"|mass="f'{self.sizeMass}'+"|gravity="+f'{self.sizeGravity}'+nl
        string+="|atmosphere="f'{getHex(self.atmosphereClass)}'+"|atmosphereD="f'{self.atmosphereType}'+ f'{", Tainted" if self._world['atmosphereTainted'] else ''}'+"|pressure="f'{self.atmospherePressure}'+"|equipment="f'{self._world["atmosphereGear"]}'+nl        
        string+="|temperature="f'{getHex(self.temperatureClass)}'+"|temperatureD="f'{self.temperatureZone}'+" Zone"+"|temperatureAvg="f'{self.temperatureAverage}'+nl
        string+="|hydrographics="f'{getHex(self.hydrogrpahicsClass)}'+"| hydrographicsD="f'{self.hydrographicsDescription}'+" ("f'{self.hydrographicsCoverage}'+"%)"+nl
        string+="|population="f'{getHex(self.populationClass)}'+"|populationD="+f'{self.populationNumber:,}'+nl
        string+="|government="f'{getHex(self._world['governmentClass'])}'+"|law="f'{getHex(self._world['lawClass'])}'+"|tech="f'{getHex(self._world['techClass'])}'+nl

        string+="|facilities="f'{", ".join(self._world['starportFacilites'])}' +nl
        string+="|bases="f'{", ".join(self._world['starportBases'])}'+nl
        tc=""
        for t in self._world['tradeCodes']:
            tc+='[['+t+']] '
        string+="|trade="+tc+nl
        string+="|travel=Green}}"
        return string
def getHex(number):
    return f'{number:x}'.upper()

if __name__=="__main__":
    input = open("worlds.json", "r")
    tables=json.load(input)
    my_world= World(tables)
    
    #my_world.rollSize(sizeClass=10)
    print(my_world.printWiki())