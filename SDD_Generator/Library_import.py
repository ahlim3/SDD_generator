import os
import pandas as pd
import random
import glob
import fileinput
import sys
import math

#importing SDD_Library of specific energy
def Lib_Import(energy):
    data_set = []
    Lib_ext = str(energy) + "keV_Lib.txt"
    parent_dir = "SDD_Lib/"
    index_path = os.path.join(parent_dir, Lib_ext)
    SDD_read = open(index_path, 'r')
    for line in SDD_read:
        data_set.append(line)
    return data_set

#Index returning Function
def Lib_csv_Import(energy, particle):
    data_set = []
    particle_index = []
    Lib_ext = str(energy) + "keV_Lib.csv"
    parent_dir = "SDD_Lib/"
    index_path = os.path.join(parent_dir, Lib_ext)
    SDD_csv_read = pd.read_csv(index_path)
    remaining_part = particle
    while remaining_part > 0:
        Number = int(random.random() * 10000)
        IndexLoc = SDD_csv_read.index[(SDD_csv_read['PartNumber'] == Number)].tolist()
        particle_index.append(IndexLoc)
        remaining_part = remaining_part - 1
    return particle_index

#SDD generator
def SDD_gen(Dose, Particle, Energy, Author, Info):
    path = str(Energy) + "keV_SDD/"
    isExist = os.path.exists(path)
    if not isExist:
        os.mkdir(path)
        print("New " + str(Energy) + "keV Folder")
    filename = str(Dose) + "Gy_" + str(Energy) + "keV"
    file_ext = '.sdd'
    SDD_path = os.path.join(path)
    output_path = SDD_path + '%s%s'%(filename, file_ext)
    uniq = 1
    while os.path.exists(output_path):
        output_path = SDD_path + '%s(%d)%s' % (filename,uniq,file_ext)
        uniq+=1
    k = open(output_path, 'w')
    k.write("SDD version,SDDv1.0;\n")
    k.write("Software,InSilico SDD Generator;\n")
    k.write("Author," + str(Author) + ";\n")
    k.write("Simulation Details,Electron Generator;\n")
    k.write("Source type,1;\n")
    k.write("Source,11;\n")
    k.write("Incident particles,11;\n")
    k.write("Mean particle energy," + str(Energy/1000) + ";\n")
    k.write("Energy distribuion,M,0;\n")
    k.write("Particle fraction,1.0;\n")
    k.write("Dose or fluence,1,1e-12;\n")
    k.write("Dose rate,0.0;\n")
    k.write("Irradiation target,Nucleus;\n")
    k.write("Volumes,0,5,5,5,0,0,0,1,4.65,4.65,4.65,0,0,0;\n")
    k.write("Chromosome sizes, 46,252.823,252.823,248.157,248.157,204.04,204.04,195.556,195.556,184.951,184.951,174.77,174.77,162.469,162.469,149.318,149.318,143.38,143.38,138.289,138.289,137.441,137.441,135.32,135.32,116.655,116.655,108.595,108.595,102.656,102.656,90.7788,90.7788,80.1738,80.1738,77.6286,77.6286,65.3268,65.3268,63.63,63.63,47.9346,47.9346,50.4798,50.4798,58.9638,158.227;\n")
    k.write("DNA Density,14.4318;\n")
    k.write("Cell Cycle Phase,0,1;\n")
    k.write("DNA Structure,0,1;\n")
    k.write("In vitro/in vivo,0;\n")
    k.write("Proliferation status,1;\n")
    k.write("Microenvironment,20,0.01;\n")
    k.write("Damage definition,1,0,10,10,17.5;\n")
    k.write("Time,0.000000;\n")
    k.write("Damage and primary count,"+ str(len(Info)) + ","+ str(Particle) + ";\n")
    k.write("Data entries,1,1,1,1,1,1,1,0,0,0,0,0,0,0;\n")
    k.write("Additional information,;\n")
    k.write("***EndOfHeader***;\n")
    for line in Info:
        k.write(line)
    k.close()