import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import scipy as scipy
import scipy.stats as stats

archivo_excel = Path(__file__).resolve().parent / "Laboratorio 5.xlsx"
df = pd.read_excel(archivo_excel, sheet_name="Kepler", header=0, index_col=0)

ds=df.iloc[2:11,1].values
tp=df.iloc[2:11,2].values
masas=df.iloc[2:11,3].values
m_sol=1.98847*(10**30)

Ds=np.array(ds, dtype=float)
Tp=np.array(tp,dtype=float)
Masas=np.array(masas,dtype=float)

T_cuad=Tp**2
ds_cub=ds**3
Tcuad2=np.array(Tp**2)
dscub2=np.array(Ds**3)
m,b=np.polyfit(Ds,Tp,1)

ajust=m*Ds+b

Tplog=np.log(Tp)
tplog=np.array(Tplog)
Dslog=np.log(Ds)
dslog=np.array(Dslog)


plt.figure()
plt.plot(ds,ajust,color='red',label=f'Ajuste lineal')
plt.scatter(ds,tp)
plt.plot(ds,tp,color='blue',label='Original')
plt.xlabel('Distancia al sol(km)')
plt.ylabel('Periodo orbital (días)')
plt.legend()
plt.grid(True)
plt.title('Periodo Orbital vs Distancia al sol')

print("Recta de ajuste lineal")
print(f'y={m}x+{b}')

plt.figure()
plt.scatter(ds_cub,T_cuad,color="green")
plt.plot(ds_cub,T_cuad,color='green')
plt.title('$T^2$ vs $ds^3$')
plt.xlabel('$ds^3(km^3)$')
plt.ylabel('$T^2 (\t{días}^2)$')
plt.grid(True)


res = stats.linregress(dscub2, Tcuad2)

m = res.slope        
b = res.intercept    
r2 = res.rvalue**2  
print("Recta de $T^2$ vs $ds^3$ ")
print(f'y={m}x{b}',r2)


plt.figure()
plt.scatter(Dslog,Tplog,color='purple')
plt.plot(Dslog,Tplog,color='purple')
plt.xlabel('$\ln{ds}$')
plt.ylabel('$\ln{Tp}$')
plt.title('Ajuste logarítmico')
plt.grid(True)

print("Recta de ajuste logaritmico")
res2 = stats.linregress(dslog, Tplog)

m2 = res2.slope        
b2 = res2.intercept    
r4 = res2.rvalue**2   
print(f'y={m2}x{b2}',r4)


#plt.figure()
#plt.scatter((ds_cub/T_cuad),(scipy.constants.G/(((4*(np.pi**2))*Masas))))
#plt.grid(True)

plt.show()

#n=((np.log((T_cuad*scipy.constants.G*m_sol)/4*(np.pi**2)))/np.log(Ds))-1
#print(n)