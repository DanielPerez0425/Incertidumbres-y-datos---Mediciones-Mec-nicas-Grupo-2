import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import scipy as scipy

archivo_excel = Path(__file__).resolve().parent / "Laboratorio 5.xlsx"
df = pd.read_excel(archivo_excel, sheet_name="Resortes", header=0, index_col=0)

inc_long=df.iloc[25,0]
Morado=lmorado=df.iloc[1,0]
Largo=llargo=df.iloc[2,0]
Corto=lcorto=df.iloc[3,0]
inc_masas1=df.iloc[5,0]
inc_masas2=df.iloc[5,3]
mgancho1=df.iloc[4,0]
mgancho2=df.iloc[5,9]
m500=df.iloc[20,0]
m200=df.iloc[21,0]
m100=df.iloc[22,0]
m50=df.iloc[20,1]

def incertidumbres(longitud,POS):
    if longitud==lcorto and POS==0:
        nombre="Resorte Corto"
        Elongacion=df.iloc[9:19, 3].values
        Masas=df.iloc[9:19,1].values
    if longitud==lmorado and POS==0:
        nombre="Resorte Mediano"
        Elongacion=df.iloc[9:19, 10].values
        Masas=df.iloc[9:19,8].values
    if longitud==llargo and POS== 0:
        nombre="Resorte Largo"
        Elongacion=df.iloc[22:32, 10].values
        Masas=df.iloc[22:32,8].values

    if longitud==0 and POS==2:
        nombre="Resortes en Serie"
        Elongacion=df.iloc[22:32, 19].values
        Masas=df.iloc[22:32,17].values
        
    if longitud==0 and POS==1:
            nombre="Resortes en Paralelo"
            Elongacion=df.iloc[9:19, 19].values
            Masas=df.iloc[9:19,17].values
            
                
    Elongacion = np.array(Elongacion, dtype=float)
    Masas = np.array(Masas, dtype=float)
    
    Fuerzas=Masas*9.81
    inc_fuerzas=inc_masas1*9.81
    
    #Gráficas con ajuste lineal
    
    m,b=np.polyfit(Elongacion,Fuerzas,1)
    F_ajust=m*Elongacion+b
    
    plt.figure()
    residuos = Fuerzas - F_ajust
    N = len(Elongacion)
    S_y = np.sqrt(np.sum(residuos**2) / (N - 2))
    suma_x_cuadrado = np.sum(Elongacion**2)
    suma_x_cuadrado2 = (np.sum(Elongacion))**2
    raiz=np.sqrt(N/((N*suma_x_cuadrado)-suma_x_cuadrado2))
    inc_k = S_y * np.sqrt(raiz)
    plt.plot(Elongacion,F_ajust,"--",color="red",label=f'Ajuste lineal')
    plt.title(f"Fuerza(N) vs Elongación(m) - {nombre}")
    plt.xlabel("Elongación (m)")
    plt.ylabel("Fuerza (N)")
    plt.grid(True)
    plt.legend()
    
    plt.errorbar(Elongacion, Fuerzas,xerr=inc_long, yerr=inc_fuerzas,fmt='o', markersize=5, capsize=3,label=f'Datos experimentales')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    return print(nombre,np.sqrt(raiz),S_y,inc_k,round(inc_k,1))

lista=[lcorto,lmorado,llargo]
for i in range(3):
    incertidumbres(lista[i],0)
incertidumbres(0,1)
incertidumbres(0,2)