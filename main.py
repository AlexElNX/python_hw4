from typing import Protocol, runtime_checkable
import requests
import random

@runtime_checkable
class TemperatureSensor(Protocol):
    def get_sensor_id(self) -> str: pass
    def read_temperature(self) -> float: pass



class WeatherAPISensor:
    def get_sensor_id(self) -> str:
        return "WAS26-Odesa"
    
    def read_temperature(self) -> float:
        url = "https://wttr.in/Odesa?format=j1&m"
        response = ""

        try:
            response = requests.get(url)

        except:
           raise RuntimeError("Network request failed")

        temp = response.json()["current_condition"][0]["temp_C"]

        return float(temp)


class SimulatedSensor:
    def __init__(self, base_temp: float, deviation: float):
        self.base_temp = base_temp
        self.deviation = deviation

    def get_sensor_id(self) -> str:
        return "Simulated-Sensor"

    def read_temperature(self) -> float:
        return (self.base_temp + round(random.uniform(-self.deviation, self.deviation)))


class FakeAlways25:
    def get_sensor_id(self) -> str:
        return "Fake-25"
    
    def read_temperature(self) -> float:
        return 25.0

class BrokenSensor:
    def get_sensor_id(self) -> str:
        return "BROKEN-999"
    
    def read_temperature(self) -> float:
        raise RuntimeError("Sensor is broken")

def monitor_room(sensors: list[TemperatureSensor]) -> None:
    for sensor in sensors :
        try:
            print(f"{sensor.get_sensor_id()} Temperatue: {sensor.read_temperature()}°C \n")
        except Exception as e:
            print(f"{sensor.get_sensor_id()} Error: {e} \n")



sensors = [WeatherAPISensor(),  SimulatedSensor(21.5, 3.0), FakeAlways25(), BrokenSensor()]

monitor_room(sensors)