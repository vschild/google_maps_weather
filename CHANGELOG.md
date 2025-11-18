# 🔄 Changelog - Control de Límites de API

## Versión 1.2.0 - Hourly Forecast & Parallel API Calls

### 🎉 Nuevas Características

1. **Pronóstico Horario**
   - ⏰ Soporte completo para pronóstico por hora
   - ⚙️ Configurable: 24 a 240 horas (1 a 10 días)
   - 📊 Por defecto: 48 horas (2 días)
   - 🎯 Vista dual: diaria y horaria en Home Assistant
   - 🌙 Detección automática día/noche en pronósticos horarios

2. **Llamadas API en Paralelo**
   - ⚡ 3 endpoints ejecutados simultáneamente con `asyncio.gather()`
   - 🚀 Sin penalización de rendimiento
   - 📡 Endpoints: condiciones actuales + pronóstico diario + pronóstico horario
   - ⏱️ Tiempo de respuesta similar a 1 llamada secuencial

3. **Nueva Configuración**
   - 🎛️ Campo configurable: "Horas de pronóstico horario"
   - 🔢 Opciones: 24, 48, 72, 96, 120, 168, 240 horas
   - 💡 Valor recomendado: 48 horas (2 días)
   - 📝 Descripciones mejoradas en la UI

### 🔄 Cambios en API Usage

**IMPORTANTE**: Ahora se realizan **3 llamadas por actualización**

1. **Intervalos Actualizados**
   - Recomendado: **120 minutos** (~720 llamadas/mes)
   - Conservador: 150 minutos (~576 llamadas/mes)
   - Muy conservador: 180 minutos (~480 llamadas/mes)
   - Eliminados intervalos < 90 min (sobrepasan límite)

2. **Monitoreo Mejorado**
   - Sensor de uso API actualizado para 3 llamadas/actualización
   - Atributo nuevo: `calls_per_update: 3`
   - Cálculo preciso de uso mensual

### 📝 Archivos Modificados

- `const.py` - Nuevas constantes y opciones de configuración
- `config_flow.py` - Campo de horas de pronóstico horario
- `__init__.py` - Implementación de llamadas paralelas con asyncio
- `weather.py` - Soporte completo de pronóstico horario
- `sensor.py` - Actualización de cálculos de uso API
- `strings.json` - Traducciones en español actualizadas
- `translations/en.json` - Traducciones en inglés actualizadas
- `manifest.json` - Versión 1.2.0
- `README.md` - Documentación completa de nuevas características

### 🔍 Cambios Técnicos

**weather.py**
```python
# Nuevos métodos
async def async_forecast_hourly() -> list[Forecast] | None
def _generate_forecast_hourly() -> list[Forecast] | None

# Features actualizados
_attr_supported_features = (
    WeatherEntityFeature.FORECAST_DAILY | WeatherEntityFeature.FORECAST_HOURLY
)
```

**__init__.py**
```python
# Llamadas paralelas con asyncio
current, forecast_daily, forecast_hourly = await asyncio.gather(
    api.get_current_conditions(),
    api.get_daily_forecast(),
    api.get_hourly_forecast(hours=hourly_forecast_hours)
)
```

### 💰 Impacto en Costos

| Configuración | Antes | Ahora |
|---------------|-------|-------|
| Llamadas/actualización | 2 | 3 |
| Intervalo recomendado | 60 min | 120 min |
| Llamadas/mes (recomendado) | ~720 | ~720 |

**Resultado**: Más datos, mismo consumo de API ✅

### 🎨 Nuevas Capacidades UI

**Tarjetas de Clima**
```yaml
# Vista diaria
type: weather-forecast
entity: weather.google_maps_weather
forecast_type: daily

# Vista horaria (NUEVO)
type: weather-forecast
entity: weather.google_maps_weather
forecast_type: hourly
```

### ⚠️ Notas de Migración

- **Instalaciones nuevas**: Todo configurado automáticamente
- **Actualizaciones**: 
  - El campo "hourly_forecast_hours" se agregará con valor por defecto (48h)
  - El intervalo de actualización se mantendrá como estaba configurado
  - Considerar ajustar el intervalo si estabas usando < 90 minutos

### 🐛 Correcciones

- Logs más eficientes para pronósticos horarios (solo primeras 3 horas)
- Validación robusta de datos de pronóstico horario
- Manejo de errores mejorado en `_generate_forecast_hourly()`

---

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
