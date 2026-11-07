import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from pathlib import Path

archivo_excel = Path(__file__).resolve().parent / "Laboratorio 8.xlsx"
df = pd.read_excel(archivo_excel, sheet_name="Esfuerzo vs Elongación", header=0, index_col=0)

inc_m=0.001
m_gancho=0.987
g=9.774
inc_diametro=0.000001
inc_micrometro=0.000001
diametro=0.000576
radio=diametro/2
atransv=np.pi*(radio**2)

masas=df.iloc[6:18,3].values
pesos=masas*g
elongaciones=df.iloc[6:18,5].values
fuerzas=[pesos[0]]
for i in range(1,len(pesos)):
    fuerzas.append(pesos[i]+fuerzas[i-1])
F=np.array(fuerzas,dtype=float)
esfuerzos=F/atransv

Masas=np.array(masas,dtype=float)
Pesos=np.array(pesos,dtype=float)
Elongaciones=np.array(elongaciones,dtype=float)
Esfuerzos=np.array(esfuerzos,dtype=float)

m,b=np.polyfit(Elongaciones,Esfuerzos,1)
ajuste = linregress(Elongaciones, Esfuerzos)
r = ajuste.rvalue       # Coeficiente de correlación lineal
r2 = r**2               # Coeficiente de determinación
youngajust=Elongaciones*m +b

# Incertidumbres

inc_F=inc_m*g
inc_A=np.pi*(diametro/2)*inc_diametro
inc_elongacion=inc_micrometro

dEsfdF=1/atransv
dEsfdA=-F/(atransv**2)

inc_esfuerzo=np.sqrt((dEsfdF*inc_F)**2+(dEsfdA*inc_A)**2)


residuos = Esfuerzos - youngajust
N = len(Esfuerzos)
S_y = np.sqrt(np.sum(residuos**2) / (N - 2))
Sxx=np.sum((Elongaciones-np.mean(Elongaciones))**2)
suma_x_cuadrado = np.sum(Elongaciones**2)
suma_x_cuadrado2 = (np.sum(Elongaciones))**2
raiz=np.sqrt(N/((N*suma_x_cuadrado)-suma_x_cuadrado2))
inc_young = S_y * raiz
inc_yajuste = S_y * np.sqrt(1/N + (Elongaciones - np.mean(Elongaciones))**2 / Sxx)



redondeosesf=[]
for i in inc_esfuerzo:
    redondeo=round(i,1)
    if redondeo==0:
         redondeo=round(i,2)
         if redondeo==0:
             redondeo=round(i,3)
             if redondeo==0:
              redondeo=round(i,4)
    redondeosesf.append(float(redondeo))

redondeosajust=[]
for i in inc_esfuerzo:
    redondeo=round(i,1)
    if redondeo==0:
         redondeo=round(i,2)
         if redondeo==0:
             redondeo=round(i,3)
             if redondeo==0:
              redondeo=round(i,4)
    redondeosajust.append(float(redondeo))


ModYoung=round(m*1e-9,1)
Inc_Young=round(inc_young*1e-9,1)

plt.figure()
plt.errorbar(Elongaciones,Esfuerzos,xerr=inc_elongacion,yerr=inc_esfuerzo,fmt="o-",capsize=3,label="Original")
plt.errorbar(Elongaciones,youngajust,xerr=inc_elongacion,yerr=inc_yajuste,fmt="o-",capsize=3,label=f"Ajuste lineal y=({ModYoung}x{b*1e-9})$10^9$")
plt.title(f"Módulo de Young")
plt.xlabel("Elongación(m)")
plt.ylabel("Esfuerzo(Pa)")
plt.grid(True)
plt.legend()
print(f'r^2={round(r2,4)}',f'Módulo de Young={ModYoung}±{Inc_Young}GPa',f'Ecuación de la recta: (y={ModYoung}x{b*1e-9})10^9')
plt.ticklabel_format(axis='x', style='sci', scilimits=(-5, -5), useMathText=True)
plt.show()
