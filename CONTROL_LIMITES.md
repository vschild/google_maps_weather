# 🎯 Control de Límites de API - Google Maps Weather

## 📊 Resumen del Tier Gratuito

La API de Google Maps Weather ofrece un **tier gratuito de 1,000 llamadas por mes** durante su período de Preview.

### ¿Por qué es importante?

Si sobrepasas las 1,000 llamadas mensuales, comenzarás a incurrir en costos:
- **Costo**: $0.15 por cada 1,000 llamadas adicionales (CPM)
- **Ejemplo**: 1,500 llamadas/mes = $0.075 adicionales

## 🛡️ Cómo Esta Integración Te Protege

### 1. Intervalo de Actualización Configurable

Durante la configuración inicial, puedes elegir cuán frecuentemente se actualizan los datos:

| Intervalo | Llamadas/Día | Llamadas/Mes | % del Límite | Costo Mensual |
|-----------|--------------|--------------|--------------|---------------|
| 45 min | 32 | ~960 | 96% | $0.00 ✓ |
| **60 min** | **24** | **~720** | **72%** | **$0.00 ✓** |
| 90 min | 16 | ~480 | 48% | $0.00 ✓ |
| 120 min | 12 | ~360 | 36% | $0.00 ✓ |
| 180 min | 8 | ~240 | 24% | $0.00 ✓ |

**Todos los intervalos disponibles están dentro del límite gratuito.**

### 2. Sensor de Monitoreo Automático

La integración incluye un sensor especial: `sensor.google_maps_weather_api_usage_estimate`

#### Información que proporciona:

```yaml
Estado: 720 llamadas/mes

Atributos:
  update_interval_minutes: 60
  update_interval_display: "60 minutos"
  estimated_monthly_calls: 720
  free_tier_limit: 1000
  usage_percentage: 72.0
  status: "✓ Dentro del límite gratuito"
  calls_per_day: 24.0
  within_free_tier: true
```

## 📈 Monitoreo en Tu Dashboard

### Tarjeta Simple

```yaml
type: entity
entity: sensor.google_maps_weather_api_usage_estimate
name: Uso de API
icon: mdi:api
```

### Tarjeta Detallada

```yaml
type: entities
title: 📊 Uso de API Google Weather
entities:
  - entity: sensor.google_maps_weather_api_usage_estimate
    name: Llamadas Mensuales Estimadas
    icon: mdi:counter
  - type: attribute
    entity: sensor.google_maps_weather_api_usage_estimate
    attribute: usage_percentage
    name: % del Límite Gratuito
    suffix: "%"
  - type: attribute
    entity: sensor.google_maps_weather_api_usage_estimate
    attribute: status
    name: Estado
  - type: attribute
    entity: sensor.google_maps_weather_api_usage_estimate
    attribute: calls_per_day
    name: Llamadas por Día
  - type: attribute
    entity: sensor.google_maps_weather_api_usage_estimate
    attribute: update_interval_display
    name: Intervalo de Actualización
```

### Tarjeta con Gauge

```yaml
type: gauge
entity: sensor.google_maps_weather_api_usage_estimate
name: Uso de API
unit: calls/month
min: 0
max: 1000
needle: true
severity:
  green: 0
  yellow: 700
  red: 900
```

## 🔔 Alertas Automáticas

### Alerta al Acercarse al Límite

```yaml
automation:
  - alias: "Alerta: Cercano al límite de API"
    description: "Notifica cuando te acercas al límite gratuito"
    trigger:
      - platform: numeric_state
        entity_id: sensor.google_maps_weather_api_usage_estimate
        above: 900
    action:
      - service: notify.mobile_app_tu_dispositivo
        data:
          title: "⚠️ Advertencia de API"
          message: >
            Uso estimado: {{ states('sensor.google_maps_weather_api_usage_estimate') }} llamadas/mes
            ({{ state_attr('sensor.google_maps_weather_api_usage_estimate', 'usage_percentage') }}% del límite)
            
            Considera aumentar el intervalo de actualización para mantenerte dentro del límite gratuito.
          data:
            notification_icon: "mdi:alert"
            color: "orange"
```

### Alerta Crítica (Sobrepaso del Límite)

```yaml
  - alias: "Alerta CRÍTICA: Sobrepasado límite de API"
    description: "Notifica si sobrepasas el límite gratuito"
    trigger:
      - platform: numeric_state
        entity_id: sensor.google_maps_weather_api_usage_estimate
        above: 1000
    action:
      - service: notify.mobile_app_tu_dispositivo
        data:
          title: "🚨 ALERTA CRÍTICA: Límite Sobrepasado"
          message: >
            ¡ATENCIÓN! Tu configuración actual generaría
            {{ states('sensor.google_maps_weather_api_usage_estimate') }} llamadas/mes.
            
            Esto sobrepasa el límite gratuito de 1000 llamadas.
            Comenzarás a incurrir en costos.
            
            ACCIÓN REQUERIDA: Aumenta el intervalo de actualización AHORA.
          data:
            notification_icon: "mdi:alert-octagon"
            color: "red"
            importance: "high"
```

## 🔧 Cómo Cambiar el Intervalo

Si necesitas ajustar tu intervalo de actualización después de la instalación:

### Opción 1: Reconfigurar la Integración

1. Ve a **Configuración** → **Dispositivos y Servicios**
2. Encuentra **Google Maps Weather**
3. Haz clic en los tres puntos (⋮)
4. Selecciona **Eliminar**
5. Vuelve a agregar la integración con un nuevo intervalo

### Opción 2: Editar Manualmente (Avanzado)

1. Ve a `.storage/core.config_entries` en tu configuración
2. Busca la entrada de `google_maps_weather`
3. Modifica el valor de `update_interval`
4. Reinicia Home Assistant

**⚠️ Advertencia**: La Opción 2 puede causar problemas si se hace incorrectamente.

## 📊 Calculadora de Uso

Puedes calcular el uso estimado con esta fórmula:

```
Llamadas por mes = (60 × 24 × 30) / Intervalo en minutos
```

Ejemplos:
- 30 min: (43,200) / 30 = **1,440 llamadas** ❌ Sobrepasa límite
- 45 min: (43,200) / 45 = **960 llamadas** ✓
- 60 min: (43,200) / 60 = **720 llamadas** ✓
- 90 min: (43,200) / 90 = **480 llamadas** ✓
- 120 min: (43,200) / 120 = **360 llamadas** ✓

## 💡 Recomendaciones

### Para Usuarios Típicos
- **Intervalo recomendado**: 60 minutos
- **Razón**: Balance perfecto entre datos actualizados y uso de API
- **Uso**: 72% del límite gratuito
- **Seguridad**: 28% de margen

### Para Usuarios Conservadores
- **Intervalo recomendado**: 90-120 minutos
- **Razón**: Máxima seguridad, datos aún actualizados
- **Uso**: 36-48% del límite gratuito
- **Seguridad**: 52-64% de margen

### Para Datos Muy Actualizados
- **Intervalo mínimo**: 45 minutos
- **Razón**: Datos más frescos, aún dentro del límite
- **Uso**: 96% del límite gratuito
- **Seguridad**: 4% de margen (¡estrecho!)

## 🎯 Buenas Prácticas

1. **Monitorea regularmente** el sensor de uso de API
2. **Configura alertas** para cuando te acerques al límite
3. **Comienza conservador** (90-120 min) y ajusta según necesites
4. **Revisa mensualmente** tu uso real en Google Cloud Console
5. **Ten margen de seguridad** - no uses el 100% del límite

## 📱 Widget de Monitoreo Rápido

Para una vista rápida en tu pantalla principal:

```yaml
type: glance
title: Estado API
entities:
  - entity: sensor.google_maps_weather_api_usage_estimate
    name: Uso Mensual
  - entity: sensor.google_maps_weather_api_usage_estimate
    name: "% Límite"
    attribute: usage_percentage
  - entity: sensor.google_maps_weather_api_usage_estimate
    name: Estado
    attribute: status
```

## ❓ FAQ

### ¿Qué pasa si sobrepaso el límite?

Si tu configuración estima más de 1000 llamadas/mes:
1. El sensor te alertará
2. Comenzarás a incurrir en costos ($0.15 por 1000 llamadas)
3. Puedes cambiar el intervalo en cualquier momento

### ¿El cálculo es exacto?

El cálculo es una **estimación** basada en:
- Tu intervalo configurado
- Asumiendo operación 24/7
- Sin contar reinicios o errores

El uso real puede ser ligeramente menor debido a:
- Reinicios de Home Assistant
- Errores de conexión temporales
- Períodos de inactividad

### ¿Puedo ver mi uso real?

Sí, en [Google Cloud Console](https://console.cloud.google.com/):
1. Ve a tu proyecto
2. Selecciona "APIs y servicios" → "Panel"
3. Busca "Weather API"
4. Ve las métricas de uso

### ¿Qué pasa después del período de Preview?

Después del Preview, la API podría:
- Cambiar el límite gratuito
- Ajustar los precios
- Modificar las condiciones

Mantente informado revisando la documentación oficial de Google.

## 🚀 Configuración Recomendada Inicial

```yaml
Configuración Sugerida para Nuevos Usuarios:

API Key: [Tu clave de Google Maps]
Latitud: [Tu ubicación]
Longitud: [Tu ubicación]
Unidades: METRIC (o IMPERIAL)
Intervalo: 60 minutos ⭐ RECOMENDADO

Resultado:
- ~720 llamadas/mes (72% del límite)
- Datos actualizados cada hora
- Bien dentro del tier gratuito
- Margen de seguridad del 28%
```

## ✅ Checklist de Seguridad

- [ ] He seleccionado un intervalo ≥ 45 minutos
- [ ] He configurado el sensor de monitoreo en mi dashboard
- [ ] He creado una alerta para uso > 900 llamadas
- [ ] Reviso el sensor al menos una vez al mes
- [ ] Conozco cómo cambiar el intervalo si es necesario

---

## 📞 Soporte

Si tienes dudas sobre el uso de la API:
- Consulta [Google Cloud Console](https://console.cloud.google.com/) para ver uso real
- Revisa la [documentación oficial](https://developers.google.com/maps/documentation/weather)
- Pregunta en el [foro de Home Assistant](https://community.home-assistant.io/)

---

**Recuerda**: Con el intervalo predeterminado de 60 minutos, estarás perfectamente dentro del límite gratuito. ¡No hay que preocuparse! 🎉
