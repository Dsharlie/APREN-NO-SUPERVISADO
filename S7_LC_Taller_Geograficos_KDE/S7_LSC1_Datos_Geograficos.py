#!/usr/bin/env python
# coding: utf-8

# <div >
# <img src = "figs/ans_banner_1920x200.png" />
# </div>

# # Datos Espaciales. Fundamentos teóricos. 
# 
# Este *cuaderno* trata sobre datos espaciales. El objetivo del *cuaderno* es que usted aprenda a leer y obtener datos espaciales, identificar, proyectar, organizar, procesar y graficar datos espaciales usando `Python`.
# 
# **NO** es necesario editar el archivo o hacer una entrega. Sin embargo, los ejemplos contienen celdas con código ejecutable (`en gris`), que podrá modificar  libremente. Esta puede ser una buena forma de aprender nuevas funcionalidades del *cuaderno*, o experimentar variaciones en los códigos de ejemplo.

# ## Introducción
# 
# 
# El análisis espacial es la rama de la estadística que se enfoca en el análisis de datos con propiedades espaciales, dentro de esto, encontramos a las coordenadas geográficas o topológicas. Se parece al análisis de series de tiempo en el punto en que el objetivo es analizar datos que cambian a lo largo de alguna dimensión. En el análisis de series de tiempo, los datos cambian a través de la dimensión del tiempo; mientras que en la estadística espacial, los datos cambian a lo largo de la dimensión espacial. 
# 
# Al igual que con la mayoría de los análisis estadísticos, en el análisis espacial, se trata de utilizar muestra de datos geográficos, utilizarlos para generar conocimientos y hacer predicciones. Por ejemplo, la estadística espacial se utiliza mucho para analizar el crimen. Al recopilar datos de ubicación de hechos delictivos, podemos generar mapas con áreas de alta y baja probabilidad de crimen, y así ayudar a los especialistas a determinar dónde es probable que ocurran futuros crímenes.
# 

# ## Tipos de Datos Espaciales
# 
# Los datos espaciales vienen en muchas "formas" y "tamaños", los tipos más comunes de datos espaciales son:
# 
# - **Punto**: son la forma más básica de datos espaciales. Denota una ubicación de un sólo punto, como una parada de bus, un edificio, o cualquier otro objeto discreto definido en el espacio.
# 
# - **Líneas**: son un conjunto de puntos ordenados, conectados por segmentos de recta.
# 
# - **Polígonos**: denotan un área y pueden pensarse como una secuencia de puntos conectados, donde el primer punto es el mismo que el último. 
# 
# - **Grillas (*o raster*)**: son una colección de puntos o celdas rectangulares, organizadas en una red regular.
# 
# En este *cuaderno* nos concentraremos en las tres primeras formas: puntos, líneas y polígonos (pero te invito a que explores por ti mismo los formatos de grilla). Los dos formatos de archivos más utilizados para este tipo de datos son `shapefiles` y `geojson`. Estos formatos tienen algunas particularidades y por lo tanto es necesario que dediquemos parte de este cuaderno a explicarlas.
# 
# ### Shapefiles
# 
# Los datos geoespaciales a menudo se almacenan en archivos `shapefile`. Este tipo de archivos almacena geometría no topológica, e información de atributos para las características espaciales en un conjunto de datos. Además, no requieren mucho espacio en disco, y son fáciles de leer y escribir (ESRI, 1998).
# 
# A diferencia de los archivos de texto que suelen ser autónomos y se componen de un único archivo, muchos formatos espaciales se componen de varios archivos. Los `shapefiles` están compuestos por tres o más archivos que deben conservar el mismo NOMBRE, y almacenarse en el mismo directorio (carpeta) de archivos para poder trabajar con ellos. Este formato de archivos suele ser muy utilizados por agencias gubernamentales para distribuir datos espaciales.
# 
# Los tres archivos principales asociados a `shapefiles` son:
# 
#    - Archivo principal: `file.shp`, es el archivo que contiene las geometrías.
#    - Archivo de índice: `file.shx`, el archivo que indexa la geometría.
#    - Tabla dBASE: `file.dbf`, es el archivo que almacena los atributos de las geometrías en un formato tabular.
# 
# Algunas veces los `shapefile` contienen archivos secundarios como:
# 
#    - Archivo de proyección: `file.prj`, contiene información sobre el sistema de coordenadas y la información de proyección. Es un archivo de texto sin formato que describe la proyección utilizando el formato de texto WKT.
#    - Archivos de índice opcionales: `file.sbn` y `file.sbx`, estos son archivos índices que optimizan las búsquedas espaciales.
#     - Archivo de metadatos: `file.shp.xml`, contiene los metadatos geoespaciales en formato XML (por ejemplo, ISO 19115 o formato XML).
#     
# Nuevamente es importante reiterar que cuando trabajemos con un shapefile, debemos mantener juntos todos los tipos de archivo asociados. Y al compartirlos, *es importante comprimir todos estos archivos en un sólo paquete antes de enviárselo*

# ### GeoJSON
# 
# GeoJSON es otro formato muy popular para datos espaciales, se basa en un estándar abierto y los archivos terminan en extensiones con `.geojson` o `.json`. El código, a continuación muestra cómo representaríamos la ubicación de un punto, como ser la ubicación de la Universidad de Los Andes, en el formato GeoJSON. El formato nos dice que es de tipo punto (`Point`) y especificamos las coordenadas (`coordinates`): latitud de 4.601590 y longitud de -74.066391. Finalmente, incluye un atributo de nombre (`name`) cuyo valor es: Universidad de Los Andes.
# 
# `
# {
#   "type": "Feature",
#   "geometry": {
#     "type": "Point",
#     "coordinates": [-74.066391, 4.601590]
#   },
#   "properties": {
#     "name": "Universidad de Los Andes"
#   }
# }
# `
# 
# Además de puntos, uno puede representar en GeoJSON líneas y polígonos. Una de las ventajas de este formato es la simplicidad y facilidad de lectura, que permite editarlos en cualquier editor de texto simple.
# 
# Antes de ver cómo manejamos estos formatos en `Python` es importante hacer la aclaración que en el formato GeoJSON y Shapefile las coordenadas están ordenadas "al revés" como longitud-latitud a diferencia de otras herramientas como ser Google Maps, que pone los formatos latitud-longitud. Por ejemplo, la Universidad de Los Andes está ubicada en (-74.066391, 4.601590) según GeoJSON y Shapefile, pero (4.601590,-74.066391) según Google Maps. Ninguna de las formas es la correcta o equivocada, simplemente son distintas, y es importante saber con la que uno está trabajando. En esta [tabla](https://macwright.com/lonlat/) (MacWright, 2022) podemos ver como se ordenan las mismas en los distintos formatos.

# ## Trabajando con datos espaciales en `Python`
# 
# Para el trabajo con datos espaciales en `Python`, vamos a utilizar la librería [geopandas](https://geopandas.org/), que permite trabajar con datos geoespaciales de una forma relativamente sencilla. [Geopandas](https://geopandas.org/) combina las capacidades de análisis de datos de [pandas](https://pandas.pydata.org/pandas-docs/stable/) con otras librerías como [shapely](https://shapely.readthedocs.io/en/stable/manual.html) y [fiona](https://fiona.readthedocs.io/en/latest/manual.html) que sirven para manejar datos espaciales. 
# 
# Las principales estructuras de datos en [geopandas](https://geopandas.org/) son `GeoSeries` y `GeoDataFrame`, que amplían las capacidades de Series y DataFrames de [pandas](https://pandas.pydata.org/pandas-docs/stable/).  La principal diferencia entre `GeoDataFrames` y [pandas](https://pandas.pydata.org/pandas-docs/stable/) `DataFrames` es que un `GeoDataFrame` debe contener (al menos) una columna para geometrías. Por defecto, el nombre de esta columna es `geometry`. La columna de geometría es una `GeoSeries` que contiene las geometrías (puntos, líneas, polígonos, etc.) como objetos con forma.
# 
# Para ilustrar el manejo usaremos bases de datos que provienen de los [datos abiertos de Bogotá](https://datosabiertos.bogota.gov.co) y están disponibles en la carpeta de `data`.
# 
# 
# ### Visualizaciones estáticas
# 
# #### Visualizando puntos
# 
# Comenzaremos visualizando la ubicación de los Establecimiento de Gastronomía y Bar en Bogotá D.C.:

# In[1]:


#Cargamos geopandas que es la librería a utilizar
import geopandas as gpd

#Cargamos los datos de establecimientos
bares = gpd.read_file("data/egba") 

# Vemos las primeras líneas 
bares.head()


# Esta base contiene la subcategoría a la que el establecimiento pertenece, el nombre, la dirección, la localidad, el sector, la latitud y longitud, y por último la geometría que nos dice que son puntos, y están en el formato longitud-latitud. Podemos ver también cierta información básica sobre este `GeoDataFrame` con la función `info`:

# In[2]:


bares.info()


# Para visualizar los bares podemos simplemente usar la función `plot()`, donde se puede ver que la base representa puntos a lo largo de latitud y longitud.

# In[3]:


bares.plot()


# Podemos mejorar esta gráfica usando `matplotlib`:

# In[4]:


import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize = (6, 6), dpi = 100)
bares.plot(kind = 'scatter', x = 'LONGITUD', y = 'LATITUD', ax = ax);


# #### Visualizando líneas
# 
# De la misma forma podemos visualizar líneas, por ejemplo las ciclovías de Bogotá:

# In[5]:


ciclovias = gpd.read_file("data/Ciclovia")
ciclovias.head()


# Este archivo por ejemplo sólo contiene las líneas sin información adicional. Haciendo la gráfica tenemos: 

# In[6]:


fig, ax = plt.subplots(figsize = (6, 6), dpi = 100)
ciclovias.plot(ax = ax);


# #### Visualizando polígonos
# 
# Para visualizar polígonos procedemos de la misma forma. En este caso vamos a visualizar las Unidades de Planeamiento Local (UPL) de Bogotá:

# In[7]:


upla = gpd.read_file("data/upla")


# In[8]:


fig, ax = plt.subplots(figsize = (12, 8), dpi = 100)
upla.plot(ax = ax);


# Este archivo contiene variada información sobre las UPL, entre ellas su área:

# In[9]:


upla.head()


# ¿Qué podemos utilizar para graficar? Por ejemplo escoger el color de relleno de los polígonos según su área (contenida en la variable `UPlArea`). Para esto usaremos el argumento `column` para escoger la columna que va a definir el color de los polígonos y el argumento `legend=True` para visualizar qué significa el color de relleno.

# In[10]:


fig, ax = plt.subplots(figsize = (12, 8), dpi = 100)
upla.plot(ax = ax, column = "UPlArea", legend = True);


# #### Visualizando puntos, líneas, y polígonos
# 
# Podemos también combinar los gráficos anteriores y operar sobre las bases. Por ejemplo, combinemos visualizaciones de bares, ciclovías, y las UPL en la misma gráfica. Para apreciarlo mejor filtraremos tres localidades del sur de Bogotá que corresponden a la zona rural de la ciudad: Río Blanco, Río Sumapaz y Río Tunjuelo.

# In[11]:


fig, ax = plt.subplots(figsize = (12, 8), dpi = 100)
filtro = ~upla["UPlNombre"].str.contains("RIO")
upla.loc[filtro,:].plot(ax = ax, color = 'white', edgecolor = 'black');
ciclovias.to_crs(4686).plot(ax = ax, color = "red"); # Note que la ciclovía está en un sistema de
# coordenadas diferente a upla y bares por lo que se debe transformar (más de esto más abajo en el cuaderno)
bares.plot(ax = ax, markersize = 2, color = "blue");


# ## Adquiriendo datos espaciales abiertos: [OpenStreetMap](https://www.openstreetmap.org/)
# 
# 
# OpenStreetMap (OSM) es probablemente la base de datos espacial abierta más conocida y ampliamente utilizada en el mundo. Esta base, de licencia abierta y gratuita, contiene mapas e información geográfica construida por voluntarios alrededor del mundo.
# 
# Veremos en esta sección cómo podemos recuperar datos de OSM utilizando la librería `pirosm`. OSM es una "base de datos del mundo", y por lo tanto contiene información sobre varias cosas: Con `pirosm` se pueden descargar y extraer datos  sobre:
# 
#    - Calles, con la función `osm.get_network()`
#    - Edificios, con la función `osm.get_buildings()`
#    - Puntos de interés, con la función `osm.get_pois()`
#    - Uso de la tierra, con la función `osm.get_landuse()`
#    - Elementos naturales, con la función `osm.get_natural()`
#    - Fronteras, con la función `osm.get_boundaries()`
# 
# Para ilustrarlo descarguemos los supermercados en Bogotá:

# In[12]:


from pyrosm import OSM, get_data

# Bajamos los datos para  Bogotá
fp = get_data("Bogota")

# Inicializamos el lector para Bogotá
osm = OSM(fp)


# In[13]:


#Obtenenemos los supermecados
super = osm.get_pois(custom_filter={"shop":["supermarket"]})
len(super)


# In[14]:


super.head()


# Obtuvimos datos de 1622 supermercados con su ubicación en la ciudad, que podemos también agregar a nuestro mapa anterior. Notemos además que esta base contiene tanto puntos como polígonos.

# In[15]:


fig, ax = plt.subplots(figsize = (12, 8), dpi = 100)
filtro = ~upla["UPlNombre"].str.contains("RIO")
upla.loc[filtro,:].plot(ax = ax, color = 'white', edgecolor = 'black');
ciclovias.to_crs(4686).plot(ax = ax, color = "red"); 
bares.plot(ax = ax, markersize = 2, color = "blue");
super.plot(ax = ax, markersize = 2, color = "green");


# ## Proyecciones geográficas
# 
# 
# La Tierra no es plana. El mundo es un elipsoide de forma irregular, pero los dispositivos en los que representamos los mapas tienen sólo dos dimensiones. Para representar la Tierra, se la proyecta en un mapa plano. 
# 
# La proyección cartográfica elegida determinará cómo se transforman y distorsionan latitudes y longitudes para preservar algunas de las propiedades del mapa: área, forma, distancia, dirección o rumbo. Por ejemplo, los marineros usan la proyección de Mercator donde los meridianos y los paralelos se cruzan entre sí siempre en el mismo ángulo de 90 grados. Les permite ubicarse fácilmente en la línea que muestra la dirección en la que navegan. Pero la proyección no conserva las distancias. 
# 
# El siguiente `.gif` ilustra cómo la proyección Mercator "aplana" la tierra:

# In[1]:


from IPython.display import IFrame
IFrame('figs/Projections.gif', width=700, height=350)


# Entonces, las proyecciones cartográficas intentan representar la superficie de la tierra o una parte de ella, en una superficie plana de papel o en la pantalla del computador.
# 
# El sistema de coordenadas de referencia (o `CRS` por sus siglas en ingles) define con la ayuda de las coordenadas, cómo la representación bidimensional de la tierra se relaciona con la ubicación real en la tierra. 
# 
# Existen varios `CRS` y la elección dependerá de lo que se quiere hacer. Roger Bivand y coautores (2013)  plasman esto de manera muy clara: “No existen proyecciones para todos los propósitos, todas implican distorsión cuando están lejos del centro del marco especificado” 
# 
# Por ejemplo tenemos sistemas de coordenadas que abarcan todo el globo terráqueo y sirven para ubicar cualquier punto de la Tierra sin necesitar otro punto de referencia. El más popular es el WGS84 (World Geodetic System 1984), cuyo código EPSG: 4326 (EPSG es un registro público con todas las proyecciones y su respectivo código).
# 
# Por otro lado, los sistemas de coordenadas proyectadas que se focalizan le dicen al computador cómo graficar en usa superficie plana para minimizar la distorsión visual en una región particular. Por ejemplo, para Colombia se recomienda utilizar el  MAGNA-SIRGAS cuyo código EPSG : 4626.
# 
# 
# Volviendo un poco a las bases anteriores, notemos que las latitudes y longitudes, de las ciclovías están expresadas de forma diferente que el resto. Esto se debe a que están en una proyección diferente. ¿Cómo podemos ver en que proyección están los datos? Para ello usamos la función `.crs`:

# In[17]:


ciclovias.crs


# En este caso, están en Pseudo-Mercator (EPSG: 3857) mientras que la base de bares está en la proyección recomendada para Colombia: MAGNA-SIRGAS

# In[18]:


bares.crs   


# Para poder graficar y trabajar con estas bases es importante siempre verificar las proyección en la que se encuentran y homogeneizarlas, para ello se puede usar la función `.to_crs`:

# In[19]:


ciclovias=ciclovias.to_crs(4686)
ciclovias.crs


# Esto será especialmente importante para medir distancias.

# ## Midiendo distancias
# 
# Cuando trabajamos con datos geográficos a menudo nos va a interesar medir distancias, esto será especialmente importante cuando queremos agrupar datos y encontrar "puntos calientes". Para demostrarlo, generaremos datos espaciales, creando primero un `DataFrame` con [pandas](https://pandas.pydata.org/pandas-docs/stable/) y luego transformarlo a un `GeoDataFrame` de [geopandas](https://geopandas.org/).
# 
# Para nuestro ejemplo vamos a medir la distancia entre la Universidad de Los Andes y el Banco de la República. Entonces primero generamos el DataFrame que tiene columnas: lugar, latitud y longitud.
# 

# In[20]:


import pandas as pd
db = pd.DataFrame({
    "lugar": ["Uniandes", "Banco de la República"],
    "lat": [4.601590, 4.602151],
    "long": [-74.066391, -74.07221]
    })
db


# Lo transformamos a un `GeoDataFrame` especificando que la geometría son puntos que surgen de la latitud y longitud:

# In[21]:


db = gpd.GeoDataFrame(db, geometry = gpd.points_from_xy(db.long, db.lat))
db


# Definimos la proyección WGS84, ya que tenemos la latitudes y longitudes que los ubican en el mapa, pero luego lo proyectamos a MAGNA-SIRGAS para tener la proyección que corresponde a Bogotá.

# In[22]:


db.crs = "EPSG:4326"
db=db.to_crs(4686)


# Antes de calcular la distancia, grafiquemos las ubicaciones en sus respectivas UPLs.

# In[23]:


fig, ax = plt.subplots(figsize = (12, 8), dpi = 100)
# La Universidad de los Andes y el Banco de la República quedan en las localidades 
filtro = upla.UPlNombre.isin(["LA CANDELARIA", "LAS NIEVES"])
upla.loc[filtro,:].plot(ax = ax, color = "white", edgecolor = "black");
db.plot(ax = ax, color = "red");

# Para poder crear una marcación de los lugares necesitamos desempaquetar la geometría
db["coordenadas"] = db["geometry"].apply(lambda x: x.representative_point().coords[:][0])
for idx, fila in db.iterrows():
    plt.annotate(text = fila['lugar'], xy = fila['coordenadas'], 
        textcoords = 'offset points', xytext = (0, 10), ha = 'right',
        bbox = dict(boxstyle = "round", fc = "white"))


# Para calcuar la distancia   entre Uniandes y el Banco de la República vamos a utilizar la función `geodesic` del modulo `diastance` de la librería [geopy](https://geopy.readthedocs.io/en/stable/). [Geopy](https://geopy.readthedocs.io/en/stable/) es un cliente de `Python` que permite acceder a servicios web de geocodificación populares y facilita el cálculo de distancias entre ubicaciones. La función [geodesic](https://geopy.readthedocs.io/en/stable/#module-geopy.distance) calcula distancia geodésica es la distancia más corta en la superficie de un modelo elipsoidal de la tierra, como ser el WGS84. Debido a que hay varios modelos elipsoidales populares, [geodesic](https://geopy.readthedocs.io/en/stable/#module-geopy.distance) usa por defecto WGS84, sin embargo la precisión va a depender de la posición en el elipsoide donde se encuentren los puntos, por ello la importancia de usar la proyección  MAGNA-SIRGAS:

# In[24]:


from geopy.distance import geodesic

coords_1 = db.coordenadas[0]
coords_2 = db.coordenadas[1]

# calculo la distancia geodésica
geodesic(coords_1, coords_2).m


# [Geopy](https://geopy.readthedocs.io/en/stable/) nos dice entonces que la distancia entre el Banco de la República y Uniandes es aproximadamente 650 metros. Esta distancia es aproximadamente la misma que obtenemos si la medimos directamente en  [Google Maps](https://www.google.com/maps/dir/4.602146,+-74.07221/4.601590,+-74.066391/@4.6013775,-74.0736601,16z/data=!3m1!4b1!4m10!4m9!1m3!2m2!1d-74.07221!2d4.602146!1m3!2m2!1d-74.066391!2d4.60159!3e2)

# ![distancia_uniandes_banco](figs/distancia.png)

# El cálculo de distancias no se limita sólo a calcular la distancia entre dos puntos, podemos también hacerlo entre puntos y líneas. Por ejemplo, podemos calcular la distancia de Uniandes y el BanRep a las ciclovías.  Como vamos a calcular la distancia de una línea a un punto, primero calculamos el punto perteneciente a la línea que está más cercano al punto. A modo de ilustración mostraremos el punto más cercano de la primera ciclovía a Uniandes.
# 
# Para encontrar el punto más cercano usamos la función `nearest_points` de [shapely](https://shapely.readthedocs.io/en/stable/manual.html):

# In[25]:


from shapely.ops import nearest_points

ciclovia = ciclovias.geometry[0]
uniandes = db.geometry[0]
punto_cercano = nearest_points(ciclovia, uniandes)[0]
punto_cercano.coords[:][0]


# Encontrado el punto más cercano, hagamos una gráfica, que nos muestre la primer ciclovia, el punto más cercano a Uniandes (estrella azul) y Uniandes (circulo amarillo):

# In[26]:


fig, ax = plt.subplots(figsize = (12, 8), dpi = 100)
filtro = ~upla["UPlNombre"].str.contains("RIO")
upla.loc[filtro,:].plot(ax = ax, color = 'white', edgecolor = 'black');
ciclovias.iloc[0:1,:].plot(ax = ax, color = "red"); 
plt.plot(*uniandes.coords[:][0], "*", color = "b", markersize = 10);
plt.plot(*punto_cercano.coords[:][0], color = "yellow", markersize = 10);


# Y calculemos la distancia:

# In[27]:


coords_1 = [[punto_cercano.coords[:][0][1], punto_cercano.coords[:][0][0]]]
coords_2 = [[uniandes.coords[:][0][1], uniandes.coords[:][0][0]]]

geodesic(coords_1, coords_2).km


# La distancia entre Uniandes y la ciclovía es de 4.4 kilómetros.  Un punto importante a notar es que [geopandas](https://geopandas.org/) guarda las coordenadas como (lon, lat), pero  [geopy](https://geopy.readthedocs.io/en/stable/) las interpreta  al revés (lat, lon).
# 
# Calculemos ahora todas las distancias entre el punto más cercano de cada ciclovía a Uniandes y el Banco de la República. Almacenaremos estas distancias en el `DataFrame: distancias`

# In[28]:


def calculate_all_distances(df, ciclovias):
    all_distances = []
    for i in range(len(df)):
        point = df.iloc[i]['geometry']
        for j in range(len(ciclovias)):
            ciclovia = ciclovias.iloc[j]['geometry']
            nearest_geoms = nearest_points(point, ciclovia)
            nearest_point = nearest_geoms[1]
            distance = geodesic((point.y, point.x), (nearest_point.y, nearest_point.x)).km
            all_distances.append({'lugar': df.iloc[i]['lugar'], 'ciclovia': j, 'distance': distance})
    return pd.DataFrame(all_distances)

distancias = calculate_all_distances(db, ciclovias)
distancias


# Tenemos entonces todas las distancias entre Uniandes y el BanRep, y los puntos más cercanos de las ciclovías.

# ## Uniones espaciales
# 
# Otra operación que usamos a menudo, es  la unión espacial. Siguiendo el ejemplo anterior, supongamos que queremos agregar una columna a nuestra `db` que indique la UPL a la cual pertenecen. Para esto podemos usar una unión espacial que va a unir la información entre dos bases espaciales.
# 
# Para esta operación utilizaremos la función `sjoin()`:

# In[29]:


upla.crs


# In[30]:


db.crs


# In[31]:


union = gpd.sjoin(db, upla)

union


# Se crearon nuevas columnas con la información de las UPLs. Para Uniandes aparece que está en La Candelaria y para el BanRep en Las Nieves.

# ## Visualizaciones interactivas
# 
# `Python` ofrece además la capacidad de generar visualizaciones interactivas, en esta sección usaremos la librería [folium](https://pypi.org/project/folium/) ) para generar estas visualizaciones. Esta librería requiere que primero especifiquemos la capa base del mapa y luego se le agreguen las capas deseadas:

# In[2]:


#importamos la librería
import folium

#Mapa base
map = folium.Map(location = [4.65283,-74.054339], tiles = "OpenStreetMap", zoom_start = 10)
# Otras opciones de tiles
#Stamen Terrain, Toner, and Watercolor

#capa bares
for i in range(0,len(bares)):
   folium.Marker(
      location=[bares.iloc[i]['LATITUD'], bares.iloc[i]['LONGITUD']],
       popup=bares.iloc[i]['NOMBRE_EST'],
   ).add_to(map)


#Display el mapa
map


# Podemos también agregar la capa de los polígonos de las UPL:

# In[33]:


#Primero removemos las UPL cuyo nombre contienen Rio
upla_filt=upla.loc[~upla["UPlNombre"].str.contains("RIO"),:]

#Agregamos la capa de polígonos con un popup con el nombre de la UPL
for _, r in upla_filt.iterrows():
    sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j,
                           style_function=lambda x: {'fillColor': '#FFFFFF'})
    folium.Popup(r['UPlNombre']).add_to(geo_j)
    geo_j.add_to(map)

map


# Finalmente agregamos la ciclovías:

# In[34]:


#Agregamos la capa de lineas para las ciclovias
ciclo=ciclovias.to_crs(4686)

folium.Choropleth(
 ciclo,
    line_weight=2,
    line_color='red'
).add_to(map)

map


# [Folium](https://pypi.org/project/folium/) entonces nos permite con facilidad ubicar nuestros datos en un mapa interactivo. Notemos que omití graficar los supermercados, esto se debe a que al ser más de 1000 datos le puede tomar a [folium](https://pypi.org/project/folium/) un tiempo considerable. Para superar esto una buena alternativa  es [bokeh](https://bokeh.org/), un submódulo de la librería [datashader](https://datashader.org/), que exploraremos en un proximo cuaderno. (Te invito que explores este  [enlace](https://anaconda.org/jbednar/nyc_taxi/notebook) para ver más detalles sobre este submódulo)
# 

# # Referencias
# 
# - Bivand, R. S., Pebesma, E. J., Gómez-Rubio, V., & Pebesma, E. J. (2008). Applied spatial data analysis with R (Vol. 747248717, pp. 237-268). New York: Springer.
# - Dougherty, J., & Ilyankou, I. (2021). "Hands-On Data Visualization".  O'Reilly Media, Inc.
# - ESRI, Environmental Systems Research Institute. (1998). “ESRI Shapefile Technical Description.” Disponible en: https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf. Accedido el 04/02/2022
# - MacWright, T. "lon lat lon lat". Disponible en https://macwright.com/lonlat/. Accedido el 04/02/2022
# - Tenkanen, H. "Spatial data science for sustainable development". Disponible en https://sustainability-gis.readthedocs.io/en/latest/index.html. Accedido el 04/02/2022

# # Información de Sesión

# In[35]:


import session_info

session_info.show(html=False)

