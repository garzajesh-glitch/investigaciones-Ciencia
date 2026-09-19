"""
###############################################################################
  SIMULACIÓN: ¿Qué tan jodido estará Guanajuato si empeoran las
  fuentes móviles carreteras?

  HALLAZGO CLAVE:
    Guanajuato YA es el #1 emisor de NOx del país.
    Solo sus fuentes móviles carreteras (autos/camiones) emiten
    más NOx que todo Veracruz (el 2º estado completo).

  Por eso la simulación no pregunta "¿subirá de lugar?" (ya está
  en el tope), sino:
      "¿Cuánto crece la BRECHA con el 2º lugar si la fuente móvil
       empeora X%, y cuánto sube su % del total nacional?"

  Nota: NO usa regresión lineal porque esto es una simulación
  mecánica (un escenario), no un aprendizaje de máquina.
###############################################################################
"""

import pandas as pd

# ----------------------------------------------------------------
# 1. Cargar datos (inventario nacional de emisiones, un solo año)
# ----------------------------------------------------------------
df = pd.read_csv('d3_aire01_49_1.csv')

# ----------------------------------------------------------------
# 2. Ranking nacional actual de NOx
# ----------------------------------------------------------------
nox_por_estado = df.groupby('Entidad')['NOx'].sum().sort_values(ascending=False)
gto_nox        = nox_por_estado['Guanajuato']   # NOx total de GTO
segundo_nox    = nox_por_estado.iloc[1]         # NOx del 2º lugar (Veracruz)
total_nacional = nox_por_estado.sum()           # NOx de todo el país

# NOx que viene de las fuentes móviles carreteras dentro de GTO
gto = df[df['Entidad'] == 'Guanajuato']
nox_moviles_gto = gto[gto['Tipo_de_Fuente'] == 'Fuentes móviles carreteros']['NOx'].sum()

# print("=== RANKING NACIONAL DE NOx (top 5) ===")
print(nox_por_estado.head(5).round(0).to_string())
# print(f"\n>> Guanajuato es el #1 emisor de NOnenx del país.")
print(f"   Lidera a {nox_por_estado.index[1]} por {gto_nox - segundo_nox:,.0f} ton"
      f" ({(gto_nox/segundo_nox - 1)*100:.1f}% más).\n")

# ----------------------------------------------------------------
# 3. EL DATO QUE TUMBA: GTO móvil supera a estados enteros
# ----------------------------------------------------------------
estados_superados = [e for e, n in nox_por_estado.items() if n < nox_moviles_gto]
print("=== DATO CLAVE ===")
print(f"Solo el tráfico vehicular de GTO ({nox_moviles_gto:,.0f} ton)"
      f" supera el NOx de {len(estados_superados)} de {len(nox_por_estado)}"
      f" estados, incluido el #2 completo.\n")

# ----------------------------------------------------------------
# 4. SIMULACIÓN: la fuente móvil empeora X%
# ----------------------------------------------------------------
print("=== SIMULACIÓN: LA FUENTE MÓVIL EMPEORA ===")

escenarios = [0, 10, 25, 50, 75, 100]
resultados = []

for pct in escenarios:
    # Nuevo NOx de la fuente móvil: hoy + (hoy * pct/100)
    nox_moviles_nuevo = nox_moviles_gto * (1 + pct / 100)

    # Nuevo total de GTO: total de hoy + (aumento en la fuente móvil)
    gto_nuevo = gto_nox + (nox_moviles_nuevo - nox_moviles_gto)

    # Brecha con el 2º lugar (Veracruz no cambia en este escenario)
    brecha_nueva = gto_nuevo - segundo_nox

    # Nuevo % del total nacional (ajustando el total por el nuevo GTO)
    nacional_nuevo = total_nacional - gto_nox + gto_nuevo
    share = gto_nuevo / nacional_nuevo * 100

    resultados.append({
        'empeora_%': pct,
        'NOx_movil_GTO': round(nox_moviles_nuevo, 1),
        'NOx_total_GTO': round(gto_nuevo, 1),
        'brecha_vs_2do': round(brecha_nueva, 1),
        '%_nacional': round(share, 2),
    })

resultados_df = pd.DataFrame(resultados)
print(resultados_df.to_string(index=False))

# ----------------------------------------------------------------
# 5. Guardar resultado
# ----------------------------------------------------------------
resultados_df.to_csv('simulacion_empeora_gto.csv', index=False)
print("\nGuardado en 'simulacion_empeora_gto.csv'")