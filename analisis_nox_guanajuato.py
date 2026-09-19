"""
Análisis de emisiones de NOx en México - Caso Guanajuato
==========================================================
Ingeniería en Ciencia de Datos e IA

Estructura:
1. Carga y exploración de datos
2. Identificación del problema (Guanajuato = mayor emisor de NOx)
3. Identificación de la causa dominante (fuentes móviles carreteras)
4. MODELO PREDICTIVO: estima NOx a partir de otros contaminantes
   correlacionados con actividad vehicular (CO, COV, PM10)
5. SIMULACIÓN DE ESCENARIOS: ¿qué pasa si reducimos las emisiones
   de fuentes móviles carreteras en Guanajuato en distintos %?
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# ----------------------------------------------------------------
# 1. CARGA DE DATOS
# ----------------------------------------------------------------
df = pd.read_csv("d3_aire01_49_1.csv")

# ----------------------------------------------------------------
# 2. PROBLEMA: ¿quién emite más NOx?
# ----------------------------------------------------------------
por_entidad = df.groupby("Entidad")["NOx"].sum().sort_values(ascending=False)
print("=== TOP 5 ESTADOS POR NOx TOTAL ===")
print(por_entidad.head(5))
print(f"\nGuanajuato ocupa el lugar #{list(por_entidad.index).index('Guanajuato') + 1}")
print(f"Total NOx Guanajuato: {por_entidad['Guanajuato']:.1f} ton/año\n")

# ----------------------------------------------------------------
# 3. CAUSA: ¿de qué sector viene ese NOx en Guanajuato?
# ----------------------------------------------------------------
gto = df[df["Entidad"] == "Guanajuato"]
por_fuente = gto.groupby("Tipo_de_Fuente")["NOx"].sum().sort_values(ascending=False)
pct_fuente = (por_fuente / por_fuente.sum() * 100).round(1)

print("=== NOx EN GUANAJUATO POR TIPO DE FUENTE ===")
for fuente, pct in pct_fuente.items():
    print(f"  {fuente}: {pct}%  ({por_fuente[fuente]:.1f} ton/año)")

fuente_dominante = pct_fuente.idxmax()
print(f"\n>> Causa dominante: '{fuente_dominante}' con {pct_fuente.max()}% del total\n")

# ----------------------------------------------------------------
# 4. MODELO PREDICTIVO
# ----------------------------------------------------------------
# Hipótesis: el NOx de fuentes móviles carreteras se puede estimar
# a partir de otros contaminantes ligados a combustión vehicular
# (CO, COV, PM10), ya que todos provienen de la misma actividad.
print("=== MODELO PREDICTIVO ===")

moviles = df[df["Tipo_de_Fuente"] == "Fuentes móviles carreteros"].dropna(
    subset=["NOx", "CO", "COV", "PM_010"]
)

X = moviles[["CO", "COV", "PM_010"]]
y = moviles["NOx"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

modelo = LinearRegression()
modelo.fit(X_train, y_train)
pred = modelo.predict(X_test)

r2 = r2_score(y_test, pred)
mae = mean_absolute_error(y_test, pred)

print(f"R² del modelo: {r2:.3f}")
print(f"Error absoluto medio (MAE): {mae:.1f} toneladas")
print(f"Coeficientes: {dict(zip(X.columns, modelo.coef_.round(3)))}")
print("(Un R² ~0.6 indica que estas variables explican razonablemente")
print(" bien el NOx, aunque hay otros factores no capturados aquí.)\n")

# ----------------------------------------------------------------
# 5. SIMULACIÓN DE ESCENARIOS
# ----------------------------------------------------------------
# ¿Qué pasa con el total nacional/estatal si Guanajuato reduce sus
# emisiones de fuentes móviles carreteras en distintos porcentajes?
# (ej. por verificación vehicular más estricta, renovación de flota, etc.)
print("=== SIMULACIÓN: REDUCCIÓN DE EMISIONES MÓVILES EN GUANAJUATO ===")

nox_moviles_gto = por_fuente["Fuentes móviles carreteros"]
nox_total_gto = por_fuente.sum()
nox_total_nacional = df["NOx"].sum()

escenarios = [0, 10, 20, 30, 50]
resultados = []

for pct_reduccion in escenarios:
    nox_moviles_nuevo = nox_moviles_gto * (1 - pct_reduccion / 100)
    nox_total_gto_nuevo = nox_total_gto - (nox_moviles_gto - nox_moviles_nuevo)

    # Recalcular ranking nacional con Guanajuato modificado
    ranking_simulado = por_entidad.copy()
    ranking_simulado["Guanajuato"] = nox_total_gto_nuevo
    ranking_simulado = ranking_simulado.sort_values(ascending=False)
    nuevo_lugar = list(ranking_simulado.index).index("Guanajuato") + 1

    resultados.append(
        {
            "reduccion_%": pct_reduccion,
            "NOx_movil_restante": round(nox_moviles_nuevo, 1),
            "NOx_total_GTO": round(nox_total_gto_nuevo, 1),
            "toneladas_evitadas": round(nox_moviles_gto - nox_moviles_nuevo, 1),
            "nuevo_lugar_nacional": nuevo_lugar,
        }
    )

resultados_df = pd.DataFrame(resultados)
print(resultados_df.to_string(index=False))

resultados_df.to_csv("simulacion_escenarios_gto.csv", index=False)
print("\nResultados guardados en 'simulacion_escenarios_gto.csv'")
