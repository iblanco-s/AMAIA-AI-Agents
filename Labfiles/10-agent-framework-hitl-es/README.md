# Módulo 10: Human-in-the-Loop con Microsoft Agent Framework

## Descripción General

Este módulo introduce el patrón **Human-in-the-Loop (HITL)** utilizando Microsoft Agent Framework. Aprenderás a construir agentes de IA que requieren aprobación humana antes de ejecutar acciones críticas.

## Conceptos Clave

### ¿Qué es Human-in-the-Loop?

Human-in-the-Loop es un patrón de diseño donde los sistemas de IA colaboran con humanos para tomar decisiones críticas. En lugar de depender únicamente de automatización, HITL garantiza que el juicio humano y la inteligencia artificial se complementen mutuamente.

### Características Principales

- 🔒 **Control sobre acciones críticas**: Aprobación humana requerida para operaciones importantes
- 🔄 **Flujo bidireccional**: El agente propone, el humano decide, el agente ejecuta
- ✅ **Aprobación o rechazo**: Los humanos pueden aprobar o rechazar solicitudes con feedback
- 🛡️ **Reducción de riesgos**: Previene errores costosos o acciones no autorizadas

## Contenido del Módulo

### Notebook: `human-in-the-loop-travel-agent.ipynb`

Este notebook contiene:

1. **Introducción a HITL**: Conceptos fundamentales y casos de uso
2. **Definición de funciones con aprobación**: Uso del parámetro `approval_mode="always_require"`
3. **Agente de reservas de viajes**: Ejemplo práctico con:
   - Búsqueda de vuelos (sin aprobación)
   - Reserva de vuelos (requiere aprobación)
   - Reserva de hoteles (requiere aprobación)
4. **Flujo de aprobación**: Demostración del ciclo completo
5. **Manejo de rechazos**: Qué sucede cuando se rechaza una aprobación

## Casos de Uso

El patrón HITL es ideal para:

- ✈️ **Reservas corporativas**: Viajes, eventos, recursos
- 💰 **Transacciones financieras**: Pagos, transferencias, autorizaciones
- 🏥 **Decisiones médicas**: Tratamientos, prescripciones
- ⚙️ **Cambios de infraestructura**: Configuraciones críticas, despliegues
- 📧 **Comunicaciones importantes**: Emails masivos, anuncios oficiales

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

### Funciones sin Aprobación

```python
@ai_function
def search_flights(...):
    # Operaciones de solo lectura no requieren aprobación
    pass
```

### Funciones con Aprobación

```python
@ai_function(approval_mode="always_require")
def book_flight(...):
    # Acciones críticas requieren aprobación humana
    pass
```

### Flujo de Trabajo

1. **Usuario solicita acción** → Envía mensaje al agente
2. **Agente procesa** → Busca información, propone acciones
3. **Sistema pausa** → Detecta función que requiere aprobación
4. **Humano revisa** → Examina la solicitud y decide
5. **Humano aprueba/rechaza** → `tool_call.approve()` o `tool_call.reject(reason)`
6. **Agente continúa** → Ejecuta si aprobado, o sugiere alternativas si rechazado

## Beneficios del Patrón HITL

✅ **Control**: Supervisión humana sobre decisiones críticas
✅ **Seguridad**: Reduce riesgos de errores costosos
✅ **Cumplimiento**: Ayuda con políticas y regulaciones
✅ **Balance**: Automatización eficiente + juicio humano
✅ **Transparencia**: Visibilidad total del proceso de toma de decisiones
✅ **Confianza**: Los usuarios confían más en sistemas con supervisión humana

## Mejores Prácticas

1. 🎯 **Identifica acciones críticas**: No todo necesita aprobación
2. 📝 **Proporciona contexto claro**: Los aprobadores necesitan información completa
3. ⚡ **Minimiza fricciones**: Solo requiere aprobación cuando es necesario
4. 🔄 **Maneja rechazos gracefully**: Ofrece alternativas o solicita más información
5. 📊 **Registra decisiones**: Mantén auditoría de aprobaciones/rechazos
6. ⏱️ **Considera timeouts**: Define qué pasa si no hay respuesta

## Ejecución

Para ejecutar el notebook:

1. Navega al directorio: `cd Labfiles/10-agent-framework-hitl-es/Python`
2. Asegúrate de tener las variables de entorno configuradas
3. Abre el notebook: `jupyter notebook human-in-the-loop-travel-agent.ipynb`
4. Ejecuta las celdas secuencialmente

## Recursos Adicionales

- [Microsoft Agent Framework Docs](https://learn.microsoft.com/en-us/agent-framework/)
- [Function Tools with Approvals](https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/function-tools-approvals)
- [Building HITL Workflows](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/building-human-in-the-loop-ai-workflows-with-microsoft-agent-framework/)

## Próximos Pasos

Después de completar este módulo, considera explorar:

- Módulo 11: Structured Outputs
- Integración con sistemas de aprobación empresariales
- Workflows multi-agente con múltiples puntos de aprobación
- Implementación de políticas de aprobación basadas en reglas
