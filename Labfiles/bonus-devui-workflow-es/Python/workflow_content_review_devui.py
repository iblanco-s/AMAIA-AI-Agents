# pip install agent-framework-devui==1.0.0b251016
import os
from typing import Any

from agent_framework import AgentExecutorResponse, WorkflowBuilder
from agent_framework.openai import OpenAIChatClient
from pydantic import BaseModel

# Configurar el cliente para usar GitHub Models
MODEL_NAME = os.getenv("GITHUB_MODEL", "openai/gpt-4o")

client = OpenAIChatClient(
    base_url="https://models.github.ai/inference",
    api_key=os.environ["GITHUB_TOKEN"],
    model_id=MODEL_NAME,
)


# Definir salida estructurada para evaluación de proyectos
class ProjectEvaluation(BaseModel):
    """Evaluación de viabilidad del proyecto con puntajes detallados."""

    overall_score: int  # Puntaje general de viabilidad (0-100)
    feedback: str  # Retroalimentación breve y recomendaciones
    estimated_budget: float  # Presupuesto estimado en euros


# Definir salida estructurada para decisión del Aprobador
class ApprovalDecision(BaseModel):
    """Decisión del director financiero sobre el proyecto."""

    approved: bool  # True = aprobado, False = rechazado
    decision_type: str  # "APROBADO", "APROBADO_CON_CONDICIONES", o "RECHAZADO"
    reason: str  # Motivo de la decisión (máximo 50 palabras)
    conditions: str  # Condiciones si aplica, o "N/A"


# Función de condición: aprobación directa (presupuesto bajo)
def direct_approval(message: Any) -> bool:
    """Verificar si el proyecto puede aprobarse directamente (presupuesto < 50K)."""
    if not isinstance(message, AgentExecutorResponse):
        return True
    try:
        evaluation = ProjectEvaluation.model_validate_json(message.agent_run_response.text)
        return evaluation.estimated_budget < 50000
    except Exception:
        return True


# Función de condición: requiere aprobación presupuestaria (presupuesto alto)
def requires_budget_approval(message: Any) -> bool:
    """Verificar si requiere aprobación humana por presupuesto elevado (>= 50K)."""
    if not isinstance(message, AgentExecutorResponse):
        return False
    try:
        evaluation = ProjectEvaluation.model_validate_json(message.agent_run_response.text)
        return evaluation.estimated_budget >= 50000
    except Exception:
        return False


# Función de condición: proyecto aprobado por el Aprobador
def project_approved(message: Any) -> bool:
    """Verificar si el Aprobador aprobó el proyecto."""
    if not isinstance(message, AgentExecutorResponse):
        return True
    try:
        decision = ApprovalDecision.model_validate_json(message.agent_run_response.text)
        return decision.approved
    except Exception:
        return True


# Función de condición: proyecto rechazado por el Aprobador
def project_rejected(message: Any) -> bool:
    """Verificar si el Aprobador rechazó el proyecto."""
    if not isinstance(message, AgentExecutorResponse):
        return False
    try:
        decision = ApprovalDecision.model_validate_json(message.agent_run_response.text)
        return not decision.approved
    except Exception:
        return False


# Función de Solicitante - genera la propuesta inicial del proyecto
requester = client.create_agent(
    name="Solicitante",
    instructions=(
        "Eres un gerente de proyectos que prepara propuestas corporativas. "
        "Genera una propuesta BREVE (máximo 150 palabras) con: objetivos, alcance y beneficios esperados. "
        "Sé conciso y profesional."
    ),
)

# Crear agente Evaluador - evalúa viabilidad con puntajes estructurados
evaluator = client.create_agent(
    name="Evaluador",
    instructions=(
        "Eres un analista de proyectos. Evalúa la propuesta y devuelve: "
        "overall_score (0-100), feedback (máximo 50 palabras) y estimated_budget en euros. "
        "Sé conciso."
    ),
    response_format=ProjectEvaluation,
)

# Crear agente Aprobador - decide automáticamente basándose en criterios de negocio
approver = client.create_agent(
    name="Aprobador",
    instructions=(
        "Eres el director financiero. Analiza la evaluación previa y decide:\n\n"
        "CRITERIOS DE APROBACIÓN:\n"
        "- approved=true, decision_type='APROBADO' si: overall_score >= 75\n"
        "- approved=true, decision_type='APROBADO_CON_CONDICIONES' si: overall_score entre 60-74\n"
        "- approved=false, decision_type='RECHAZADO' si: overall_score < 60 O presupuesto > 2M sin justificación\n\n"
        "Devuelve tu decisión en el formato estructurado requerido."
    ),
    response_format=ApprovalDecision,
)

# Crear agente Finalizador de Rechazo - cierra el flujo cuando se rechaza
rejection_finalizer = client.create_agent(
    name="Finalizador_Rechazo",
    instructions=(
        "El proyecto ha sido RECHAZADO por el director financiero. "
        "Genera un informe final BREVE (máximo 80 palabras) explicando:\n"
        "1. Motivo del rechazo\n"
        "2. Recomendaciones para futuras propuestas\n"
        "Sé profesional y constructivo."
    ),
)

# Crear agente Documentador - genera documentación final
documenter = client.create_agent(
    name="Documentador",
    instructions=(
        "Eres un especialista en documentación. "
        "Crea documentación BREVE del proyecto (máximo 150 palabras) con estructura clara."
    ),
)

# Crear agente Resumidor - crea el informe final de publicación
summarizer = client.create_agent(
    name="Resumidor",
    instructions=(
        "Crea un informe final CONCISO (máximo 100 palabras): "
        "resumen del proyecto, ruta seguida (aprobación directa o con aprobación presupuestaria) y conclusión."
    ),
)

# Construir flujo de trabajo con ramificación y convergencia:
# Solicitante → Evaluador → [2 ramas según presupuesto]:
#   - Si presupuesto < 50K: → Documentador → Resumidor (aprobación directa)
#   - Si presupuesto >= 50K: → Aprobador → [2 ramas según decisión]:
#       - Si aprobado: → Documentador → Resumidor
#       - Si rechazado: → Finalizador_Rechazo (FIN)
workflow = (
    WorkflowBuilder(
        name="Flujo de Trabajo de Evaluación de Proyectos",
        description="Evaluación de proyectos con 2 rutas según presupuesto (Solicitante → Evaluador → Aprobador/Documentador)",
    )
    .set_start_executor(requester)
    .add_edge(requester, evaluator)
    # Rama 1: Aprobación directa (presupuesto < 50K)
    .add_edge(evaluator, documenter, condition=direct_approval)
    # Rama 2: Requiere aprobación presupuestaria (presupuesto >= 50K)
    .add_edge(evaluator, approver, condition=requires_budget_approval)
    # Sub-rama 2a: Aprobador aprueba → continúa a Documentador
    .add_edge(approver, documenter, condition=project_approved)
    # Sub-rama 2b: Aprobador rechaza → termina en Finalizador_Rechazo
    .add_edge(approver, rejection_finalizer, condition=project_rejected)
    # Ambas rutas de aprobación convergen: Documentador → Resumidor
    .add_edge(documenter, summarizer)
    .build()
)


def main():
    from agent_framework.devui import serve

    serve(entities=[workflow], port=8093, auto_open=True)


if __name__ == "__main__":
    main()
