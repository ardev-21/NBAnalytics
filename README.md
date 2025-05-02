<!--h2 without bottom border-->
<div id="user-content-toc">
  <ul align="center">
    <summary><h2 style="display: inline-block"> Proyecto: NBAnalytic: Basket Science</h2></summary>
  </ul>
</div>

<!--horizontal divider(gradiant)-->
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

# ¡Hola! 👋 DAS - Data Analytics Solution 👨‍💻 Un Equipo de 5 Analistas de Datos | 📊 Nahuel - Ariel - Frank - Mariano - Carlos.

<!--Intro start-->

## 📚 Objetivo del análisis:

### Buscando al mejor equipo de basket.

El propósito principal de este proyecto se enfoca en el ámbito del deporte profesional, específicamente en la NBA (Asociación Nacional de Baloncesto). En la actualidad, los equipos y analistas están inundados de datos que utilizan para evaluar el rendimiento de los jugadores, las estrategias y hacer predicciones sobre los partidos. Sin embargo, no todos los equipos cuentan con el mismo nivel de sofisticación en su análisis, lo que crea una brecha en la ventaja competitiva.

**Análisis del stock del inventario de licores:** El proyecto se centra en el análisis de datos en el contexto de la NBA, donde los equipos buscan mejorar el rendimiento y la toma de decisiones a través del uso de información estadística. Aunque hay una gran disponibilidad de datos, no todos los equipos tienen las mismas capacidades analíticas, lo que genera una desigualdad en la ventaja competitiva.

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
- Jupyter Notebook

## 👨‍💻 Metodologías:

- Modelado Relacional (ER)
- Creación instancia con Amazon RDS
- Creación base de datos en Amazon RDS
- Análisis Exploratorio de Datos (EDA) “tratamiento de la base de datos en Python”
- Extracción, Transformación y Carga de datos (ETL) “carga de datos en GCP”
- Automatización de ingesta de datos
- Mockup

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

- **Tabla de hechos:** game
- **Tablas dimensionales:** player, team
- **Relaciones:** 1:N entre game y player, game y team.
- **Llaves:** Llaves primarias (PK) y foráneas (FK) garantizan consistencia.

### Limpieza y Análisis Exploratorio (EDA):

- Eliminación de valores nulos, filtro desde el año 2000 en adelante y columnas innecesarias.

### Extracción, Transformación y Carga de datos (ETL):

- **Validación de Datos Python:** Eliminación de inconsistencias y valores atípicos.

### Automatización:

- Extracción automática de datos actualizados.
- Optimización para análisis en tiempo real.
- Importancia del Proceso Integración continua: Datos confiables y listos para análisis estratégico.
- Escalabilidad: Infraestructura sólida para futuras expansiones.

### Mockup:

- Visualizar y entender los datos de manera más efectiva, facilitando la identificación de oportunidades de mejora y la implementación de estrategias más eficientes para la elección de futuros jugadores.
- Dar un panorama detallado de cómo va ser el resultado final de la propuesta.
