import pytest
from unittest.mock import patch
import requests
from clima import obtener_datos_clima, verificar_conexion


# Test para verificar la función de conexión
def test_verificar_conexion_exitosa():
    with patch.object(requests, 'get', return_value=True):
        assert verificar_conexion() == True

def test_verificar_conexion_error():
    with patch.object(requests, 'get', side_effect=requests.exceptions.ConnectionError):
        assert verificar_conexion() == False


# Test para verificar la función de obtener datos del clima
def test_obtener_datos_clima_exitoso():
    mock_response = requests.Response()
    mock_response._content = b'{"main": {"temp": 25, "humidity": 60}, "weather": [{"description": "clear sky"}]}'
    mock_response.status_code = 200  # Simulamos un código de estado 200 OK
    with patch.object(requests, 'get', return_value=mock_response):
        resultado = obtener_datos_clima("Ciudad de México")
        assert resultado["Ciudad"] == "Ciudad de México"
        assert resultado["Temperatura (°C)"] == 25
        assert resultado["Humedad (%)"] == 60
        assert resultado["Condición"] == "Clear sky"

def test_obtener_datos_clima_error():
    with patch.object(requests, 'get', side_effect=requests.exceptions.RequestException):
        resultado = obtener_datos_clima("Ciudad de México")
        assert resultado is None

# Mensaje de éxito después de pasar todas las pruebas
if __name__ == "__main__":
    pytest.main()
    print("\nTodas las pruebas han pasado exitosamente")