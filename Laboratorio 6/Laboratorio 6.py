import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import scipy as scipy

archivo_excel = Path(__file__).resolve().parent / "Laboratorio 6.xlsx"
df = pd.read_excel(archivo_excel, sheet_name="MCU", header=0, index_col=0)

inc_t=0.01
inc_dis=0.001
inc_m=0.0001
k=170.2396175771972
inc_k=9.166133392644946

def incertidumbres(n):
    if n==1:
        r=df.iloc[2,2]
        d=df.iloc[2:7,3].values
        t=df.iloc[2:7,4].values
        m=df.iloc[14,0]
    if n==2:
        r=df.iloc[9,2]
        t=df.iloc[9:14,4].values
        m=df.iloc[9:14,3].values
        d=0
    if n==3:
        r=df.iloc[16:21,2].values
        m=df.iloc[16,3]
        t=df.iloc[16:21,4].values
        d=0

    r=np.array(r, dtype=float)
    d=np.array(d, dtype=float)
    t=np.array(t, dtype=float)
    m=np.array(m, dtype=float)
    T=t/20
    v=(2*np.pi*r)/T
    vcuad=v**2
    Fc=m*vcuad/r
    Fk=k*(r-d)
    Dif=(np.abs(Fc-Fk)/Fc)*100

    #Incertidumbre del periodo T
    inc_T=inc_t/20

    #Incertdiumbre de la velocidad v
    dvdr=(2*np.pi)/T
    dvdT=(-2*np.pi*r)/(T**2)
    inc_v=np.sqrt((dvdr*inc_dis)**2+(dvdT*inc_T)**2)

    #Incertidumbre de v^2
    inc_vcuad=2*v*inc_v

    #Incertidumbre de Fuerza centripeta
    dFcdm=(vcuad)/r
    dFcdv=(2*m*v)/r
    dFcdr=(-m*vcuad)/(r**2)
    inc_Fc=np.sqrt((dFcdm*inc_m)**2+(dFcdv*inc_v)**2+(dFcdr*inc_dis)**2)

    #Incertidumbre de Fuerza del resorte
    dFkdk=d-r
    dFkdd=k
    dFkdr=-k

    inc_Fk=np.sqrt((dFkdk*inc_k)**2+(dFkdd*inc_dis)**2+(dFkdr*inc_dis)**2)

    #Incertidumbre de las diferencias
    dDifdFk=100/Fc
    dDifdFc=(-100*Fk)/(Fc**2)
    inc_Dif=np.sqrt((dDifdFk*inc_Fk)**2+(dDifdFc*inc_Fc)**2)

    return print(f'Tabla {n}',
                 f'Radio={r} ± {inc_dis} ',
                 f'Masa={m} ± {inc_m} ',
                 f'Tiempo (20 revoluciones)={t} ± {inc_t} ' ,
                 f'Periodo={T} ± {inc_T}',
                 f'Velocidad={v} ± {inc_v}',
                 f'$v^2$={vcuad} ± {inc_vcuad}',
                 f'Fuerza del resorte={Fk} ± {inc_Fk}',
                 f'Fuerza centrípeta={Fc} ± {inc_Fc}',
                 f'Diferencia={Dif} ± {inc_Dif}')
for i in range(1,4):
    incertidumbres(i)



