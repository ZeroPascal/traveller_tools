import unittest
from world import World

class TestWorld(unittest.TestCase):
    def setUp(self):
        self.world=World()
    def test_size(self):
        #Earth Gravity
        self.world.rollSize(sizeClass=8,sizeDiameter=12725,sizeMass=1)
        self.assertEqual(1,self.world.sizeGravity,"Gravity Calculation Failed")

    def test_atmosphere(self):
        self.world.sizeClass=0
        self.assertEqual(-7,self.world.rollAtmosphere(),"Atmosphere Mod Incorrect")
    def test_temerature(self):
        mods = [0,1,6,7]
        for m in mods:
            self.world.atmosphereClass=m
            self.assertEqual(0,self.world.rollTemerature(temperatureZone='Normal'),"Temp Mod Incorrect")
        mods = [2,3]
        for m in mods:
            self.world.atmosphereClass=m
            self.assertEqual(2,self.world.rollTemerature(temperatureZone='Hot'),"Temp Mod Incorrect")
        mods = [4,5,14]
        for m in mods:
            self.world.atmosphereClass=m
            self.assertEqual(-5,self.world.rollTemerature(temperatureZone='Cold'),"Temp Mod Incorrect")
        mods = [8,9]
        for m in mods:
            self.world.atmosphereClass=m
            self.assertEqual(1,self.world.rollTemerature(temperatureZone='Normal'),"Temp Mod Incorrect")
        mods = [10,13,15]
        for m in mods:
            self.world.atmosphereClass=m
            self.assertEqual(2,self.world.rollTemerature(temperatureZone='Normal'),"Temp Mod Incorrect")
        mods = [11,12]
        for m in mods:
            self.world.atmosphereClass=m
            self.assertEqual(6,self.world.rollTemerature(temperatureZone='Normal'),"Temp Mod Incorrect")
    def test_hydrographics(self):
        #Size 0 or 1 Hydrographics = 0
        for s in range(2):
            self.world.sizeClass=s
            self.world.rollHydrographics()
            self.assertEqual(0,self.world.hydrogrpahicsClass,"zero Size World Gives wrong Hydrographics")
        self.world.sizeClass=2
        atmo=[0,1,10,11,12,14,13,15]
        for a in range(16):
            self.world.atmosphereClass=a
            #Assures Not Hot or Boiling
            self.world.temperatureClass= 0
            if(a in atmo):
                self.assertEqual(-11,self.world.rollHydrographics(),'Atmosphere Exemptions Incorred')
            else:
                self.assertEqual(-7+a,self.world.rollHydrographics(), 'Hydro Mod Inccorect with Atmo '+f'{a}')
        self.world.atmosphereClass=9
        self.world.temperatureClass=12 #Hot
        self.assertEqual(0,self.world.rollHydrographics(),"Hydro Mod Inncorrect for "+f'{self.world.temperatureType}'+' Zone, Atmo '+f'{self.world.atmosphereClass}'+' Pressure '+f'{self.world.atmospherePressure}')
        self.world.temperatureClass=20 #Boiling
        self.assertEqual(-4,self.world.rollHydrographics(),"Hydro Mod Inncorrect for "+f'{self.world.temperatureType}'+' Zone, Atmo '+f'{self.world.atmosphereClass}'+' Pressure '+f'{self.world.atmospherePressure}')
        self.world.atmosphereClass=15
        self.world.atmospherePressure=self.world.atmospherePressure_MAX
        self.assertEqual(-17,self.world.rollHydrographics(),"Hydro Mod Inncorrect for "+f'{self.world.temperatureType}'+' Zone, Atmo '+f'{self.world.atmosphereClass}'+' Pressure '+f'{self.world.atmospherePressure}')


   # def tearDown(self):
    #    self.world.dispose()

if __name__ == '__main__':
    unittest.main()