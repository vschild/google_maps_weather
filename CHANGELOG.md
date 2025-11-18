# 🔄 Changelog - Control de Límites de API

## Versión 1.1.2 - Fix Crítico de Pronóstico y Condiciones

### 🐛 Correcciones Críticas

1. **Fix Detección Día/Noche**
   - Ahora detecta correctamente si es de día o de noche
   - Usa `clear-night` cuando está despejado de noche
   - Usa `sunny` cuando está despejado de día
   - Lee el campo `isDaytime` de la API de Google

2. **Fix Pronóstico Definitivo**
   - Eliminado el método `_async_forecast_daily()` con callback (no funciona en HA 2024.x)
   - Implementado correctamente solo `async_forecast_daily()`
   - Agregado sistema de cache para el pronóstico
   - Cache se invalida automáticamente en cada actualización
   - Logs mejorados para debug

3. **Mejoras en Logs**
   - Logs más detallados del procesamiento del pronóstico
   - Información de cada día generado
   - Mejor manejo de errores con traceback completo

### 📝 Archivos Modificados
- `weather.py` - Fix completo de pronóstico y condiciones día/noche
- `const.py` - Comentarios actualizados en CONDITION_MAP
- `manifest.json` - Versión 1.1.2

### 🔍 Cambios Técnicos

**Detección día/noche:**
```python
# Ahora lee isDaytime de la API
is_daytime = current.get("isDaytime", True)
if condition == "sunny" and not is_daytime:
    condition = "clear-night"
```

**Pronóstico con cache:**
```python
async def async_forecast_daily(self) -> list[Forecast] | None:
    # Usa cache si existe
    if self._forecast_cache is not None:
        return self._forecast_cache
    # Genera y cachea
    forecast = self._generate_forecast()
    self._forecast_cache = forecast
    return forecast
```

---

## Versión 1.1.1 - Bug Fixes

### 🐛 Correcciones

1. **Fix UV Index Sensor**
   - Eliminado `device_class` incompatible del sensor UV Index
   - Solucionado error: "is not a valid unit for device class 'irradiance'"
   - El sensor ahora funciona correctamente sin advertencias

2. **Fix Pronóstico Diario (Intento 1)**
   - Corregido método `async_forecast_daily()` para Home Assistant 2024.x
   - Agregado método `_async_forecast_daily()` con callback
   - Mejorado el parsing de fechas desde la API
   - Agregados logs de debug para facilitar troubleshooting

### 📝 Archivos Modificados
- `sensor.py` - Fix UV Index
- `weather.py` - Fix forecast + mejores logs
- `manifest.json` - Versión 1.1.1

---

## Versión 1.1.0 - Control de Límites Implementado

### 🎯 Objetivo
Agregar control completo sobre el uso de la API para no sobrepasar el límite gratuito de 1,000 llamadas por mes.

---

## ✨ Nuevas Características

### 1. ⚙️ Intervalo de Actualización Configurable

**Archivos modificados**: `config_flow.py`, `const.py`, `__init__.py`

Opciones disponibles:
- 45 minutos (~960 llamadas/mes)
- 60 minutos (~720 llamadas/mes) - Recomendado ⭐
- 90 minutos (~480 llamadas/mes)
- 120 minutos (~360 llamadas/mes)
- 180 minutos (~240 llamadas/mes)

### 2. 📊 Sensor de Monitoreo

**Archivo modificado**: `sensor.py`

Nuevo sensor: `sensor.google_maps_weather_api_usage_estimate`

Muestra:
- Llamadas mensuales estimadas
- Porcentaje de uso del límite
- Estado (dentro/fuera del límite)
- Intervalo configurado

### 3. 📖 Nueva Documentación

**Archivo nuevo**: `CONTROL_LIMITES.md`

Guía completa sobre límites de API con ejemplos y alertas.

---

**Versión actual**: 1.1.2  
**Fecha**: Noviembre 2024
