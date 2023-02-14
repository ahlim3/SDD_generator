from Parameter import Dose_Range
from Parameter import CSDA_list_gen
from Parameter import EnergyLib
from Parameter import CSDA_Prob
from Parameter import Sel_Part
from Parameter import Iteration_Limit
from Library_import import Lib_Import
from Library_import import Lib_csv_Import
from Library_import import SDD_gen
import pandas as pd
import random

def Electron_SDD_Generator(InputEnergy, InputDose, Author):
    Energy_Range = EnergyLib(InputEnergy)
    DoseRange = Dose_Range(EnergyLib(InputEnergy))
    cumm_prob = CSDA_Prob(CSDA_list_gen(EnergyLib(InputEnergy)))
    [Electron_Selection, Dose_Selection, Dose] = Iteration_Limit(InputDose, cumm_prob, Energy_Range, DoseRange)
    
    Electron_Selection.sort()
    Electron_Selection.reverse()
    selection_count = []
    
    for energy in Energy_Range:
        count = 0
        for selection in Electron_Selection:
            if energy == selection:
                count = count + 1
        selection_count.append(count)
    selection_index = 0
    countList = []
    excution_particle = 0
    
    for Energy in Energy_Range:
        specific_selection_count = selection_count[selection_index]
        Specific_Lib = Lib_Import(Energy)
        Damage_index = Lib_csv_Import(Energy, specific_selection_count)
        n = 0
        while n < len(Damage_index):
            for i in Damage_index[n]:
                intermediate_info = Specific_Lib[i]
                particleinfo = intermediate_info.split(';')
                startinginfo = particleinfo[0].split(',')
                startinginfo[1] = str(excution_particle)
                if excution_particle != 0 and int(startinginfo[0]) == 2:
                    startinginfo[0] = str(int(1))
                particleinfo[0] = ','.join(startinginfo)
                intermediate_info = ';'.join(particleinfo)
                countList.append(intermediate_info)
            n = n + 1
            excution_particle = excution_particle + 1
        selection_index = selection_index + 1
    replacement = list(countList[0])
    replacement[0] = '2'
    replacement = "".join(replacement)
    countList[0] = replacement
    
    Time_Switch = 0
    SDD_gen(InputDose, excution_particle, InputEnergy, Author, countList, Time_Switch)
    
def Electron_SDD_Generator_DoseRate(InputEnergy, InputDose, Author, TimeStamp, HalfLife):
    Energy_Range = EnergyLib(InputEnergy)
    DoseRange = Dose_Range(EnergyLib(InputEnergy))
    cumm_prob = CSDA_Prob(CSDA_list_gen(EnergyLib(InputEnergy)))
    [Electron_Selection, Dose_Selection, Dose] = Iteration_Limit(InputDose, cumm_prob, Energy_Range, DoseRange)
    
    Electron_Selection.sort()
    Electron_Selection.reverse()
    selection_count = []
    
    for energy in Energy_Range:
        count = 0
        for selection in Electron_Selection:
            if energy == selection:
                count = count + 1
        selection_count.append(count)
    selection_index = 0
    countList = []
    excution_particle = 0
    
    for Energy in Energy_Range:
        specific_selection_count = selection_count[selection_index]
        Specific_Lib = Lib_Import(Energy)
        Damage_index = Lib_csv_Import(Energy, specific_selection_count)
        n = 0
        while n < len(Damage_index):
            for i in Damage_index[n]:
                intermediate_info = Specific_Lib[i]
                particleinfo = intermediate_info.split(';')
                startinginfo = particleinfo[0].split(',')
                startinginfo[1] = str(excution_particle)
                particleinfo[0] = ','.join(startinginfo)
                Int_TimeStamp = float(TimeStamp * excution_particle)
                Time_Stamp = Int_TimeStamp / pow(0.5, Int_TimeStamp/(HalfLife*1E9))
                particleinfo[-1] = str(int(Time_Stamp)) + ";\n"
                intermediate_info = ';'.join(particleinfo)
                countList.append(intermediate_info)
            n = n + 1
            excution_particle = excution_particle + 1
        selection_index = selection_index + 1
    replacement = list(countList[0])
    replacement[0] = '2'
    replacement = "".join(replacement)
    countList[0] = replacement
    
    Time_Switch = 1
    SDD_gen(InputDose, excution_particle, InputEnergy, Author, countList, Time_Switch)
