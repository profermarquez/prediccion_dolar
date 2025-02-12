import pandas as pd
from bs4 import BeautifulSoup

# HTML de la tabla
html = """<table class="general-historical__table table"><thead class="general-historical__thead thead"><tr><th scope="col">Fecha</th><th scope="col">Compra</th><th scope="col">Venta</th></tr></thead>  <tbody class="general-historical__tbody tbody"><tr><td>10/02/2025</td><td>1185,00</td><td>1205,00</td></tr><tr><td>10/02/2025</td><td>1185,00</td><td>1205,00</td></tr><tr><td>10/02/2025</td><td>1185,00</td><td>1205,00</td></tr><tr><td>10/02/2025</td><td>1185,00</td><td>1205,00</td></tr><tr><td>07/02/2025</td><td>1185,00</td><td>1205,00</td></tr><tr><td>07/02/2025</td><td>1190,00</td><td>1210,00</td></tr><tr><td>07/02/2025</td><td>1195,00</td><td>1215,00</td></tr><tr><td>06/02/2025</td><td>1195,00</td><td>1215,00</td></tr><tr><td>06/02/2025</td><td>1195,00</td><td>1215,00</td></tr><tr><td>06/02/2025</td><td>1195,00</td><td>1215,00</td></tr><tr><td>05/02/2025</td><td>1195,00</td><td>1215,00</td></tr><tr><td>05/02/2025</td><td>1195,00</td><td>1215,00</td></tr><tr><td>05/02/2025</td><td>1195,00</td><td>1215,00</td></tr><tr><td>04/02/2025</td><td>1195,00</td><td>1215,00</td></tr><tr><td>04/02/2025</td><td>1200,00</td><td>1220,00</td></tr><tr><td>04/02/2025</td><td>1200,00</td><td>1220,00</td></tr><tr><td>03/02/2025</td><td>1205,00</td><td>1225,00</td></tr><tr><td>03/02/2025</td><td>1200,00</td><td>1220,00</td></tr><tr><td>03/02/2025</td><td>1200,00</td><td>1220,00</td></tr></tbody>  </table>"""

# Procesar HTML con BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Buscar la tabla
tabla = soup.find("table")

# Extraer datos de la tabla
datos = []
filas = tabla.find("tbody").find_all("tr")

for fila in filas:
    celdas = fila.find_all("td")
    if len(celdas) >= 3:
        fecha = celdas[0].text.strip()
        compra = celdas[1].text.strip().replace(",", ".")
        venta = celdas[2].text.strip().replace(",", ".")
        datos.append([fecha, float(compra), float(venta)])

# Convertir a DataFrame
df = pd.DataFrame(datos, columns=["Fecha", "Compra", "Venta"])

# Convertir la fecha al formato correcto
df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d/%m/%Y")

# Mostrar el DataFrame
print(df)


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# 📌 PASO 1: Asegurar que las fechas están bien en el DataFrame
df = df.sort_values(by="Fecha")  # Ordenar por fecha
df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d/%m/%Y")  # Convertir la fecha correctamente
df.set_index("Fecha", inplace=True)  # Usar fecha como índice

# Tomamos la columna de "Venta" como la referencia para el análisis
precios = df["Venta"]

# 📌 PASO 2: Visualización de la serie temporal corregida
plt.figure(figsize=(12,6))
plt.plot(precios.index, precios.values, label="Cotización Histórica")
plt.xlabel("Fecha")
plt.ylabel("Precio de Venta ($ARS)")
plt.title("Evolución de la Cotización")
plt.xticks(rotation=45)  # Rotamos etiquetas para mejor visibilidad
plt.legend()
plt.show()

# 📌 PASO 3: Simulación de Paseo Aleatorio (Random Walk)
np.random.seed(42)  # Para reproducibilidad

dias_prediccion = 30  # Días a predecir
ultimo_precio = precios.iloc[-1]  # Última cotización conocida
media_rendimiento = precios.pct_change().dropna().mean()  # Rendimiento promedio
std_rendimiento = precios.pct_change().dropna().std()  # Volatilidad

simulacion_precios = [ultimo_precio]
fechas_prediccion = pd.date_range(start=precios.index[-1], periods=dias_prediccion+1, freq="D")

for _ in range(dias_prediccion):
    cambio_porcentual = np.random.normal(media_rendimiento, std_rendimiento)
    nuevo_precio = simulacion_precios[-1] * (1 + cambio_porcentual)
    simulacion_precios.append(nuevo_precio)

# Graficamos la simulación corregida
plt.figure(figsize=(12,6))
plt.plot(precios.index, precios.values, label="Cotización Histórica", color="blue")
plt.plot(fechas_prediccion, simulacion_precios, label="Simulación Random Walk", linestyle="dashed", color="red")
plt.xlabel("Fecha")
plt.ylabel("Cotización ($ARS)")
plt.title("Simulación de Random Walk")
plt.xticks(rotation=45)
plt.legend()
plt.show()

# 📌 PASO 4: Predicción usando ARIMA
modelo = ARIMA(precios, order=(5,1,0))  # Modelo ARIMA con parámetros básicos
modelo_entrenado = modelo.fit()
predicciones = modelo_entrenado.forecast(steps=dias_prediccion)

# Crear fechas futuras para la predicción
fechas_futuras = pd.date_range(start=precios.index[-1], periods=dias_prediccion, freq="D")

# Graficamos la predicción ARIMA corregida
plt.figure(figsize=(12,6))
plt.plot(precios.index, precios.values, label="Cotización Histórica", color="blue")
plt.plot(fechas_futuras, predicciones, label="Predicción ARIMA", linestyle="dashed", color="green")
plt.xlabel("Fecha")
plt.ylabel("Cotización ($ARS)")
plt.title("Predicción de la Cotización con ARIMA")
plt.xticks(rotation=45)
plt.legend()
plt.show()

# 📌 PASO 5: Mostrar Resultados
print("📈 Predicción de la cotización para los próximos días:")
print(pd.DataFrame({"Fecha": fechas_futuras, "Predicción": predicciones}))

