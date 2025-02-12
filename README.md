# Contexto:
Buscamos obtener los datos históricos de la cotización del dólar blue en Argentina utilizando 
web scraping con Python. Sitios como Ámbito. Una vez obtenidos los datos, es importante realizar un análisis exploratorio para comprender su comportamiento estadístico, para mas adelante simular un paseo aleatorio que represente posibles trayectorias futuras de la cotización del dólar.

La Simulación de Random Walk se encuentra en la parte PASO 3
Donde toma el último precio registrado (ultimo_precio = precios.iloc[-1]).
, calcula el rendimiento promedio diario (media_rendimiento = precios.pct_change().dropna().mean()).
, computamos la volatilidad (desviación estándar) (std_rendimiento = precios.pct_change().dropna().std()).
y simula cada día futuro. En este código se genera un cambio porcentual aleatorio basado en una 
distribución normal (np.random.normal(media_rendimiento, std_rendimiento)), 
luego calcula el nuevo precio multiplicando el anterior por (1 + cambio_porcentual), 
para finalmente agregar el nuevo precio a la lista de simulaciones

# Instalar y activar el entorno virtual
/virtualenv env         /env/Scripts/activate.bat

# requerimientos:

pip install requests 

pip install beautifulsoup4

pip install statsmodels

pip install matplotlib

pip install pandas

pip install statsmodels 

# Libreria
https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.html