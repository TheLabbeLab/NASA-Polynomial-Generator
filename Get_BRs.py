import os
import numpy as np
import yaml
from tabulate import tabulate
from CodeFunctions import MessDataExtraction

Base_Dir = os.getcwd()

MESS_Map = yaml.load(open('MESS_Map.yaml', 'r'), Loader=yaml.Loader)

print('\n')

for key, value in MESS_Map["Species"].items():
    print(f'{key} : {value}')

print('\n')

key_mess = input("Enter the keyword to get BR: ")
Temps = np.array(input("Enter Tempeature (Use SPACE as delimeter): ").split(" "))

print('\n')

DirSortIndex = []
Directories = []

for folder in os.listdir():
    if os.path.isdir(folder) and len(folder.split('-')) > 1:
        DirSortIndex.append(int(folder.split('-')[-1]))
        Directories.append(folder) 
        
DirSortIndex = np.argsort(np.array(DirSortIndex))
Directories = np.array(Directories)[DirSortIndex]

for folder in Directories:
    New_Dir = os.path.join(Base_Dir, folder)
    os.chdir(New_Dir)
    for file in os.listdir():
        if file.startswith(folder) and file.endswith('out'):
            FilePath = os.path.join(New_Dir, file)
            print(file)
            Parent_HighP, Parent_rates = MessDataExtraction.messExtract(FilePath, T=Temps, P=[], keywords=key_mess)
            Total_HP_Rates = np.sum(Parent_HighP[0,2:], axis=0)
            
            BRs = []
            for i in range(2, Parent_HighP.shape[1]):
                BRs.append(Parent_HighP[0,i] / Total_HP_Rates)
            
            BRs = np.array(BRs)                
            
            Header_List = list(MESS_Map['Barrier'].values())                
            Header_List.insert(0, "Temperature")
            
            BR_Transpose = np.transpose(BRs)
            
            data = []
            for i in range(0, BR_Transpose.shape[0]):
                row = [Temps[i]] + list(np.round(np.round(BR_Transpose[i], decimals=2) * 100, decimals=2))
                data.append(row)
            
            print(tabulate(data, headers=Header_List, tablefmt="pretty"))
            print('\n')
            
    os.chdir(Base_Dir)
