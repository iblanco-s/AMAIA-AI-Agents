# Módulo 10: Azure AI Agents SDK - Bing Search Tool

## 📋 Descripción General

Este módulo te enseña cómo crear agentes de IA que pueden buscar información en Internet usando **Bing Search** a través del **Azure AI Agents SDK**. Aprenderás a construir un agente de investigación de mercado que puede obtener información actualizada en tiempo real sobre tendencias tecnológicas, noticias de la industria, análisis competitivos y más.

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

1. ✅ Configurar y usar **BingGroundingTool** en Azure AI Foundry
2. ✅ Crear agentes que buscan información actualizada en Internet
3. ✅ Implementar casos de uso de investigación de mercado
4. ✅ Configurar parámetros de búsqueda (mercado, idioma, frescura)
5. ✅ Gestionar conversaciones multi-turno con información web en tiempo real

## 🛠️ Herramientas y Tecnologías

- **Azure AI Agents SDK**: Framework para crear agentes de IA
- **BingGroundingTool**: Herramienta de búsqueda en Internet integrada
- **Azure AI Foundry**: Plataforma de desarrollo y despliegue
- **Python 3.8+**: Lenguaje de programación
- **Jupyter Notebooks**: Entorno de desarrollo interactivo

## 📁 Estructura del Módulo

```
10-azure-ai-agents-sdk-bing-search-es/
├── README.md
└── Python/
    └── market-research-agent.ipynb
```

## 🚀 Caso de Uso: Agente de Investigación de Mercado

El agente implementado en este módulo es un **Agente de Investigación de Mercado** especializado en:

### Capacidades del Agente

1. **Investigación de Tendencias Tecnológicas**
   - Buscar las últimas tendencias en IA, cloud computing, etc.
   - Identificar tecnologías emergentes
   - Analizar el estado actual del mercado

2. **Análisis de Noticias de la Industria**
   - Recopilar noticias recientes sobre empresas o sectores
   - Monitorear anuncios y lanzamientos de productos
   - Seguir desarrollos en áreas específicas

3. **Investigación de Productos y Tecnologías**
   - Obtener información detallada sobre productos específicos
   - Comparar características y capacidades
   - Entender casos de uso y aplicaciones

4. **Análisis Competitivo**
   - Comparar diferentes proveedores y soluciones
   - Identificar fortalezas y debilidades
   - Analizar posicionamiento de mercado

## ⚙️ Configuración Previa

### 1. Configurar Conexión de Bing Search en Azure AI Foundry

Antes de ejecutar el notebook, necesitas crear una conexión de Bing Search:

#### Paso 1: Obtener API Key de Bing Search

1. Ve al [Portal de Azure](https://portal.azure.com)
2. Busca "Bing Search v7" en el marketplace
3. Crea un nuevo recurso de Bing Search API
4. Una vez creado, ve a "Keys and Endpoint"
5. Copia una de las API Keys

#### Paso 2: Crear Conexión en Azure AI Foundry

1. Abre [Azure AI Foundry Portal](https://ai.azure.com)
2. Ve a tu proyecto
3. Navega a **Settings** > **Connections**
4. Haz clic en **New Connection**
5. Selecciona **Bing Search**
6. Proporciona:
   - **Name**: Un nombre descriptivo (ej: "bing-search-connection")
   - **API Key**: La key que copiaste anteriormente
7. Guarda la conexión
8. Copia el **Connection ID** que aparece (lo necesitarás para el .env)

### 2. Configurar Variables de Entorno

Añade las siguientes variables al archivo `.env` en la raíz del proyecto:

```env
# Variables existentes
PROJECT_ENDPOINT=https://tu-proyecto.cognitiveservices.azure.com/
MODEL_DEPLOYMENT_NAME=tu-modelo-desplegado

# Nueva variable para Bing Search
BING_CONNECTION_ID=tu-connection-id-de-bing
```

### 3. Instalar Dependencias

Las dependencias necesarias ya están incluidas en el `requirements.txt` del proyecto:

```bash
# Si aún no lo has hecho, ejecuta:
pip install -r requirements.txt
```

## 📚 Contenido del Notebook

### Secciones Principales

1. **Introducción y Configuración**
   - Carga de librerías y variables de entorno
   - Conexión al Azure AI Agents Client
   - Verificación de configuración

2. **Crear BingGroundingTool**
   - Inicialización de la herramienta de búsqueda
   - Configuración de parámetros:
     - `count`: Número de resultados (default: 5)
     - `market`: Mercado/región (ej: "es-ES" para España)
     - `set_lang`: Idioma de la interfaz (ej: "es")
     - `freshness`: Frescura de resultados ("day", "week", "month")

3. **Crear el Agente de Investigación**
   - Definición del agente con instrucciones especializadas
   - Configuración de herramientas (BingGroundingTool)
   - Creación de thread de conversación

4. **Ejemplos de Uso Práctico**
   - 5 ejemplos completos de casos de uso
   - Prompts personalizables
   - Visualización de respuestas estructuradas

5. **Gestión y Limpieza**
   - Visualización del historial de conversación
   - Eliminación del agente

## 💡 Ejemplos de Prompts

Aquí hay algunos ejemplos de prompts que puedes usar con el agente:

### Tendencias Tecnológicas
```
¿Cuáles son las principales tendencias en inteligencia artificial y machine learning en 2025?
```

### Noticias de la Industria
```
Busca las últimas noticias sobre Azure AI y Microsoft en el sector de inteligencia artificial
```

### Investigación de Productos
```
Investiga qué es Azure AI Agents SDK y cuáles son sus principales características y casos de uso
```

### Análisis Competitivo
```
Compara las plataformas de agentes de IA de los principales proveedores cloud (Azure, AWS, Google Cloud)
```

### Investigación Personalizada
```
Busca información sobre [tendencias en computación cuántica / blockchain / IoT / etc.]
```

## 🔧 Parámetros de BingGroundingTool

### Configuración Disponible

```python
bing_tool = BingGroundingTool(
    connection_id=bing_connection_id,  # Required: Connection ID from Azure AI Foundry
    count=5,                            # Optional: Number of search results (1-50)
    market="es-ES",                     # Optional: Market code (e.g., "es-ES", "en-US")
    set_lang="es",                      # Optional: UI language code (e.g., "es", "en")
    freshness="week"                    # Optional: "day", "week", "month", or ""
)
```

### Códigos de Mercado Comunes

- `es-ES`: España (Español)
- `es-MX`: México (Español)
- `es-AR`: Argentina (Español)
- `en-US`: Estados Unidos (Inglés)
- `en-GB`: Reino Unido (Inglés)
- `pt-BR`: Brasil (Portugués)

## 🎓 Conceptos Clave

### 1. Grounding con Bing Search

El "grounding" se refiere a la capacidad del agente de basar sus respuestas en información real y actualizada de Internet, en lugar de depender únicamente de su conocimiento de entrenamiento.

**Ventajas:**
- ✅ Información actualizada en tiempo real
- ✅ Respuestas basadas en fuentes verificables
- ✅ Capacidad de investigar eventos recientes
- ✅ Acceso a datos más allá del conocimiento del modelo

### 2. Diferencia con Code Interpreter

| Herramienta | Propósito | Casos de Uso |
|-------------|-----------|--------------|
| **BingGroundingTool** | Búsqueda de información en Internet | Noticias, tendencias, investigación de mercado |
| **CodeInterpreterTool** | Análisis de datos y cálculos | Estadísticas, visualizaciones, procesamiento de archivos |

Estos tools son complementarios y pueden usarse juntos en el mismo agente.

### 3. Gestión de Conexiones

Las conexiones en Azure AI Foundry permiten:
- Centralizar credenciales y configuración
- Reutilizar conexiones entre múltiples agentes
- Gestionar permisos y acceso
- Monitorear uso y costos

## 🚀 Próximos Pasos

Después de completar este módulo, puedes:

1. **Combinar Múltiples Herramientas**
   - Usar BingGroundingTool + CodeInterpreterTool
   - Agregar funciones personalizadas
   - Crear agentes más complejos

2. **Crear Sistemas Multi-Agente**
   - Un agente especializado en búsqueda (Bing)
   - Otro agente para análisis de datos
   - Coordinador que orquesta ambos

3. **Implementar en Producción**
   - Crear una API REST con FastAPI
   - Integrar con Agent Framework
   - Desplegar como servicio A2A

4. **Optimizar Búsquedas**
   - Experimentar con diferentes parámetros
   - Filtrar por dominio o categoría
   - Procesar y estructurar resultados

## 📖 Recursos Adicionales

### Documentación Oficial

- [Azure AI Agents SDK Documentation](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-agents-readme)
- [Bing Grounding Tool Reference](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/bing-grounding)
- [Bing Search API Documentation](https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/overview)

### Blogs y Tutoriales

- [Introducing Grounding with Bing Search](https://blogs.bing.com/search/January-2025/Introducing-Grounding-with-Bing-Search-in-Azure-AI-Agent-Service)
- [Azure AI Foundry Agent Service](https://azure.microsoft.com/en-us/blog/introducing-deep-research-in-azure-ai-foundry-agent-service/)

## ❓ Solución de Problemas

### Error: "BING_CONNECTION_ID not found"

**Solución**: Asegúrate de que has añadido la variable `BING_CONNECTION_ID` al archivo `.env` en la raíz del proyecto.

### Error: "Connection not found"

**Solución**: Verifica que:
1. Has creado la conexión de Bing Search en Azure AI Foundry
2. El Connection ID es correcto
3. Tienes permisos en el proyecto

### Error: "Unauthorized" o "403 Forbidden"

**Solución**:
1. Verifica que tu Bing Search API Key es válida
2. Comprueba que no has excedido la cuota de tu plan
3. Asegúrate de estar autenticado con `az login`

### Las búsquedas devuelven pocos resultados

**Solución**: Ajusta el parámetro `count` en BingGroundingTool:
```python
bing_tool = BingGroundingTool(
    connection_id=bing_connection_id,
    count=10  # Aumentar el número de resultados
)
```

### Los resultados no están en el idioma esperado

**Solución**: Configura correctamente `market` y `set_lang`:
```python
bing_tool = BingGroundingTool(
    connection_id=bing_connection_id,
    market="es-ES",
    set_lang="es"
)
```

## 🤝 Contribuciones

Si encuentras errores o tienes sugerencias para mejorar este módulo, por favor abre un issue en el repositorio del proyecto.

## 📄 Licencia

Este módulo es parte del proyecto AMAIA AI Agents Training.

---

**¡Disfruta construyendo tu agente de investigación de mercado con Bing Search! 🚀**
