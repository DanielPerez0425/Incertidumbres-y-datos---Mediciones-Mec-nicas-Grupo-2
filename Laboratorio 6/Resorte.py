import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import scipy as scipy
import scipy.stats as stats

archivo_excel = Path(__file__).resolve().parent / "Laboratorio 6.xlsx"
df = pd.read_excel(archivo_excel, sheet_name="MCU", header=0, index_col=0)

m=df.iloc[26:32,5].values
elongacion=df.iloc[26:32,7].values

M=np.array(m, dtype=float)
Elongacion=np.array(elongacion, dtype=float)
F=M*9.81

k,b=np.polyfit(Elongacion,F,1)

res = stats.linregress(Elongacion, F)

k1 = res.slope        
b1 = res.intercept    
r2 = res.rvalue**2  


F_ajust=k*Elongacion+b

plt.figure()
plt.scatter(Elongacion,F_ajust)
plt.plot(Elongacion,F_ajust,color="red",label="Ajuste lineal")
plt.plot(Elongacion,F,color="blue",label="Original")
plt.grid(True)
#plt.show()

S_y=np.sqrt(np.sum((F-F_ajust)**2)/3)
o=np.sqrt(5/(5*np.sum(Elongacion**2))-((np.sum(Elongacion))**2))

inc_k=S_y*o
#print(f'k={k}',f'Incertidumbre= {inc_k}',f'$r^2$={r2}')
print(S_y,o,inc_k)