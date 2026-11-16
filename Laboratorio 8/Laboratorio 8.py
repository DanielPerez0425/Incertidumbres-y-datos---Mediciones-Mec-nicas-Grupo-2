import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from pathlib import Path

archivo_excel = Path(__file__).resolve().parent / "Laboratorio 8.xlsx"
df = pd.read_excel(archivo_excel, sheet_name="Esfuerzo vs Elongación", header=0, index_col=0)

inc_m=0.001
g=9.774
inc_diametro=0.000001
inc_micrometro=0.000005
inc_reg=0.0001
longitud=1.084
mu=1e-6

def incertidumbres(alambre):

    if alambre==1184:
        nombre='Alambre 1184'
        m_alamb=0.0035
        l_0=0.621
        masas=df.iloc[41:52,4].values
        elong=df.iloc[41:52,8].values

    if alambre==1172:
        nombre='Alambre 1172'
        m_alamb=0.0043
        l_0=0.623
        masas=df.iloc[57:68,4].values
        elong=df.iloc[57:68,8].values

    N=np.linspace(1,11,11)
    elong=np.asarray(elong,dtype=float)
    diametro=0.61/1000
    radio=diametro/2
    atransv=np.pi*(radio**2)
    elongaciones=elong/l_0

    fuerzas=masas*g
    F=np.array(fuerzas,dtype=float)
    esfuerzos=F/atransv

    Masas=np.array(masas,dtype=float)
    Elongaciones=np.array(elongaciones,dtype=float)
    Esfuerzos=np.array(esfuerzos,dtype=float)

    m,b=np.polyfit(Elongaciones,Esfuerzos,1)
    ajuste = linregress(Elongaciones, Esfuerzos)
    r = ajuste.rvalue       # Coeficiente de correlación lineal
    r2 = r**2               # Coeficiente de determinación
    youngajust=Elongaciones*m +b

    # Incertidumbres

    inc_F=inc_m*g
    inc_A=2*np.pi*(diametro/2)*inc_diametro

    dElongdDelta=1/l_0
    dElongdl0=(-elong)/(l_0**2)

    inc_elongacion=np.sqrt((dElongdDelta*inc_micrometro)**2+(dElongdl0*inc_reg)**2)
    
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

    redondeoselong=[]
    for i in inc_elongacion:
        redondeo=round(i,1)
        if redondeo==0:
            redondeo=round(i,2)
            if redondeo==0:
                redondeo=round(i,3)
            if redondeo==0:
                    redondeo=round(i,4)
        redondeoselong.append(float(redondeo))

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

    ModYoung=round(m,1)
    Inc_Young=round(inc_young,1)

    plt.figure()
    plt.errorbar(Elongaciones,Esfuerzos,xerr=inc_elongacion,yerr=inc_esfuerzo,fmt="o-",capsize=3,label="Original")
    if b>0:
        plt.errorbar(Elongaciones,youngajust,xerr=inc_elongacion,yerr=inc_yajuste,fmt="o-",capsize=3,label=f"Ajuste lineal y=({round(ModYoung*1e-9,4)}x+{round(b*1e-9,4)})$10^9$")
    else:
        plt.errorbar(Elongaciones,youngajust,xerr=inc_elongacion,yerr=inc_yajuste,fmt="o-",capsize=3,label=f"Ajuste lineal y=({round(ModYoung*1e-9,4)}x{round(b*1e-9,4)})$10^9$")
    plt.title(f"Módulo de Young con {nombre}")
    plt.xlabel("Elongación")
    plt.ylabel("Esfuerzo(Pa)")
    plt.grid(True)
    plt.legend()
    plt.ticklabel_format(axis='x', style='sci', scilimits=(-5, -5), useMathText=True)
    #plt.show()

    # Cálculo Teórico

    denslin=m_alamb/longitud

    dDenslindm=1/longitud
    dDenslindl=(-m_alamb)/(longitud**2)

    inc_denslin=np.sqrt((dDenslindm*inc_m)**2+(dDenslindl*inc_reg)**2)

    f1=(1/(2*longitud))*np.sqrt(F/denslin)

    df1dl=(-1/(2*(longitud**2)))*np.sqrt(F/denslin)
    df1dF=1/(4*longitud*np.sqrt(F*denslin))
    df1dDenslin=(-np.sqrt(F))/(4*longitud*(np.power(denslin,3/2)))

    inc_f1=np.sqrt((df1dl*inc_reg)**2+(df1dF*inc_F)**2+(df1dDenslin*inc_denslin)**2)

    Yf=(4*(longitud**2)*(f1**2)*denslin)/(atransv*Elongaciones)

    dYfdl=(8*longitud*(f1**2)*denslin)/(atransv*Elongaciones)
    dYfdf1=(8*(longitud**2)*f1*denslin)/(atransv*Elongaciones)
    dYfdDenslin=(4*(longitud**2)*(f1**2))/(atransv*Elongaciones)
    dYfdA=(-4*(longitud**2)*(f1**2)*denslin)/((atransv**2)*Elongaciones)
    dYfdElong=(-4*(longitud**2)*(f1**2)*denslin)/((atransv)*(Elongaciones**2))

    inc_Yf=np.sqrt((dYfdl*inc_reg)**2+(dYfdf1*inc_f1)**2+(dYfdDenslin*inc_denslin)**2+(dYfdA*inc_A)**2+(dYfdElong*inc_elongacion)**2)

    return print(
                f'{nombre}:',
                f'Fuerzas: {F}±{inc_F}',
                f'Elongaciones:{Elongaciones}±{inc_elongacion}',
                f'Esfuerzos:{Esfuerzos}±{inc_esfuerzo}',
                f'r^2={round(r2,4)}',
                f'Módulo de Young=({round(ModYoung*1e-9,4)}±{round(Inc_Young*1e-9,4)})GPa',
                f'Módulo de Young por frecuencia: {round(Yf[-5]*1e-9,4)}±{round(inc_Yf[-5]*1e-9,4)}GPa',
                f'Ecuación de la recta: (y={ModYoung*1e-9}x+({b*1e-9}))10^9'
                )

incertidumbres(1184)
incertidumbres(1172)