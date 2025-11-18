# 🔧 Corrección de Bugs - Versión 1.1.1

## 🐛 Problemas Corregidos

### 1. Error en Sensor UV Index
**Problema**: Log de error sobre unidad de medida inválida
```
Entity sensor.google_maps_weather_uv_index is using native unit of measurement 'None' 
which is not a valid unit for the device class ('irradiance')
```

**Solución**: ✅ Eliminado el `device_class` incompatible. El sensor UV Index ahora funciona sin advertencias.

### 2. Pronóstico No Se Muestra
**Problema**: La tarjeta weather no muestra el pronóstico de los siguientes días

**Solución**: ✅ Corregido el método de pronóstico para ser compatible con Home Assistant 2024.x. Ahora el pronóstico se muestra correctamente.

---

## 📥 Cómo Actualizar

### Opción A: Actualización Rápida (Recomendada)

1. **Descarga los archivos actualizados**
   - Descarga `google_maps_weather.zip` 

2. **Detén Home Assistant** (opcional pero recomendado)
   ```bash
   # Si tienes acceso por terminal
   ha core stop
   ```

3. **Reemplaza los archivos**
   - Borra la carpeta actual: `/config/custom_components/google_maps_weather/`
   - Extrae el nuevo zip en el mismo lugar

4. **Reinicia Home Assistant**
   ```bash
   ha core restart
   ```
   O desde la UI: Configuración → Sistema → Reiniciar

5. **Verifica los cambios**
   - Ve a Configuración → Sistema → Logs
   - No deberías ver el error del UV Index
   - Abre la tarjeta weather y verifica que aparece el pronóstico

### Opción B: Actualización Manual de Archivos

Si prefieres actualizar solo los archivos modificados:

1. **Reemplaza estos archivos**:
   - `sensor.py` (corrige UV Index)
   - `weather.py` (corrige pronóstico)
   - `manifest.json` (actualiza versión)

2. **Reinicia Home Assistant**

---

## ✅ Verificación Post-Actualización

### 1. Verifica que no hay errores en los logs
```
Configuración → Sistema → Logs
Busca: "google_maps_weather"
```

No deberías ver:
- ❌ Errores sobre UV Index y device_class
- ❌ Warnings sobre sensores

### 2. Verifica el sensor UV Index
```
Configuración → Entidades
Busca: sensor.google_maps_weather_uv_index
```

Debería:
- ✅ Mostrar un valor numérico (0-11)
- ✅ No tener warnings

### 3. Verifica el pronóstico
```
Tu dashboard → Tarjeta Weather
```

Debería mostrar:
- ✅ Condiciones actuales
- ✅ **Pronóstico de los próximos días** (esto es lo nuevo)
- ✅ Temperaturas máximas y mínimas
- ✅ Iconos de clima para cada día

---

## 🔍 Debug del Pronóstico

Si el pronóstico aún no aparece después de actualizar:

### 1. Habilita logs de debug

Agrega a tu `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.google_maps_weather: debug
```

Reinicia Home Assistant.

### 2. Revisa los logs

Ve a Configuración → Sistema → Logs y busca:

```
Successfully generated X days of forecast
Processing X days of forecast
```

### 3. Fuerza una actualización

Ve a Developer Tools → Services:

```yaml
service: homeassistant.update_entity
target:
  entity_id: weather.google_maps_weather
```

### 4. Verifica los datos de la API

Los logs de debug te mostrarán si:
- ✅ Los datos llegan correctamente de la API
- ❌ Hay algún problema con el formato de datos
- ❌ La API no devuelve pronóstico

---

## 🆘 Solución de Problemas

### Problema: "El pronóstico todavía no aparece"

**Posibles causas y soluciones**:

1. **Cache del navegador**
   - Presiona Ctrl+Shift+R (o Cmd+Shift+R en Mac)
   - Limpia el cache del navegador
   - Recarga la página

2. **La tarjeta no está configurada correctamente**
   ```yaml
   type: weather-forecast
   entity: weather.google_maps_weather
   show_forecast: true  # ← Asegúrate que esto esté
   ```

3. **Los archivos no se actualizaron correctamente**
   - Verifica que `manifest.json` tenga `"version": "1.1.1"`
   - Verifica que `weather.py` tenga el método `_async_forecast_daily`

4. **Home Assistant necesita recarga completa**
   - No solo "Reload", sino un reinicio completo
   - Configuración → Sistema → Reiniciar

### Problema: "Sigo viendo el error de UV Index"

**Solución**:
1. Verifica que `sensor.py` tenga `None` en lugar de `SensorDeviceClass.IRRADIANCE` para UV Index
2. Reinicia completamente Home Assistant
3. Si persiste, elimina y vuelve a agregar la integración

### Problema: "La integración no carga"

**Solución**:
1. Verifica que todos los archivos estén presentes
2. Revisa los logs para ver el error exacto
3. Asegúrate que la versión de Home Assistant sea 2024.1.0 o superior

---

## 📊 Cambios Técnicos Detallados

### sensor.py
```python
# ANTES (v1.1.0)
GoogleMapsWeatherSensor(
    coordinator, entry, "UV Index", "uv_index", "uvIndex",
    None, SensorDeviceClass.IRRADIANCE,  # ← Esto causaba el error
)

# DESPUÉS (v1.1.1)
GoogleMapsWeatherSensor(
    coordinator, entry, "UV Index", "uv_index", "uvIndex",
    None, None,  # ← Sin device_class, sin error
)
```

### weather.py
```python
# AGREGADO en v1.1.1

@callback
def _async_forecast_daily(self) -> list[Forecast] | None:
    """Return the daily forecast in native units."""
    return self._get_forecast()

def _get_forecast(self) -> list[Forecast] | None:
    """Generate forecast data."""
    # Método compartido con mejor manejo de errores
    # y logs de debug
```

---

## 🎉 Resultado Final

Después de actualizar a v1.1.1:

### Lo que verás:
- ✅ Sin errores en los logs
- ✅ Sensor UV Index funcionando perfectamente
- ✅ **Pronóstico visible en la tarjeta weather**
- ✅ Todos los sensores operativos
- ✅ Control de límites de API funcionando

### Lo que puedes hacer:
```yaml
# Ejemplo de tarjeta completa
type: weather-forecast
entity: weather.google_maps_weather
show_forecast: true
forecast_type: daily
name: El Clima
```

---

## 📝 Notas Adicionales

- Esta es una actualización de **corrección de bugs**, no cambia funcionalidades
- No necesitas reconfigurar la integración
- Tu API Key y configuración se mantienen
- El intervalo de actualización configurado se respeta

---

## 💬 ¿Sigues Teniendo Problemas?

Si después de seguir estos pasos todavía tienes problemas:

1. **Exporta tus logs**:
   - Configuración → Sistema → Logs
   - Copia los logs relacionados con `google_maps_weather`

2. **Verifica tu configuración**:
   - ¿Qué versión de Home Assistant usas?
   - ¿Los archivos están en la ubicación correcta?
   - ¿La API Key sigue siendo válida?

3. **Intenta una instalación limpia**:
   - Elimina la integración
   - Borra la carpeta `google_maps_weather`
   - Instala desde cero con los archivos actualizados

---

**Versión corregida**: 1.1.1  
**Fecha**: Noviembre 2024  
**Estado**: ✅ Bugs corregidos y probados
