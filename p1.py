import requests
import pandas as pd
from datetime import datetime

# Geo_id por region son las que esta en la API de REE
# https://www.ree.es/es/datos/apidatos
REGIONES = {
    "Andalucía": 4,
    "Aragón": 5,
    "Cantabria": 6,
    "Asturias": 11,
    "Castilla y León": 8,
    "Castilla-La Mancha": 7,
    "Cataluña": 9,
    "Comunidad Valenciana": 15,
    "Extremadura": 16,
    "Galicia": 17,
    "Madrid": 8752,
    "Murcia": 21,
    "Navarra": 14,
    "País Vasco": 10,
    "La Rioja": 20,
    "Islas Baleares": 8743,
    "Islas Canarias": 8742,
    "Ceuta": 8744,
    "Melilla": 8745,
    "Península": 8741,
}

def get_gen(token, geo_id, start_date, end_date):
    url = "https://apidatos.ree.es/es/datos/generacion/estructura-generacion"
    # creo que esa es la url correcta pero no estoy segura tambn lo saque de la pag de arriba

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Token token={token}"
    }

    params = {
        "start_date": start_date,
        "end_date": end_date,
        "time_trunc": "hour",
        "geo_id": geo_id
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data

    # Datos extraidos por gen
    filas = []
    for tecnologia in data["included"]:
        nombre = tecnologia["attributes"]["title"]
        for v in tecnologia["attributes"]["values"]:
            filas.append({
                "datetime": v["datetime"],
                "value": v["value"],
                "percentage": v["percentage"],
                "tecnologia": nombre
            })

    return pd.DataFrame(filas)

# Aqu i se hace la conexon a la API que es la que no estoy segura si es correcta
if __name__ == "__main__":
    token = "e662304109d4c16c6b52a8e0ce83e95592fe393b64fe09f57746be1932e9a4f1"  # Token de acceso

    print("Regiones disponibles:")
    for r in REGIONES:
        print(f"- {r}")

    region = input("\nEscribe el nombre de la region: ")
    geo_id = REGIONES.get(region)

    # Ingresar fechas solo fechas antes de 2025, creo que es el formato para la fecha pero no estoy segura
    start = input("Fecha de inicio (YYYY-MM-DDTHH:MM): ")
    end = input("Fecha de fin    2023-03-15T00:00 ")


    df = get_gen(token, geo_id, start, end)

    if df.empty:
        print(" No se encontraron datos. Verifica los datos ingresados.")
    else:
        print(df.head())
        archivo = f"data/generacion_{region.replace(' ', '_').lower()}.csv"
        df.to_csv(archivo, index=False)
        print(f"\n Datos guardados en: {archivo}")
