# TFM - Predicción de Resultados de Ensayos Clínicos mediante Machine Learning
**Autor:** Miquel Ribas  
**Máster Universitario en Ciencia de Datos (UOC)**  
**Versión del proyecto:** 2025  
**Lenguajes:** Python 3.11.14 / R opcional  
**Entorno:** Anaconda (entorno `tfm`)

---

## Descripción del proyecto
Este repositorio contiene el desarrollo completo del Trabajo Final de Máster (TFM), cuyo objetivo es **predecir resultados de ensayos clínicos** utilizando técnicas de **Machine Learning** aplicadas a datos extraídos de **ClinicalTrials.gov**.

El proyecto implementa un pipeline reproducible de ciencia de datos que cubre:

- Descarga automatizada de datos desde la API oficial.
- Preprocesamiento y tratamiento de valores faltantes.
- Entrenamiento de modelos base y avanzados (RandomForest, XGBoost, etc.).
- Evaluación rigurosa con métricas apropiadas para datos desbalanceados.
- Recursos para reproducir todos los experimentos.

---

## Estructura del proyecto

```text
tfm_clinicaltrials/
│
├── data/
│   ├── raw/          # Datos descargados directamente desde la API (snapshot)
│   ├── clean/      # Datos parcialmente procesados (limpieza inicial)
│   └── processed/    # Dataset final para modelado
│
├── notebooks/
│   ├── 00_data_download_check.ipynb
│   ├── 01_eda_clinicaltrials.ipynb
│   ├── 02_preprocessing_feature_engineering.ipynb
│
├── src/
│   ├── __init__.py
│   └── download_clinicaltrials.py   # Script para descargar datos desde la API
│
├── models/                          # Modelos entrenados (.pkl/.joblib)
│
├── reports/
│   ├── figures/                     # Gráficos para memoria / paper
│   └── tables/                      # Tablas exportadas
│
└── requirements.txt
````

---

## Instalación del entorno

1. Abrir **Anaconda Navigator**
2. Crear un entorno nuevo:

   * Nombre: `tfm`
   * Python: `3.11`
3. Instalar paquetes recomendados:

### Desde conda:

```bash
conda install pandas numpy scikit-learn matplotlib seaborn jupyterlab ipykernel
```

### Desde pip:

```bash
pip install xgboost shap imbalanced-learn statsmodels lightgbm
```

### Registrar kernel de Jupyter:

```bash
python -m ipykernel install --user --name tfm --display-name "TFM (T14)"
```

---

## Descarga de datos (API ClinicalTrials.gov)

Los datos se obtienen mediante el script:

```
src/download_clinicaltrials.py
```

Idealmente ejecutar el notebook 00_data_download_check.ipynb

Esto genera un snapshot reproducible en:

```
data/raw/clinicaltrials_raw_YYYYMMDD_HHMMSS.csv
```


---

## Flujo de trabajo (notebooks)

### **00 - Data Download & Raw Data Check**

* Ejecuta descarga desde API.
* Se analiza una muestra del archivo RAW.
* Se escogen que columnas usar y se descarga el dataset completo.
* Guarda un dataset *clean*.

### **01 - EDA (Exploratory Data Analysis)**

* Vista general del dataset.
* Análisis de valores faltantes.
* Distribuciones clave (fases, condiciones, estados, fechas).

### **02 - Preprocesamiento + Feature Engineering**

* Limpieza avanzada.
* Codificación categórica.
* Construcción de nuevas características relevantes.
* Generación del dataset final de modelado.
---

## Reproducibilidad

Este repositorio contiene:

* Versionado de entorno (`requirements.txt`)
* Snapshot de datos (`data/raw/`)
* Resultados y figuras (`reports/`)

Todos los experimentos pueden reproducirse ejecutando los notebooks en orden del 00 al 05.

---

## Licencia y uso

Los datos utilizados provienen de **ClinicalTrials.gov**, que permite su uso público con fines académicos.

El código es completamente libre para uso educativo y académico.

---

## Contacto

Para cualquier duda sobre este trabajo:

**Autor:** Miquel Ribas Portella (mribaspo@uoc.edu)
**Universitat Oberta de Catalunya (UOC)**

```
