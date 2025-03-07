import requests
import pandas as pd
import matplotlib.pyplot as plt

# Clave de API (Reemplazar con una clave válida de OpenWeatherMap)
API_KEY = "TU API_KEY"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Lista de ciudades a consultar
ciudades = ["Ciudad de México", "Madrid", "Nueva York", "Londres", "Tokio"]

def verificar_conexion():
    """Verificar si hay conexión a internet."""
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        print("Error: No hay conexión a Internet.")
        return False

def obtener_datos_clima(ciudad):
    """Obtener datos climáticos de una ciudad usando la API."""
    params = {"q": ciudad, "appid": API_KEY, "units": "metric"}
    try:
        respuesta = requests.get(BASE_URL, params=params)
        respuesta.raise_for_status()  # Lanzar excepción para códigos de error HTTP
        datos = respuesta.json()

        if "main" in datos and "weather" in datos:
            return {
                "Ciudad": ciudad,
                "Temperatura (°C)": datos["main"]["temp"],
                "Humedad (%)": datos["main"]["humidity"],
                "Condición": datos["weather"][0]["description"].capitalize()
            }
        else:
            print(f"No se encontraron datos válidos para {ciudad}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos para {ciudad}: {e}")
        return None

def obtener_datos_para_ciudades(ciudades):
    """Obtener datos de clima para una lista de ciudades."""
    if not verificar_conexion():
        return pd.DataFrame()

    datos_clima = [obtener_datos_clima(ciudad) for ciudad in ciudades]
    # Filtrar solo los datos válidos
    datos_clima = [d for d in datos_clima if d is not None]
    
    return pd.DataFrame(datos_clima)

def graficar_temperaturas(df):
    """Graficar las temperaturas en un gráfico de barras."""
    if df.empty:
        print("No hay datos para graficar.")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(df["Ciudad"], df["Temperatura (°C)"], color='skyblue')
    plt.xlabel("Ciudad")
    plt.ylabel("Temperatura (°C)")
    plt.title("Temperatura en Diferentes Ciudades")
    plt.show()

def graficar_humedades(df):
    """Graficar las humedades en un gráfico de barras."""
    if df.empty:
        print("No hay datos para graficar.")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(df["Ciudad"], df["Humedad (%)"], color='lightcoral')
    plt.xlabel("Ciudad")
    plt.ylabel("Humedad (%)")
    plt.title("Humedad en Diferentes Ciudades")
    plt.show()

def main():
    # Obtener datos para las ciudades
    df = obtener_datos_para_ciudades(ciudades)
    if not df.empty:
        print(df)
        graficar_temperaturas(df)
        graficar_humedades(df)

if __name__ == "__main__":
    main()
