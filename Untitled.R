# 1. Cargar la librería para análisis de datos
# install.packages("tidyverse")

library(tidyverse)
autos <- mpg
# 2. R ya incluye varios datasets de prueba.
# Usaremos 'mpg', que contiene datos de economía de combustible de 38 modelos de autos.
# Vamos a ver las primeras filas en la consola:
print(head(autos))

# 3. MANIPULACIÓN DE DATOS (Filtrar y Seleccionar)
# Queremos ver solo los autos modernos (año 2008) y con motores grandes (cilindrada > 4 litros)
autos_grandes <- autos %>%
  filter(year == 2008, displ > 4)

# Mostramos el resultado filtrado
print("Autos del 2008 con motores grandes:")
print(autos_grandes)

# 4. VISUALIZACIÓN DE DATOS (Crear una gráfica)
# Vamos a graficar el tamaño del motor (displ) contra el consumo en autopista (hwy)
grafica <- ggplot(data = autos) +
  geom_point(mapping = aes(x = displ, y = hwy, color = class)) +
  labs(
    title = "Tamaño del Motor vs Consumo en Autopista",
    x = "Tamaño del Motor (Litros)",
    y = "Millas por Galón en Autopista"
  ) +
  theme_minimal()

# Mostrar la gráfica en PyCharm
print(grafica)
