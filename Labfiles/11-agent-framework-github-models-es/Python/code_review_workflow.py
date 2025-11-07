# pip install agent-framework-devui==1.0.0b251016
import os
from typing import Any

from agent_framework import AgentExecutorResponse, WorkflowBuilder
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv
from pydantic import BaseModel

# Cargar variables de entorno
load_dotenv(override=True)

# Configurar el cliente para usar exclusivamente los modelos de GitHub
client = OpenAIChatClient(
    base_url="https://models.github.ai/inference",
    api_key=os.environ["GITHUB_TOKEN"],
    model_id=os.getenv("GITHUB_MODEL", "openai/gpt-4o"),
)

# Definir la salida estructurada para los resultados de la revisión de código
class CodeReviewResult(BaseModel):
    """Evaluación de la revisión de código con puntuaciones y retroalimentación."""
    score: int  # Puntuación de calidad general (0-100)
    feedback: str  # Retroalimentación concisa y accionable
    efficiency: int  # Puntuación de eficiencia (0-100)
    style_compliance: int  # Puntuación de cumplimiento de estilo (0-100)
    correctness: int  # Puntuación de corrección (0-100)
    readability: int  # Puntuación de legibilidad (0-100)

# Función de condición: dirigir al agente de refactorización si la puntuación es < 85
def needs_refactoring(message: Any) -> bool:
    """Comprueba si el código necesita refactorización basándose en la puntuación de la revisión."""
    if not isinstance(message, AgentExecutorResponse):
        return False
    try:
        review = CodeReviewResult.model_validate_json(message.agent_run_response.text)
        return review.score < 85
    except Exception:
        return False

# Función de condición: el código está aprobado (puntuación >= 85)
def is_approved(message: Any) -> bool:
    """Comprueba si el código está aprobado (alta calidad)."""
    if not isinstance(message, AgentExecutorResponse):
        return True
    try:
        review = CodeReviewResult.model_validate_json(message.agent_run_response.text)
        return review.score >= 85
    except Exception:
        return True

# Crear Agente Desarrollador (DeveloperAgent) - escribe código
developer_agent = client.create_agent(
    name="DeveloperAgent",
    instructions=(
        "Eres un desarrollador de software experto. "
        "Escribe una función de Python clara y eficiente basada en el requerimiento del usuario. "
        "Concéntrate en la corrección, eficiencia y buenas prácticas de codificación."
    ),
)

# Crear Agente Revisor de Código (CodeReviewerAgent) - evalúa y proporciona retroalimentación estructurada
code_reviewer_agent = client.create_agent(
    name="CodeReviewerAgent",
    instructions=(
        "Eres un experto revisor de código. "
        "Evalúa la función de Python proporcionada basándote en:\n"
        "1. Corrección - ¿Funciona como se espera?\n"
        "2. Eficiencia - ¿Es computacionalmente eficiente?\n"
        "3. Cumplimiento de Estilo - ¿Sigue las guías de estilo de Python (PEP 8)?\n"
        "4. Legibilidad - ¿Es fácil de entender el código?\n\n"
        "Devuelve un objeto JSON con:\n"
        "- score: calidad general (0-100)\n"
        "- feedback: retroalimentación concisa y accionable para mejorar\n"
        "- correctness, efficiency, style_compliance, readability: puntuaciones individuales (0-100)"
    ),
    response_format=CodeReviewResult,
)

# Crear Agente de Refactorización (RefactorAgent) - mejora el código basándose en la retroalimentación
refactor_agent = client.create_agent(
    name="RefactorAgent",
    instructions=(
        "Eres un programador experto en refactorización. "
        "Recibirás una función de Python junto con retroalimentación de la revisión. "
        "Mejora el código abordando todos los problemas mencionados en la retroalimentación. "
        "Mantén la intención original mientras mejoras la corrección, eficiencia, estilo y legibilidad."
    ),
)

# Crear Agente de Documentación (DocumentationAgent) - añade comentarios y docstrings
documentation_agent = client.create_agent(
    name="DocumentationAgent",
    instructions=(
        "Eres un especialista en documentación técnica. "
        "Recibirás una función de Python que ha sido aprobada o refactorizada. "
        "Añade comentarios claros y un docstring completo que explique qué hace la función, "
        "sus parámetros y qué devuelve."
    ),
)

# Crear Agente de Informes (ReportAgent) - crea un informe final del proceso
report_agent = client.create_agent(
    name="ReportAgent",
    instructions=(
        "Eres un agente de informes. "
        "Crea un informe final del proceso de desarrollo que incluya:\n"
        "1. Un resumen de la función desarrollada\n"
        "2. La ruta del flujo de trabajo seguida (aprobación directa o refactorización)\n"
        "3. Las métricas clave de la revisión de código\n"
        "Mantenlo conciso y profesional."
    ),
)

# Construir el flujo de trabajo con ramificación y convergencia:
# DeveloperAgent → CodeReviewerAgent → [ramificaciones]:
#   - Si la puntuación >= 85: → DocumentationAgent → ReportAgent (ruta de aprobación directa)
#   - Si la puntuación < 85: → RefactorAgent → DocumentationAgent → ReportAgent (ruta de mejora)
# Ambas rutas convergen en ReportAgent para el informe final
workflow = (
    WorkflowBuilder(
        name="Flujo de Trabajo de Revisión de Código",
        description="Creación de código multi-agente con enrutamiento basado en calidad (Developer→Reviewer→Refactor/Documentation)",
    )
    .set_start_executor(developer_agent)
    .add_edge(developer_agent, code_reviewer_agent)
    # Rama 1: Alta calidad (>= 85) va directamente a documentación
    .add_edge(code_reviewer_agent, documentation_agent, condition=is_approved)
    # Rama 2: Baja calidad (< 85) va primero a refactorización, luego a documentación
    .add_edge(code_reviewer_agent, refactor_agent, condition=needs_refactoring)
    .add_edge(refactor_agent, documentation_agent)
    # Ambas rutas convergen: DocumentationAgent → ReportAgent
    .add_edge(documentation_agent, report_agent)
    .build()
)

def main():
    from agent_framework.devui import serve
    serve(entities=[workflow], port=8094, auto_open=True)

if __name__ == "__main__":
    main()
