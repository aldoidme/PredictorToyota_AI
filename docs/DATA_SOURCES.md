# Fuentes de datos reales - Toyota Predictor Peru

## Objetivo
Definir fuentes estables, legales y faciles de mantener para integrar datos reales en el sistema.

## Criterios de seleccion
- Estabilidad: disponibilidad continua y cambios minimos en la fuente.
- Legalidad: uso permitido por terminos publicos o APIs.
- Mantenimiento: bajo costo de actualizacion y cambios de formato.
- Cobertura: datos relevantes para Toyota en Peru.

## Fuentes recomendadas (prioridad alta)

### 1) Acciones Toyota (tendencia de acciones)
- Fuente: Yahoo Finance
- Acceso: API no oficial via yfinance
- Cobertura: historico de precios, volumen, ajustes
- Estado: recomendado
- Riesgo: cambios ocasionales en el endpoint
- Uso: tendencias simples y recomendacion comprar/mantener/vender

### 2) Tendencias de busqueda
- Fuente: Google Trends
- Acceso: API no oficial via pytrends
- Cobertura: interes por termino, region, periodo
- Estado: recomendado
- Riesgo: limites de tasa, variacion del indice
- Uso: demanda de modelos y interes del mercado

## Fuentes en evaluacion (prioridad media)

### 3) Precios nuevos (modelos Toyota Peru)
- Fuente sugerida: web oficial de Toyota Peru o catalogos publicos
- Acceso: solo si hay pagina publica o PDF oficial
- Estado: en evaluacion
- Riesgo: cambios de formato y restricciones de uso
- Uso: precios nuevos aproximados para comparativas

### 4) Precios usados (mercado secundario)
- Fuente sugerida: portales publicos con anuncios visibles
- Acceso: depende de terminos de uso de cada portal
- Estado: en evaluacion
- Riesgo: restricciones de scraping y cambios constantes
- Uso: precio usado aproximado por modelo

### 5) Ventas historicas
- Fuente sugerida: reportes oficiales publicos (ministerios, gremios, boletines)
- Acceso: documentos PDF o reportes en web
- Estado: en evaluacion
- Riesgo: formato no estructurado y baja frecuencia
- Uso: demanda real a nivel mensual

## Recomendaciones de documentacion
Para cada fuente aprobada, registrar:
- Nombre de la fuente
- URL oficial
- Tipo de acceso (API, web, PDF)
- Frecuencia de actualizacion
- Campos disponibles
- Riesgos y limitaciones
- Responsable de mantenimiento

## Notas legales
- No usar scraping sin verificar terminos de uso.
- Preferir APIs o fuentes publicas con permisos claros.
- Documentar fecha y version de la fuente.
