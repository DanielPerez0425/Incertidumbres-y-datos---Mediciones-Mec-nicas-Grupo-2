import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

archivo_excel = Path(__file__).resolve().parent / "Laboratorio 7.xlsx"
df1 = pd.read_excel(archivo_excel, sheet_name="Conservacion del momento lineal", header=0, index_col=0)
df2 = pd.read_excel(archivo_excel, sheet_name="Conservación de la energía", header=0, index_col=0)

g=9.81
inc_m=0.0001
inc_dist=0.0005
m_canic=0.0058
m_A=0.5152
m_B=0.5176
delta_t=0.02
inc_t=0.001
inc_Tracker_t=1/120

print("-"*50)
print("Conservación del momento lineal")
print("-"*50)

#----------------------------------------------------------------------------------------------------------------------------------------#
#                                                        Conservacion del momento lineal
#----------------------------------------------------------------------------------------------------------------------------------------#
def incertconsmomlin(inoe,repomov):
    if inoe==1 and repomov==1:
        nombre="Choque inelástico en reposo"
        deltax_A_i=df1.iloc[4:18,7].values
        deltax_A_f=df1.iloc[4:27,8].values
        deltax_B_i=[0]
        deltax_B_f=df1.iloc[4:27,10].values
    if inoe==2 and repomov==1:
        nombre="Choque elástico en reposo"
        deltax_A_i=df1.iloc[4:26,11].values
        deltax_A_f=df1.iloc[4:17,12].values
        deltax_B_i=[0]
        deltax_B_f=df1.iloc[4:21,14].values
    if inoe==1 and repomov==2:
        nombre="Choque inelástico en movimiento"
        deltax_A_i=df1.iloc[29:46,7].values
        deltax_A_f=df1.iloc[29:52,8].values
        deltax_B_i=df1.iloc[29:53,9].values
        deltax_B_f=df1.iloc[29:53,10].values    
    if inoe==2 and repomov==2:
        nombre="Choque elástico en movimiento"
        deltax_A_i=df1.iloc[29:52,11].values
        deltax_A_f=df1.iloc[29:52,12].values
        deltax_B_i=df1.iloc[29:57,13].values
        deltax_B_f=df1.iloc[29:49,14].values

    Deltax_A_i=np.array(deltax_A_i,dtype=float)
    Deltax_A_f=np.array(deltax_A_f,dtype=float)
    Deltax_B_i=np.array(deltax_B_i,dtype=float)
    Deltax_B_f=np.array(deltax_B_f,dtype=float)

    desvestAi=np.std(Deltax_A_i,ddof=1)
    desvestAf=np.std(Deltax_A_f,ddof=1)
    desvestBi=np.std(Deltax_B_i,ddof=1)
    desvestBf=np.std(Deltax_B_f,ddof=1)

    sigmaxAi=desvestAi/np.sqrt(len(Deltax_A_i))
    sigmaxAf=desvestAf/np.sqrt(len(Deltax_A_f))
    sigmaxBi=desvestBi/np.sqrt(len(Deltax_B_i))
    sigmaxBf=desvestBf/np.sqrt(len(Deltax_B_f))

    inc_DeltaxAi=np.sqrt((sigmaxAi)**2+(inc_dist)**2)
    inc_DeltaxAf=np.sqrt((sigmaxAf)**2+(inc_dist)**2)
    inc_DeltaxBi=np.sqrt((sigmaxBi)**2+(inc_dist)**2)
    inc_DeltaxBf=np.sqrt((sigmaxBf)**2+(inc_dist)**2)

    promAi=np.mean(Deltax_A_i)
    promAf=np.mean(Deltax_A_f)
    promBi=np.mean(Deltax_B_i)
    promBf=np.mean(Deltax_B_f)

    VelAi=promAi/delta_t
    VelAf=promAf/delta_t
    VelBi=promBi/delta_t
    VelBf=promBf/delta_t

    #Derivadas parciales

    dVelAidx=1/delta_t
    dVelAfdx=1/delta_t
    dVelBidx=1/delta_t
    dVelBfdx=1/delta_t

    dVelAidt=-(promAi)/(delta_t**2)
    dVelAfdt=-(promAf)/(delta_t**2)
    dVelBidt=-(promBi)/(delta_t**2)
    dVelBfdt=-(promBf)/(delta_t**2)

    #Incertidumbres de las velocidades

    inc_VelAi=np.sqrt((dVelAidx*inc_DeltaxAi)**2+(dVelAidt*inc_t)**2)
    inc_VelAf=np.sqrt((dVelAfdx*inc_DeltaxAf)**2+(dVelAfdt*inc_t)**2)
    inc_VelBi=np.sqrt((dVelBidx*inc_DeltaxBi)**2+(dVelBidt*inc_t)**2)
    inc_VelBf=np.sqrt((dVelBfdx*inc_DeltaxBf)**2+(dVelBfdt*inc_t)**2)

    pAi=m_A*VelAi
    pAf=m_A*VelAf
    pBi=m_B*VelBi
    pBf=m_B*VelBf

    dpAidm=VelAi
    dpAfdm=VelAf
    dpBidm=VelBi
    dpBfdm=VelBf

    dpAidv,dpAfdv,dpBidv,dpBfdv=m_A,m_A,m_B,m_B

    inc_pAi=np.sqrt((dpAidm*inc_m)**2+(dpAidv*inc_VelAi)**2)
    inc_pAf=np.sqrt((dpAfdm*inc_m)**2+(dpAfdv*inc_VelAf)**2)
    inc_pBi=np.sqrt((dpBidm*inc_m)**2+(dpBidv*inc_VelBi)**2)
    inc_pBf=np.sqrt((dpBfdm*inc_m)**2+(dpBfdv*inc_VelBf)**2)

    pTi=pAi+pBi
    pTf=pAf+pBf

    dpTidmA=VelAi
    dpTidmB=VelBi
    dpTidVelAi,dpTidVelBi=m_A,m_B

    dpTfdmA=VelAf
    dpTfdmB=VelBf
    dpTfdVelAf,dpTfdVelBf=m_A,m_B

    inc_pTi=np.sqrt((dpTidmA*inc_m)**2+(dpTidmB*inc_m)**2+(dpTidVelAi*inc_VelAi)**2+(dpTidVelBi*inc_VelBi)**2)
    inc_pTf=np.sqrt((dpTidmA*inc_m)**2+(dpTidmB*inc_m)**2+(dpTfdVelAf*inc_VelAf)**2+(dpTfdVelBf*inc_VelBf)**2)


    incertidumbres=[inc_DeltaxAi,inc_DeltaxAf,inc_DeltaxBi,inc_DeltaxBf,inc_VelAi,inc_VelAf,inc_VelBi,inc_VelBf,inc_pAi,inc_pAf,inc_pBi,inc_pBf,inc_pTi,inc_pTf]
    redondeos=[]
    for i in incertidumbres:
        redondeo=round(i,1)
        if redondeo==0:
            redondeo=round(i,2)
            if redondeo==0:
                redondeo=round(i,3)
                if redondeo==0:
                    redondeo=round(i,4)
        redondeos.append(float(redondeo))

    aux=VelAi*np.sqrt(m_A/(m_A+m_B))
          
    return print(
                 f'{nombre} con 50Hz:',
                 '\ bar{Delta x}_{Ai}=' f'{round(promAi,4)}±{redondeos[0]}m',
                 '\ bar{Delta x}{Af}=' f'{round(promAf,4)}±{redondeos[1]}m',
                 '\ bar{Delta x}{Bi}=' f'{round(promBi,4)}±{redondeos[2]}m',
                 '\ bar{Delta x}{B_f}=' f'{round(promBf,4)}±{redondeos[3]}m',
                 f'Velocidad inicial de la masa A: {round(VelAi,4)}±{redondeos[4]}m/s',
                 f'Velocidad final de la masa A: {round(VelAf,4)}±{redondeos[5]}m/s',
                 f'Velocidad inicial de la masa B: {round(VelBi,4)}±{redondeos[6]}m/s',
                 f'Velocidad final de la masa B: {round(VelBf,4)}±{redondeos[7]}m/s',
                 f'Momentum inicial de la masa A: {round(pAi,4)}±{redondeos[8]}Ns',
                 f'Momentum final de la masa A:{round(pAf,4)}±{redondeos[9]}Ns',
                 f'Momentum inicial de la masa B:{round(pBi,4)}±{redondeos[10]}Ns',
                 f'Momentum final de la masa B:{round(pBf,4)}±{redondeos[11]}Ns',
                 f'Momentum inicial del sistema:{round(pTi,4)}±{redondeos[12]}Ns',
                 f'Momentum final del sistema:{round(pTf,4)}±{redondeos[13]}Ns'
                 )

incertconsmomlin(1,1)
incertconsmomlin(1,2)
incertconsmomlin(2,1)
incertconsmomlin(2,2)

print("-"*50)
print("Conservación de la energía")
print("-"*50)
#----------------------------------------------------------------------------------------------------------------------------------------#
#                                                         Conservacion de la energía
#----------------------------------------------------------------------------------------------------------------------------------------#

T=df2.iloc[1:41,0].values
Y=df2.iloc[1:41,1].values
V=df2.iloc[1:41,2].values
K=df2.iloc[1:41,3].values
KR=df2.iloc[1:41,5].values
VX=df2.iloc[1:41,8].values
VY=df2.iloc[1:41,9].values
X=df2.iloc[1:41,7].values

t=np.array(T,dtype=float)
y=np.array(Y,dtype=float)
x=np.array(X,dtype=float)
v=np.array(V,dtype=float)
vx=np.array(VX,dtype=float)
vy=np.array(VY,dtype=float)
Ek=np.array(K,dtype=float)
Ekr=np.array(KR,dtype=float)

Ep=m_canic*g*y
EK=(1/2)*m_canic*(v**2)
EKR=(2/5)*EK
Em=Ep+EK+EKR

dvxdx=np.zeros(len(t))
dvxdt=np.zeros(len(t))
dvxdx[0]=0
dvxdt[0]=0

for i in range(1,len(t)-1):
    dvxdx[i]=1/(t[i+1]-t[i-1])
    dvxdt[i]=-(x[i+1]-x[i-1])/((t[i+1]-t[i-1]))**2

inc_vx=np.sqrt((dvxdx*inc_dist)**2+(dvxdt*inc_Tracker_t)**2)


dvydy=np.zeros(len(t))
dvydt=np.zeros(len(t))
dvydy[0]=0
dvydt[0]=0

for i in range(1,len(t)-1):
    dvydy[i]=1/(t[i+1]-t[i-1])
    dvydt[i]=(y[i+1]-y[i-1])/((t[i+1]-t[i-1]))**2

inc_vy=np.sqrt((dvydy*inc_dist)**2+(dvydt*inc_Tracker_t)**2)


raiz=np.sqrt(vx**2+vy**2)
dvdvx=vx/raiz
dvdvy=vy/raiz
dvdvx[0]=0
dvdvy[0]=0

inc_v=np.sqrt((dvdvx*inc_vx)**2+(dvdvy*inc_vy)**2)

dEkdm=(1/2)*(v**2)
dEkdv=m_canic*v

inc_Ek=np.sqrt((dEkdm*inc_m)**2+(dEkdv*inc_v)**2)


dEpdm=g*y
dEpdy=m_canic*g

inc_Ep=np.sqrt((dEpdm*inc_m)**2+(dEpdy*inc_dist)**2)

dEkrdm=(2/5)*dEkdm
dEkrdv=(2/5)*dEkdv

inc_Ekr=np.sqrt((dEkrdm*inc_m)**2+(dEkrdv*inc_v)**2)


dEmdm=(7/5)*dEpdm+dEkdm
dEmdy=dEpdy
dEmdv=(7/5)*dEkdv

inc_Em=np.sqrt((dEmdm*inc_m)**2+(dEmdy*inc_dist)**2+(dEmdv*inc_v)**2)


redondeosv=[]
for i in inc_v:
    redondeo=round(i,1)
    if redondeo==0:
         redondeo=round(i,2)
         if redondeo==0:
             redondeo=round(i,3)
             if redondeo==0:
              redondeo=round(i,4)
    redondeosv.append(float(redondeo))

redondeosEk=[]
for i in inc_Ek:
    redondeo=round(i,1)
    if redondeo==0:
         redondeo=round(i,2)
         if redondeo==0:
             redondeo=round(i,3)
             if redondeo==0:
              redondeo=round(i,4)
    redondeosEk.append(float(redondeo))


redondeosEp=[]
for i in inc_Ep:
    redondeo=round(i,1)
    if redondeo==0:
         redondeo=round(i,2)
         if redondeo==0:
             redondeo=round(i,3)
             if redondeo==0:
              redondeo=round(i,4)
    redondeosEp.append(float(redondeo))


redondeosEkr=[]
for i in inc_Ekr:
    redondeo=round(i,1)
    if redondeo==0:
         redondeo=round(i,2)
         if redondeo==0:
             redondeo=round(i,3)
             if redondeo==0:
              redondeo=round(i,4)
    redondeosEkr.append(float(redondeo))

redondeosEm=[]
for i in inc_Em:
    redondeo=round(i,1)
    if redondeo==0:
         redondeo=round(i,2)
         if redondeo==0:
             redondeo=round(i,3)
             if redondeo==0:
              redondeo=round(i,4)
    redondeosEm.append(float(redondeo))

distancia_porcentual = abs((Em[-1] - Em[0]) / Em[0]) * 100
print(
      f'Tiempo: {t}±{inc_Tracker_t}',
      f'Altura: {y}±{inc_dist}',
      f'Velocidad: {v}±{redondeosv}',
      f'Energía Cinética: {EK}±{redondeosEk}',
      f'Energía potencial: {Ep}±{redondeosEp}',
      f'Energía cinética rotacional: {EKR}±{redondeosEkr}',
      f'Energía mecánica: {Em}±{redondeosEm}',
      f'Pérdida porcentual de energía: {round(distancia_porcentual,2)}%'
      )

plt.figure()
plt.errorbar(t,y,xerr=inc_Tracker_t,yerr=inc_dist,fmt="o-",capsize=3,label="Altura")
plt.legend()
plt.grid(True)

plt.figure()
plt.errorbar(t,v,xerr=inc_Tracker_t,yerr=inc_v,fmt="o-",capsize=3,label="Velocidad")
plt.legend()
plt.grid(True)

plt.figure()
plt.errorbar(t[:-2],EK[:-2],xerr=inc_Tracker_t,yerr=inc_Ek[:-2],fmt="o-",capsize=3,label="Energía cinética")
plt.errorbar(t[:-2],EKR[:-2],xerr=inc_Tracker_t,yerr=inc_Ekr[:-2],fmt="o-",capsize=3,label="Energía cinética rotacional")
plt.errorbar(t[:-2],Ep[:-2],xerr=inc_Tracker_t,yerr=inc_Ep[:-2],fmt="o-",capsize=3,label="Energía potencial")
plt.errorbar(t[:-2],Em[:-2],xerr=inc_Tracker_t,yerr=inc_Em[:-2],fmt="o-",capsize=3,label="Energía mecánica")
plt.xlabel("t")
plt.ylabel("$E_k$,$E_{kr}$,$E_p$,$E_m$")
plt.title("E(J) vs t(s) con barras de error")
plt.legend()
plt.grid(True)
plt.show()