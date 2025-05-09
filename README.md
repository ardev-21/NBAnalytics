<!--h2 without bottom border-->
<div id="user-content-toc">
  <ul align="center">
    <summary><h2 style="display: inline-block"> Proyecto: NBAnalytic: Basket Science</h2></summary>
  </ul>
</div>

<!--horizontal divider(gradiant)-->
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

# ¡Hola! 👋 DAS - Data Analytics Athletic 👨‍💻 Un Equipo de 5 Analistas de Datos | 📊 Nahuel - Ariel - Frank - Mariano - Carlos.

<!--Intro start-->

## 📚 Objetivo del análisis:

### Buscando al mejor equipo de basket.

El propósito principal de este proyecto se enfoca en el ámbito del deporte profesional, específicamente en la NBA (Asociación Nacional de Baloncesto). En la actualidad, los equipos y analistas están inundados de datos que utilizan para evaluar el rendimiento de los jugadores, las estrategias y hacer predicciones sobre los partidos. Sin embargo, no todos los equipos cuentan con el mismo nivel de sofisticación en su análisis, lo que crea una brecha en la ventaja competitiva.

**Análisis del Basket Profesional:** El proyecto se centra en el análisis de datos en el contexto de la NBA, donde los equipos buscan mejorar el rendimiento y la toma de decisiones a través del uso de información estadística. Aunque hay una gran disponibilidad de datos, no todos los equipos tienen las mismas capacidades analíticas, lo que genera una desigualdad en la ventaja competitiva.

## 🛠 Tecnologías Usadas:

- Amazon RDS: Para el servidor de la base de datos.
- SQL Server: Restricciones y validaciones para garantizar la integridad de datos.
- Python: Limpieza y análisis exploratorio de datos.
  - Pandas
  - NumPy
  - Matplotlib / Seaborn
  - pyodbc
  - sqlalchemy
  - os
  - shutil
  - time
  - watchdog
  - dotenv
  - kaggle
- Jupyter Notebook

## 👨‍💻 Metodologías:

- Modelado Relacional (ER)
- Creación instancia con Amazon RDS
- Creación base de datos en Amazon RDS
- Análisis Exploratorio de Datos (EDA) “tratamiento de la base de datos en Python”
- Extracción, Transformación y Carga de datos (ETL) “Amazon RDS”
- Automatización de ingesta de datos

**Datos: Origen y Descripción**

- **Fuente:** Conjunto de datos "NBA Database" obtenido de Kaggle.
- **Contenido:**  - Estadísticas individuales por partido y por temporada (puntos, asistencias, rebotes, etc.).
                  - Datos de equipos (victorias, derrotas, efectividad ofensiva/defensiva).
                  - Datos de partidos (fecha, resultado, localía, alineaciones).
                  - Información avanzada (PER, Win Shares, BPM, etc.).
- **Métricas clave:** 
- **Enfoque:** Año 2000 – 2023.
- **Recolección de Datos:** Dataset descargado de Kaggle en formato CSV.

### Diseño del Modelo Entidad-Relación:

- **Tabla de hechos:** play_by_play
- **Tablas dimensionales:** player, team
- **Relaciones:** 1:N entre game y player, game y team.
- **Llaves:** Llaves primarias (PK) y foráneas (FK) garantizan consistencia.

### Limpieza y Análisis Exploratorio (EDA):

- Eliminación de valores nulos y columnas innecesarias.
- Filtro desde el año 2000 en adelante, por jugadores y equipos.

### Extracción, Transformación y Carga de datos (ETL):

- **Validación de Datos Python:** Eliminación de inconsistencias y valores atípicos.

### Automatización:

- Extracción automática de datos actualizados.
- Optimización para análisis en tiempo real.
- Importancia del Proceso Integración continua: Datos confiables y listos para análisis estratégico.

### Modelado de datos en DAX:

- Crear columnas calculadas.
- Definir medidas.
- Gestionar relaciones.
- Arreglar de tipos de datos.
- Crear tabla calendario.

### Dashboards

- Insights accionables: Permite visualizar patrones que ayuden a optimizar la gestión y rendimiento deportivo de la NBA.
- Incorporar formato personalizado en las visualizaciones como el tema, etiquetas, títulos y otros elementos de formato.
- Creación de gráficos, tablas y otros elementos visuales.
- Establecer la interactividad, filtros y segmentadores idóneos.

## 🚀Conclusiones:

- Alto éxito en la transición de jugadores drafteados a titulares.
- Costo por victoria promedio de la liga indica una eficiencia relativa en el gasto.
- Las alineaciones titulares muestran un balance ofensivo sólido en términos de eficiencia de tiro y asistencias.
- Un número significativo de lesiones históricas, con mayor incidencia en Guards y Forwards, siendo los esguinces de tobillo y dolor de rodilla las más comunes.
- La temporada 2021-22 fue la de mayor número de lesiones registradas.
- El dashboard ofrece una visión integral de factores como la edad del roster, desarrollo de jóvenes y rookies, estabilidad del equipo y retención de jugadores drafteados para analizar la construcción de franquicias exitosas a largo plazo.

