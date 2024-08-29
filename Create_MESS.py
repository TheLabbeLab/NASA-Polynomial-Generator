import os
import yaml
import numpy as np
from CodeFunctions import MESSWriter

Base_Dir = os.getcwd() 

MESS_Map = yaml.load(open('MESS_Map.yaml', 'r'), Loader=yaml.Loader)

Base_Folder = input("Enter the folder name: ")

Base_Folder_Path = os.path.join(Base_Dir, Base_Folder)

os.chdir(Base_Folder_Path)

for file in os.listdir():
     if file.endswith(".inp"):
        MESS_Name = file
        MESS_File = open(file, 'r')
        MESS_Contents = MESS_File.readlines()
        MESS_File.close()
        
os.chdir(Base_Dir)

# print(MESS_Contents)

print('\n')

for key, value in MESS_Map["Species"].items():
    print(f'{key} : {value}')

print('\n')

for key, value in MESS_Map["Barrier"].items():
    print(f'{key} : {value}')

print('\n')

print("Enter Barrier names for which you want to modify the TS Barrier Height. Use Comma as delimeter")
Barrier_Names = np.array(input("Enter the key name: ").replace(" ","").split(','))
  
# print(Well_Names)  
# print(Well_Names[0])
  

Energy_Var = float(input("Enter the Energy Variation(This value will be used to create mimum and maximum Energy TS Barrier Range): "))

Ver_Ind = 1

for i, TS_Name in enumerate(Barrier_Names):
    MESSWriter.Writer(MESS_Name, MESS_Contents, TS_Name, Energy_Var, Ver_Ind)
    Ver_Ind += 2
