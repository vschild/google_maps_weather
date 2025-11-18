# 🔍 DEBUG v1.1.3 - Temperaturas Null

## 🐛 Problema Detectado

El servicio `weather.get_forecasts` devuelve:
```yaml
temperature: null  # ← Este es el problema
```

Esto hace que Home Assistant no muestre el pronóstico porque `temperature` es un campo **requerido**.

---

## 📦 Versión 1.1.3 - Con Logs de Debug

He actualizado la integración con logs detallados para encontrar dónde están las temperaturas en la respuesta de Google.

### [Descargar v1.1.3](computer:///mnt/user-data/outputs/google_maps_weather.zip)

---

## 🚀 Pasos para Debuggear

### 1. Instala la versión 1.1.3

```bash
# Reemplaza los archivos
rm -rf /config/custom_components/google_maps_weather/
# Extrae el nuevo zip
```

### 2. Habilita Logs de Debug

Edita `/config/configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.google_maps_weather: debug
```

### 3. Reinicia Home Assistant

```
Configuración → Sistema → Reiniciar
```

### 4. Espera 1-2 Minutos

Deja que la integración actualice los datos.

### 5. Revisa los Logs

```
Configuración → Sistema → Logs
```

Busca estas líneas (estarán al final):

```
First day structure keys: [...]
daytimeForecast keys: [...]
Day 0 temp extraction: temp_max=None, temp_min=None
Day 0 daytime.temperature: {...}
Day 0 nighttime.temperature: {...}
```

### 6. Copia y Envía Los Logs

**Por favor copia y envía**:

1. La línea que dice `First day structure keys:`
2. La línea que dice `daytimeForecast keys:`
3. Las líneas que dicen `Day 0 daytime.temperature:`
4. Las líneas que dicen `Day 0 nighttime.temperature:`

Con esa información podré ver exactamente dónde Google está poniendo las temperaturas.

---

## 💡 Lo Que Estoy Buscando

La API de Google puede devolver las temperaturas en diferentes ubicaciones:

**Opción 1** (lo que esperaba):
```json
{
  "daytimeForecast": {
    "temperature": {
      "degrees": 15.0
    }
  }
}
```

**Opción 2** (posible):
```json
{
  "maxTemperature": {
    "degrees": 15.0
  },
  "minTemperature": {
    "degrees": 10.0
  }
}
```

**Opción 3** (posible):
```json
{
  "daytimeForecast": {
    "maxTemperature": {
      "degrees": 15.0
    }
  }
}
```

O podría estar en otro lugar completamente diferente. Los logs me dirán exactamente dónde buscar.

---

## 🔍 Ejemplo de Lo Que Necesito Ver

Cuando revises los logs, busca algo como esto y cópialo completo:

```
2024-11-17 22:30:15 DEBUG (MainThread) [custom_components.google_maps_weather.weather] First day structure keys: ['interval', 'displayDate', 'daytimeForecast', 'nighttimeForecast', 'maxTemperature', 'minTemperature']

2024-11-17 22:30:15 DEBUG (MainThread) [custom_components.google_maps_weather.weather] daytimeForecast keys: ['interval', 'weatherCondition', 'temperature', 'precipitation', 'wind', ...]

2024-11-17 22:30:15 DEBUG (MainThread) [custom_components.google_maps_weather.weather] Day 0 daytime.temperature: {'value': 15.0, 'unit': 'CELSIUS'}

2024-11-17 22:30:15 DEBUG (MainThread) [custom_components.google_maps_weather.weather] Day 0 nighttime.temperature: {'value': 10.0, 'unit': 'CELSIUS'}
```

---

## ⚡ Arreglo Rápido Temporal

Mientras esperamos los logs, aquí hay una versión alternativa que intenta TODAS las ubicaciones posibles para las temperaturas.

Ya está incluida en v1.1.3, que intenta extraer de:
- `daytimeForecast.temperature.degrees`
- `daytimeForecast.maxTemperature.degrees`  
- `day.maxTemperature.degrees`
- `nighttimeForecast.temperature.degrees`
- `nighttimeForecast.minTemperature.degrees`
- `day.minTemperature.degrees`

Pero necesito los logs para ver cuál es la estructura real.

---

## 📋 Checklist

- [ ] Instalada v1.1.3
- [ ] Habilitados logs de debug en configuration.yaml
- [ ] Reiniciado Home Assistant
- [ ] Esperado 2 minutos
- [ ] Copiados los logs que mencionan "First day structure"
- [ ] Copiados los logs que mencionan "daytimeForecast keys"
- [ ] Copiados los logs que mencionan "Day 0 temperature"

---

Con esos logs podré crear la versión definitiva que funcione correctamente. 🎯
