"""
download_clinicaltrials.py (API v2, JSON)

Este script descarga los datos de ensayos clínicos de ClinicalTrials.gov mediante llamadas a la REST API v2 y guarda los datos en un CSV en data/raw/.

Se puede ejecutar este script desde la raíz del proyecto mediante: 
python -m src.download_clinicaltrials
"""

import time
from datetime import datetime
from pathlib import Path

import sys

import pandas as pd
import requests
import json

from tqdm import tqdm

# Endpoint principal de la API v2
BASE_URL = "https://clinicaltrials.gov/api/v2/studies"


def flatten_ensayo(ensayo):
    """Aplana TODO el JSON de un ensayo en un dict plano. Se emplea recursividad para ir entrando en todos los niveles"""
    def _flatten(obj, parent_key=""):
        flat = {}
        for k, v in obj.items():
            key = f"{parent_key}.{k}" if parent_key else k

            if isinstance(v, dict):
                flat.update(_flatten(v, key))
            elif isinstance(v, list):
                flat[key] = json.dumps(v, ensure_ascii=False)
            else:
                flat[key] = v

        return flat
    
    return _flatten(ensayo)

def extraer_ensayos(max_studies = 20000, page_size = 1000, columnas=None):
    """
    Extracción de los datos de la API de ClinicalTrials.gov mediante paginación para evitar llegar a los límites.

    max_studies : int
        Número máximo de ensayos a extraer en total
    page_size : int
        Número de ensayos en cada página (para paginación)

    Devuelve un dataframe donde cada fila es un ensayo. A los campos se les ha aplicado flatten.
    """

    params = {"format": "json", "pageSize": min(page_size,1000), "countTotal": "true",
              "filter.advanced": "AREA[StudyType]Interventional AND AREA[StartDate]RANGE[2000-01-01, MAX] AND AREA[LastUpdatePostDate]RANGE[2000-01-01, 2025-12-01] AND               (AREA[Phase]EARLY_PHASE1 OR AREA[Phase]PHASE1 OR AREA[Phase]PHASE2 OR AREA[Phase]PHASE3 OR AREA[Phase]PHASE4)",
             }
    if columnas:
        params["fields"] = "|".join(columnas)

    all_rows = []
    page_token = None

    # Barra de progreso basada en max_studies (es lo que tú controlas)
    pbar = tqdm(total=max_studies, desc="Descargando ensayos", unit="ensayos")


    while True:
        params.pop("pageToken", None)
        if page_token:
            params["pageToken"] = page_token
            

#        print(f"Realizando petición, descargados {len(all_rows)} ensayos...")
        resp = requests.get(BASE_URL, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        ensayos = data.get("studies") or []
        if not ensayos:
            print("No hay más ensayos, parando la ejecución.")
            break

        for ensayo in ensayos:
            try:
                all_rows.append(flatten_ensayo(ensayo))
                pbar.update(1)
            except Exception as e:
                nct_id = (
                    ensayo.get("protocolSection", {})
                    .get("identificationModule", {})
                    .get("nctId")
                )
                print(f"[WARN] Error aplicando flatten al ensayo {nct_id}: {e}")
                continue

            if len(all_rows) >= max_studies:
                print(f"Alcanzado el número máximo de ensayos={max_studies}, parando la ejecución.")
                pbar.close()
                return pd.DataFrame(all_rows)

        page_token = data.get("nextPageToken")
        if not page_token:
            print("No existe nextPageToken, parando la ejecución.")
            break

        time.sleep(0.2)
        
    pbar.close()
    return pd.DataFrame(all_rows)


def main():
    """
   Descargar datos y guardarlos en data/raw/
    """

    max_studies = 20000
    columnas = None


    if len(sys.argv) > 1:
        try:
            max_studies = int(sys.argv[1])
            print(f"Descargando {max_studies} filas")
        except:
            print("Usando valor por defecto (20000) filas")
        if len(sys.argv) == 2:
            print("Descargando todos los campos por defecto")

    if len(sys.argv) > 2:
        try:
            columnas = sys.argv[2:]
            print("Usando columnas:", columnas)
        except:
            print("Descargando todos los campos")
            
            
    df = extraer_ensayos(max_studies = max_studies, page_size = 1000,columnas=columnas)

    print(f"Se han descargado {len(df)} ensayos.")

    # Se crea la carpeta para los datos RAW si no existe
    raw_dir = Path(__file__).resolve().parents[1] / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    out_path = raw_dir / f"clinicaltrials_raw_{datetime.today():%Y%m%d_%H%M%S}.csv"
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Datos RAW guardados en: {out_path}")


if __name__ == "__main__":
    main()