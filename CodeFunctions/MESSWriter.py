import os
import shutil
from CodeFunctions import ShellScriptWriter

def Writer(MESS_Name, MESS_Contents, TS_Name, Energy_Var, Ver_Ind, TS_Check = False):
    
    Base_Dir = os.getcwd() 
    
    for i, line in enumerate(MESS_Contents):
        
        if "ZeroEnergy" in line:
            ZeroEnergy_line1_Index = i
        
        if TS_Name in line:
            # TS_line = line
            # print(TS_line)
            TS_Check = True
        
        if TS_Check:
            
            for j, line2 in enumerate(MESS_Contents[i:]):
                if "ZeroEnergy" in line2:
                    ZeroEnergy_line2 = line2  
                    ZeroEnergy_line2_Index = i + j
                      
                if "WellDepth" in line2:
                    WellDepth_line1_Index = i + j
                    WellDepth_line2 = MESS_Contents[i + j + 1]
                    break           
            
            ZeroEnergy2 = float(ZeroEnergy_line2.split()[-1])
            WellDepth2  = float(WellDepth_line2 .split()[-1])

            # Adding Energy Threshold to TS Energy
            
            New_ZeroEnergy2 = ZeroEnergy2 + Energy_Var
            New_WellDepth1  = New_ZeroEnergy2
            New_ZeroEnergy1 = round(New_ZeroEnergy2 - WellDepth2, 2)
                    
            MESS_Contents[ZeroEnergy_line1_Index] = f"    ZeroEnergy[kcal/mol]   {New_ZeroEnergy1} \n"
            MESS_Contents[ZeroEnergy_line2_Index] = f"    ZeroEnergy[kcal/mol]   {New_ZeroEnergy2} \n"
            MESS_Contents[WellDepth_line1_Index]  = f"    WellDepth[kcal/mol]    {New_WellDepth1} \n"
            
            MESS_Version = MESS_Name.split('-')
            Version_Index = int(MESS_Version[-1].split('.')[0]) + Ver_Ind
            MESS_Version[-1] = f'{Version_Index}.inp'
            MESS_New_Name = "-".join(MESS_Version)
            
            MESS_File = open(MESS_New_Name, 'w')        
            MESS_File.writelines(MESS_Contents)
            MESS_File.close()   
            
            ShellScriptWriter.RunFileWriter(MESS_New_Name)
            
            NewDir = MESS_New_Name.split('.')[0]
            os.mkdir(NewDir) 
            NewDir = os.path.join(Base_Dir, NewDir)
            
            shutil.move(MESS_New_Name, NewDir)
            shutil.move("MESS_SHfile.sh", NewDir)
            
            # Subtracting Energy Threshold from TS Energy
            
            New_ZeroEnergy2 = ZeroEnergy2 - Energy_Var
            New_WellDepth1  = New_ZeroEnergy2
            New_ZeroEnergy1 = round(New_ZeroEnergy2 - WellDepth2, 2)
                    
            MESS_Contents[ZeroEnergy_line1_Index] = f"    ZeroEnergy[kcal/mol]   {New_ZeroEnergy1} \n"
            MESS_Contents[ZeroEnergy_line2_Index] = f"    ZeroEnergy[kcal/mol]   {New_ZeroEnergy2} \n"
            MESS_Contents[WellDepth_line1_Index]  = f"    WellDepth[kcal/mol]    {New_WellDepth1} \n"
            
            MESS_Version = MESS_Name.split('-')
            Version_Index = int(MESS_Version[-1].split('.')[0]) + Ver_Ind + 1
            MESS_Version[-1] = f'{Version_Index}.inp'
            MESS_New_Name = "-".join(MESS_Version)
            
            MESS_File = open(MESS_New_Name, 'w')        
            MESS_File.writelines(MESS_Contents)    
            MESS_File.close()
            
            ShellScriptWriter.RunFileWriter(MESS_New_Name)
            
            NewDir = MESS_New_Name.split('.')[0]
            os.mkdir(NewDir) 
            NewDir = os.path.join(Base_Dir, NewDir)
            
            shutil.move(MESS_New_Name, NewDir)
            shutil.move("MESS_SHfile.sh", NewDir)
            
            break