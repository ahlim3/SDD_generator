import math
import random

#Defining Dose per electron
def Dose_Function(E):
    if E > 20:
        Gy = (190.4 * math.exp(0.0001526*E) - 190.3 *math.exp(-0.006081*E)) * 10
    elif E < 10:
        Gy = (287.2 * pow(E, -1.054) + 4.692) * 10
    else:
        Gy = (-0.9715 * E + 38.99) * 10
    GyPerPart = 1/Gy
    return GyPerPart

#Defining Energy Library used for SDD complier
def EnergyLib(E):
    EnergyRange = []
    if E > 500:
        IntE = round(E / 100) * 100
    elif E > 100:
        IntE = round(E / 5) * 5
    else:
        IntE = round(E/10) * 10
    while IntE > 0:
        EnergyRange.append(int(IntE))
        if IntE > 500:
            IntE = IntE - 100
        elif IntE > 100:
            IntE = IntE - 50
        else:
            IntE = IntE - 5
    EnergyRange.append(1)
    return EnergyRange

#Returning list of dose per electron for defined Energy Library
def Dose_Range(EnergyRange):
    DoseRange = []
    for E in EnergyRange:
        DoseRange.append(Dose_Function(E))
    return DoseRange

#CSDA estimation based on NIST eStar
def CSDA_Function(energy):
    coeff = [0.0391, -0.2664, 0.6271, -0.3345, -1.1255, 2.5041, -2.4158, 1.3853, 0.0254, 0]
    coeff.reverse()
    CSDA = 0
    n = 0
    for coe in coeff:
        CSDA = CSDA + pow(energy / 1000, n) * coe
        n = n + 1
    return CSDA

#CSDA List for energy
def CSDA_list_gen(Energy_Range):
    CSDA_list = []
    for E in Energy_Range:
        CSDA_list.append(CSDA_Function(E))
    
    #Additional CSDA range for 0 eV at the end
    CSDA_list.append(0)
    return CSDA_list

# CSDA Cummulative Probability Return
def CSDA_Prob(CSDA_list):
    delta = []
    n = 0
    
    #Difference between CSDA range of upper and lower boundary
    for CSDA in CSDA_list:
        if CSDA == 0:
            break
        delta.append(CSDA - CSDA_list[n+1])
        n = n + 1
    #Maximum CSDA range defined
    CSDA_Max = CSDA_list[0]
    prob = []
    
    #Instant probability calculation based on maximum CSDA
    for inst_delta in delta:
        prob.append(inst_delta/CSDA_Max)
    
    cumm_prob = []
    cur_prob = 0
    
    #Cummulative probability based on the summation of instaneous probability
    for inst_prob in prob:
        cur_prob = cur_prob + inst_prob
        cumm_prob.append(cur_prob)
    cumm_prob[-1] = 1.0
    return cumm_prob

#Particle_Selection
def Sel_Part(cumm_prob, Energy_Range, DoseRange):
    compared_prob = random.random()
    selection_index = 0
    for sel in cumm_prob:
        if compared_prob < sel:
            energy_return = Energy_Range[selection_index]
            dose_return = DoseRange[selection_index]
            break
        selection_index = selection_index + 1
    return energy_return, dose_return

#Iteration limit Dose
def Iteration_Limit(Dose, cumm_prob, Energy_Range, DoseRange):
    inst_Dose = Dose
    EnergyList = []
    DoseList = []
    while inst_Dose > 0:
        Part_Sel = Sel_Part(cumm_prob, Energy_Range, DoseRange)
        EnergyList.append(Part_Sel[0])
        DoseList.append(Part_Sel[1])
        inst_Dose = inst_Dose - Part_Sel[1]
    Dose_return = Dose - inst_Dose
    return EnergyList, DoseList, Dose_return


