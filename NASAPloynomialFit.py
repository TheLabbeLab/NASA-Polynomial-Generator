# Labbe Lab propoerty
# Coder: Pray Shah
# Generates NASA-7 Polynomial Fit!

import os
import re
import numpy as np
from scipy.optimize import curve_fit
import functools

global R

R = 1.9872 #cal/mol.k

class NASA7Ploynomial():
    
    def SpecificHeat(T, a1, a2, a3, a4, a5):
        
        T = np.array(T, dtype='float64')

        specificHeat = R * (a1 + a2*T + a3*T**2 + a4*T**3 + a5*T**4)

        return specificHeat
    
    def Enthalpy(T, a6, a1, a2, a3, a4, a5):

        T = np.array(T, dtype='float64')
        
        enthalpy = R * T * (a1 + (a2/2)*T + (a3/3)*T**2 + (a4/4)*T**3 + (a5/5)*T**4 + (a6/T))
    
        return enthalpy
    
    def Entropy(T, a7, a1, a2, a3, a4, a5):

        T = np.array(T, dtype='float64')

        entropy    = R * (a1*np.log(T) + a2*T + (a3/2)*T**2 + (a4/3)*T**3 + (a5/4)*T**4 + a7)

        return entropy

def LineNumSearch(DataFile, SearchLine):
    for linenum, line in enumerate(fileData):
        if SearchLine.search(line):
            return linenum

outputFile = 'ChemkinFormatThermoChemistry.inp'
writeFile  = open(outputFile, 'w')

SpeciesNameLine = re.compile(r"NAME")
LineStart       = re.compile(r"METH  READIN")
LineEnd         = re.compile(r"FINISH")

for file in os.listdir():
    if file.endswith(r'.i97'):
        ThermInpfile = open(file)
        fileData = ThermInpfile.readlines()
        # print(file)
        LineStartNum        = LineNumSearch(fileData, LineStart) + 1
        LineEndNum          = LineNumSearch(fileData, LineEnd)
        SpeciesNameNum      = LineNumSearch(fileData, SpeciesNameLine)
        SpeciesName         = fileData[SpeciesNameNum].split()[-1]
        EnthlpyOfFormation  = float(fileData[SpeciesNameNum + 1].split()[2])  / 1000 # Converting Joules to KJoules
        # print(float(EnthlpyOfFormation))
        # print(LineStartNum, LineEndNum)
        ThermoData = fileData[LineStartNum:LineEndNum]
        # print(ThermoData)
        Temps = []
        specificHeat = []
        enthalpy = []
        entropy = []
        for line in ThermoData:
            Temps.          append(float(line.split()[1]))
            specificHeat.   append(float(line.split()[3]))
            entropy.        append(float(line.split()[5]))
            enthalpy.       append(float(line.split()[7]) + EnthlpyOfFormation)
        
        # print(SpeciesName)

        Temps           = np.array(Temps, dtype='float64')
        minIndex        = np.where(Temps == 300)[0][0]
        breakIndex      = np.where(Temps == 1000)[0][0]
        specificHeat    = np.array(specificHeat) / 4.184 # Converitng Joules to Cals    
        enthalpy        = np.array(enthalpy)     * 1000 / 4.184 # Converitng Joules to Cals
        entropy         = np.array(entropy)      / 4.184 # Converitng Joules to Cals
        # Specific Heat
        # print(f"Enthalpy: {enthalpy}")
        # print(f"Specific Heat {specificHeat}")
        # print(Temps[minIndex:breakIndex + 1])
        # print(Temps[breakIndex:])

        shLowerParams, _ = curve_fit(NASA7Ploynomial.SpecificHeat, Temps[minIndex:breakIndex + 1], specificHeat[minIndex:breakIndex + 1], maxfev=1000000)

        shUpperParams, _ = curve_fit(NASA7Ploynomial.SpecificHeat, Temps[breakIndex:], specificHeat[breakIndex:], maxfev=1000000)

        a1Lower, a2Lower, a3Lower, a4Lower, a5Lower = shLowerParams

        a1Upper, a2Upper, a3Upper, a4Upper, a5Upper = shUpperParams
        
        # Enthalpy

        enthalpyFunc    = functools.partial(NASA7Ploynomial.Enthalpy, a1=a1Lower, a2=a2Lower, a3=a3Lower, a4=a4Lower, a5=a5Lower)
        a6Lower         = curve_fit(enthalpyFunc, Temps[minIndex:breakIndex + 1], enthalpy[minIndex:breakIndex + 1], maxfev=500000)[0][0]

        # print(a6Lower)

        enthalpyFunc    = functools.partial(NASA7Ploynomial.Enthalpy, a1=a1Upper, a2=a2Upper, a3=a3Upper, a4=a4Upper, a5=a5Upper)
        a6Upper         = curve_fit(enthalpyFunc, Temps[breakIndex:]        , enthalpy[breakIndex:], maxfev=500000)[0][0]

        # print(a6Upper)

        # Entropy

        entropyFunc     = functools.partial(NASA7Ploynomial.Entropy, a1=a1Lower, a2=a2Lower, a3=a3Lower, a4=a4Lower, a5=a5Lower)
        a7Lower         = curve_fit(entropyFunc, Temps[minIndex:breakIndex + 1], entropy[minIndex:breakIndex + 1], maxfev=500000)[0][0]

        entropyFunc     = functools.partial(NASA7Ploynomial.Entropy, a1=a1Upper, a2=a2Upper, a3=a3Upper, a4=a4Upper, a5=a5Upper)
        a7Upper         = curve_fit(entropyFunc, Temps[breakIndex:]        , entropy[breakIndex:], maxfev=500000)[0][0]

        # print("Lower:")
        # print(a1Lower, a2Lower, a3Lower, a4Lower, a5Lower, a6Lower, a7Lower)
        # print("Upper")
        # print(a1Upper, a2Upper, a3Upper, a4Upper, a5Upper, a6Upper, a7Upper)

        writeFile.write(f"{SpeciesName} Date   Element    Phase   300     {int(Temps[-1])}   1000    \t1\n")
        writeFile.write(f"{a1Upper:+.8E}{a2Upper:+.8E}{a3Upper:+.8E}{a4Upper:+.8E}{a5Upper:+.8E} \t2\n")
        writeFile.write(f"{a6Upper:+.8E}{a7Upper:+.8E}{a1Lower:+.8E}{a2Lower:+.8E}{a3Lower:+.8E} \t3\n")
        writeFile.write(f"{a4Lower:+.8E}{a5Lower:+.8E}{a6Lower:+.8E}{a7Lower:+.8E}                \t4\n")
        writeFile.write("\n")

writeFile.close()
