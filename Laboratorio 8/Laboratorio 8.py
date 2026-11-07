import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

archivo_excel = Path(__file__).resolve().parent / "Laboratorio 8.xlsx"
df = pd.read_excel(archivo_excel, sheet_name="Esfuerzo vs Elongación", header=0, index_col=0)

inc_m=0.001
m_gancho=0.987
g=9.774
inc_diametro=0.000001
diametro=0.000576
radio=diametro/2
atransv=np.pi*(radio**2)


masas=df.iloc[6:18,3].values
Pesos=masas*g
elongaciones=df.iloc[6:18,5].values
fuerzas=[Pesos[0]]
for i in range(1,len(Pesos)):
    fuerzas.append(Pesos[i]+fuerzas[i-1])
F=np.array(fuerzas,dtype=float)
esfuerzos=F/atransv
pru=df.iloc[6:18,7].values
dif=esfuerzos-pru
print(dif)