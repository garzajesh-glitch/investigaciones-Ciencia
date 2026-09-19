import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('d3_aire01_49_1.csv')


df = pd.read_csv('d3_aire01_49_1.csv')
df = df.dropna(subset=['NOx'])  # dropna sobre la columna numérica que nos importa

# 1. Agrupar por Entidad (sumar todas las filas/municipios de cada estado)
por_entidad = df.groupby('Entidad')['NOx'].sum()

# 2. Ordenar por el VALOR numérico de NOx, de mayor a menor
por_entidad = por_entidad.sort_values(ascending=False)

# 3. Cortar a los primeros 10
top10 = por_entidad.head(10)

plt.figure(figsize=(10, 6), facecolor='white')
ax = plt.subplot(111)
ax.set_facecolor('white')
plt.bar(top10.index, top10.values, color='gray', edgecolor='black', linewidth=0.8)

plt.xlabel('Entidad Federativa', fontsize=11, family='sans-serif', labelpad=10)
plt.ylabel('Emisiones de NOx (Toneladas)', fontsize=11, family='sans-serif', labelpad=10)

# Estandarizar la fuente de los valores de los ejes (8-14 puntos)
plt.xticks(rotation=45, ha='right', fontsize=10, family='sans-serif')
plt.yticks(fontsize=10, family='sans-serif')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()

# Grafica con la fuente que mas emite NOx
gto = df[df['Entidad'] == 'Guanajuato']
por_fuente = gto.groupby('Tipo_de_Fuente')['NOx'].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6), facecolor='white')
ax = plt.subplot(111)
ax.set_facecolor('white')
plt.bar(por_fuente.index, por_fuente.values, color='gray', edgecolor='black', linewidth=0.8)

plt.xlabel('Fuentes de Emisión', fontsize=11, family='sans-serif', labelpad=10)
plt.ylabel('Emisiones de NOx (Toneladas)', fontsize=11, family='sans-serif', labelpad=10)

# Estandarizar la fuente de los valores de los ejes (8-14 puntos)
plt.xticks(rotation=45, ha='right', fontsize=10, family='sans-serif')
plt.yticks(fontsize=10, family='sans-serif')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()