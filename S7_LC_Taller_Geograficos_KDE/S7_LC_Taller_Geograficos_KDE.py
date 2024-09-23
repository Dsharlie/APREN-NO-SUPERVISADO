#!/usr/bin/env python
# coding: utf-8

# <div >
# <img src = "figs/ans_banner_1920x200.png" />
# </div>

# # Caso-taller:  Analizando el Delito en Chicago

# En este caso-taller vamos a utilizar datos geográficos y estimación de densidad de kernel para analizar delitos en Chicago. Esta ciudad es muy famosa no sólo por haber sido el hogar del mafioso Al Capone, sino también por sus altas tasas de delitos. 
# 
# Para este taller obtuve datos del portal de la [ciudad de Chicago](https://www.chicago.gov/city/en/dataset/crime.html). La base de datos fue traducida y modificada para nuestras necesidades. Esta contiene todos los homicidios y robos que sucedieron entre el 1 de junio y el 31 de agosto de 2019.
# 

# ## Instrucciones generales
# 
# 1. Para desarrollar el *cuaderno* primero debe descargarlo.
# 
# 2. Para responder cada inciso deberá utilizar el espacio debidamente especificado.
# 
# 3. La actividad será calificada sólo si sube el *cuaderno* de jupyter notebook con extensión `.ipynb` en la actividad designada como "entrega calificada por el personal".
# 
# 4. El archivo entregado debe poder ser ejecutado localmente por el tutor. Sea cuidadoso con la especificación de la ubicación de los archivos de soporte, guarde la carpeta de datos en el mismo `path` de su cuaderno, por ejemplo: `data`.

# ## Desarrollo
# 

# ### 1.Carga de datos 
# 
# #### 1.1. Delitos
# 
# En la carpeta `data` se encuentra el archivo `Chicago_delitos_verano_2019.csv` cargue estos datos en su *cuaderno*. Describa brevemente el contenido de la base.

# In[ ]:


# Utilice este espacio para escribir el código.


# (Utilice este espacio para describir su procedimiento)

# #### 1.2. Barrios de Chicago
# 
# También en la carpeta `data` se encuentran los archivos con los polígonos de las áreas comunitarias en un archivo comprimido llamado `Areas_comunitarias_Chicago.zip`. Genere un mapa interactivo con un popup con el nombre del area comunitaria.

# In[ ]:


# Utilice este espacio para escribir el código.


# (Utilice este espacio para describir su procedimiento).

# ### 2.   Análisis distribución del crimen por barrios
# 
# #### 2.1.  Genere una tabla descriptiva donde se muestra el número total de delitos, el número total de robos y el número total de homicidios, y como porcentaje de total por barrios. La tabla debe contener ademas una fila final donde se muestre el total para la ciudad. Describa los resultados que obtiene.
# 

# In[ ]:


# Utilice este espacio para escribir el código.


# (Utilice este espacio para describir el procedimiento, análisis, y conclusiones)

# #### 2.2. Genere una gráfica de dispersión entre el total de homicidios y robos por barrios. Incluya en la gráfica la recta de regresión que mejor ajusta a esos datos. Describa los resultados que obtiene.

# In[ ]:


# Utilice este espacio para escribir el código.


# (Utilice este espacio para describir el procedimiento, análisis, y conclusiones)

# ### 3. Distribución espacial del delito
# 
# #### 3.1 Distribución respecto al centro de la ciudad
# 
# Tomando como centro de la ciudad las coordenadas (-87.627800, 41.881998), estime funciones de densidad que muestren gráficamente el gradiente del total de robos, y homicidios, como función de la distancia al centro de la ciudad. Explique cómo midió las distancias incluyendo que medida de distancia utilizó. Para elegir el ancho de banda y la función de kernel más apropiados utilice validación cruzada usando todas las opciones posibles de kernel. Describa los resultados que obtiene.

# In[ ]:


# Utilice este espacio para escribir el código.


# (Utilice este espacio para describir el procedimiento, análisis, y conclusiones)

# ### 3.2 Puntos calientes en la ciudad
# 
# Usando `statsmodels` implemente la estimación de densidad bivariada para el total de robos y el total de homicidios. Muestre los resultados usando curvas de nivel en una visualización interactiva. Compare los resultados de estimar usando los anchos de banda: `normal_reference` y `cv_ml`. Explique en que consisten ambas formas de estimar el ancho de banda. Comente sobre los puntos calientes encontrados bajo ambos métodos y su ubicación en la ciudad. (Esto puede tomar mucho tiempo y requerir mucha capacidad computacional, puede aprovechar los recursos de [Google Colab](https://colab.research.google.com/))

# In[ ]:


# Utilice este espacio para escribir el código.


# (Utilice este espacio para describir el procedimiento, análisis, y conclusiones)

# ## 4. Explicando la ubicación del delito
# 
# El objetivo de este punto es encontrar posibles correlaciones  entre el crimen y características de la ciudad. Para ello, utilice los datos de OpenStreetMap y explore si existe una correlación entre el porcentaje del área de la comunidad  dedicado a tiendas (`retail`)  y comercios (`commercial`) y el número total de robos y homicidios en esa comunidad. Ofrezca una explicación intuitiva de por qué cree que aparecen estas correlaciones. (Esto puede tomar mucho tiempo y requerir mucha capacidad computacional, puede aprovechar los recursos de [Google Colab](https://colab.research.google.com/))

# In[ ]:


# Utilice este espacio para escribir el código.


# (Utilice este espacio para describir el procedimiento, análisis, y conclusiones)
