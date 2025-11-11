# Módulo 11: Structured Outputs con Microsoft Agent Framework

## Descripción General

Este módulo enseña cómo crear agentes que producen **salidas estructuradas** en forma de objetos JSON que se ajustan a esquemas específicos. Aprenderás a garantizar que las respuestas de la IA tengan un formato predecible y procesable.

## Conceptos Clave

### ¿Qué son Structured Outputs?

Las salidas estructuradas garantizan que las respuestas del agente sigan un formato JSON específico definido por un esquema. En lugar de obtener texto libre que requiere parsing complejo, obtienes datos estructurados que tu aplicación puede procesar de manera confiable.

### Características Principales

- 📋 **Esquemas definidos con Pydantic**: Modelos de datos con tipado fuerte
- ✅ **Validación automática**: Garantía de formato correcto
- 🔄 **Conversión directa**: JSON a objetos Python sin parsing manual
- 🎯 **Respuestas predecibles**: Siempre el mismo formato de salida
- 🏗️ **Modelos anidados**: Soporte para estructuras complejas

## Contenido del Módulo

### Notebook: `structured-outputs-product-extractor.ipynb`

Este notebook contiene tres ejemplos completos:

#### 1. Extracción de Información de Productos
- Define esquema `ProductInfo` con Pydantic
- Extrae datos estructurados de descripciones en texto libre
- Incluye especificaciones técnicas anidadas
- Maneja campos opcionales y requeridos

#### 2. Catálogo de Múltiples Productos
- Esquema `ProductCatalog` para múltiples productos
- Extracción en batch de información
- Conteo y organización automática

#### 3. Análisis de Reseñas con Sentimiento
- Esquema `ReviewAnalysis` con enum para sentimiento
- Extracción de pros/cons
- Clasificación de sentimiento (positivo/neutral/negativo)
- Validación de rangos (calificación 1-5)

## Casos de Uso

Las salidas estructuradas son ideales para:

- 📦 **E-commerce**: Extracción de datos de productos
- 📄 **Procesamiento de documentos**: Facturas, contratos, formularios
- 🎫 **Sistemas de tickets**: Clasificación y extracción de información
- 📊 **Generación de reportes**: Datos financieros, métricas, KPIs
- 🏷️ **Clasificación de contenido**: Etiquetado, categorización
- ⭐ **Análisis de reseñas**: Sentimiento, pros/cons
- 👥 **Extracción de datos de CV**: Habilidades, experiencia, educación
- 🏥 **Registros médicos**: Diagnósticos, síntomas, tratamientos

## Requisitos

### Dependencias

```bash
pip install agent-framework pydantic
```

### Variables de Entorno

```bash
export GITHUB_TOKEN="your_github_token"
export GITHUB_MODEL="openai/gpt-4o"  # Opcional
```

## Estructura del Código

### Definir Esquemas con Pydantic

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class ProductInfo(BaseModel):
    name: str = Field(description="Nombre del producto")
    price: float = Field(description="Precio en euros")
    features: List[str] = Field(description="Características")
    rating: Optional[float] = Field(None, description="Calificación")
```

### Configurar Agente con Structured Output

```python
async with ChatAgent(
    chat_client=client,
    name="extractor",
    instructions="...",
    response_format=ProductInfo  # ⭐ Especifica el esquema
) as agent:
    response = await agent.run([prompt])
    product = ProductInfo.model_validate_json(response.content)
```

## Tipos de Datos Soportados

| Tipo Python | Descripción | Ejemplo |
|-------------|-------------|---------|
| `str` | Cadena de texto | "MacBook Pro" |
| `int` | Número entero | 42 |
| `float` | Número decimal | 1299.99 |
| `bool` | Booleano | True/False |
| `List[T]` | Lista de elementos | ["feature1", "feature2"] |
| `Optional[T]` | Valor opcional (puede ser None) | None o "value" |
| `Enum` | Valores restringidos | Sentiment.POSITIVE |
| `BaseModel` | Modelo anidado | ProductSpecifications |

## Validaciones con Pydantic

### Rangos Numéricos

```python
rating: int = Field(ge=1, le=5)  # Entre 1 y 5
```

### Longitudes de Texto

```python
name: str = Field(min_length=1, max_length=100)
```

### Valores por Defecto

```python
in_stock: bool = Field(default=True)
```

### Enums para Valores Restringidos

```python
from enum import Enum

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
```

## Beneficios vs Texto Libre

| Aspecto | Texto Libre | Structured Output |
|---------|-------------|-------------------|
| **Formato** | Inconsistente | Siempre JSON válido |
| **Parsing** | Regex/NLP complejo | Directo a objetos Python |
| **Validación** | Manual y propensa a errores | Automática con Pydantic |
| **Tipado** | Todo son strings | Tipos nativos (int, float, bool) |
| **Confiabilidad** | Variable | Garantizada |
| **Integración** | Requiere mucho código | Inmediata |
| **Mantenimiento** | Alto | Bajo |

## Mejores Prácticas

1. 📝 **Descripciones claras**: Usa el parámetro `description` en todos los campos
   ```python
   name: str = Field(description="Nombre completo del producto")
   ```

2. 🎯 **Tipos específicos**: Usa Enum cuando hay valores limitados
   ```python
   class Status(str, Enum):
       PENDING = "pending"
       APPROVED = "approved"
   ```

3. ✨ **Campos opcionales**: Marca como `Optional` lo que puede no estar disponible
   ```python
   rating: Optional[float] = Field(None, description="...")
   ```

4. 🔍 **Validaciones**: Define restricciones apropiadas
   ```python
   price: float = Field(gt=0, description="Precio debe ser positivo")
   ```

5. 🏗️ **Modelos anidados**: Usa composición para estructuras complejas
   ```python
   class Product(BaseModel):
       specs: ProductSpecifications  # Modelo anidado
   ```

6. 📋 **Instrucciones al agente**: Sé explícito sobre qué extraer
   ```python
   instructions="Extrae TODA la información disponible. Si un campo no está, usa null."
   ```

## Ejemplos de Output

### Producto Individual

```json
{
  "name": "MacBook Pro 16\"",
  "category": "Laptops",
  "brand": "Apple",
  "price": 2899.99,
  "description": "Laptop profesional con chip M3 Pro",
  "features": [
    "Chip M3 Pro",
    "16GB RAM",
    "512GB SSD"
  ],
  "specifications": {
    "weight": "2.15 kg",
    "dimensions": "35.57 x 24.81 x 1.68 cm",
    "color": "Gris espacial"
  },
  "in_stock": true,
  "rating": 4.8
}
```

### Catálogo de Productos

```json
{
  "store_name": "TechStore",
  "category": "Smartphones",
  "total_products": 3,
  "products": [
    {"name": "iPhone 15 Pro", "price": 1349.99, ...},
    {"name": "Galaxy S24", "price": 1299.99, ...},
    {"name": "Pixel 9 Pro", "price": 1099.99, ...}
  ]
}
```

## Ejecución

Para ejecutar el notebook:

1. Navega al directorio: `cd Labfiles/11-agent-framework-structured-outputs-es/Python`
2. Asegúrate de tener las variables de entorno configuradas
3. Abre el notebook: `jupyter notebook structured-outputs-product-extractor.ipynb`
4. Ejecuta las celdas secuencialmente

## Comparación con Function Calling

| Característica | Function Calling | Structured Outputs |
|----------------|------------------|-------------------|
| **Propósito** | Ejecutar acciones | Extraer/generar datos |
| **Salida** | Resultado de función | JSON estructurado |
| **Validación** | En la función | Automática con schema |
| **Uso** | Operaciones, APIs | Análisis, extracción |

**Cuándo usar cada uno:**
- ⚙️ **Function Calling**: Cuando necesitas que el agente **haga algo**
- 📊 **Structured Outputs**: Cuando necesitas que el agente **extraiga o genere datos**

## Recursos Adicionales

- [Microsoft Agent Framework Docs](https://learn.microsoft.com/en-us/agent-framework/)
- [Structured Outputs Tutorial](https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/structured-output)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Próximos Pasos

Después de completar este módulo, considera:

- Combinar structured outputs con function calling
- Crear pipelines de extracción de datos complejos
- Integrar con bases de datos para almacenar datos extraídos
- Construir APIs que usen structured outputs para respuestas consistentes
- Explorar validación avanzada con Pydantic validators

## Troubleshooting

### El agente no respeta el esquema
- ✅ Verifica que uses `response_format=YourModel`
- ✅ Asegúrate que el modelo LLM soporte structured outputs
- ✅ Revisa que las instrucciones sean claras

### Errores de validación
- ✅ Marca campos opcionales como `Optional[T]`
- ✅ Verifica que los tipos sean correctos
- ✅ Revisa las restricciones (ge, le, etc.)

### Campos faltantes
- ✅ Instruye al agente explícitamente sobre qué hacer si falta información
- ✅ Usa valores por defecto cuando sea apropiado
- ✅ Marca campos como `Optional` si pueden no estar
