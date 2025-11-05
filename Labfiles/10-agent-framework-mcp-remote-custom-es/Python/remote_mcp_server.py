"""
Servidor MCP Remoto para Gestión de Inventario Aeronáutico
===========================================================

Este servidor MCP expone herramientas de inventario vía HTTP/SSE
para ser consultado remotamente desde GitHub Codespaces u otros entornos.

Arquitectura:
- FastMCP: Define las herramientas de negocio
- SSE Server: Expone el servidor vía HTTP para acceso remoto
- Puerto: 8000 (configurable)

Uso:
    python remote_mcp_server.py

El servidor estará disponible en http://localhost:8000/sse
"""

from mcp.server.fastmcp import FastMCP
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear instancia FastMCP
mcp = FastMCP("AeroInventoryRemote")

@mcp.tool()
def get_inventory_levels() -> dict:
    """Devuelve el inventario actual de componentes aero clave en las plantas."""
    logger.info("Ejecutando get_inventory_levels")
    return {
        "Álabe de turbina (AP)": 6,
        "Carcasa del compresor": 8,
        "Conjunto de sello": 28,
        "Álabe guía de tobera": 5,
        "Carcasa del rodamiento": 12,
        "Eje": 9,
        "Difusor": 30,
        "Revestimiento del combustor": 3,
        "Bastidor frontal": 17,
        "Carcasa del ventilador": 45,
    }

@mcp.tool()
def get_weekly_sales() -> dict:
    """Devuelve el consumo semanal por órdenes de trabajo de la última semana."""
    logger.info("Ejecutando get_weekly_sales")
    return {
        "Álabe de turbina (AP)": 22,
        "Carcasa del compresor": 18,
        "Conjunto de sello": 3,
        "Álabe guía de tobera": 2,
        "Carcasa del rodamiento": 14,
        "Eje": 19,
        "Difusor": 4,
        "Revestimiento del combustor": 1,
        "Bastidor frontal": 13,
        "Carcasa del ventilador": 17,
    }

@mcp.tool()
def get_critical_items(threshold: int = 10) -> dict:
    """
    Devuelve componentes con inventario por debajo del umbral especificado.

    Args:
        threshold: Nivel mínimo de inventario para considerar un item como crítico
    """
    logger.info(f"Ejecutando get_critical_items con threshold={threshold}")
    inventory = get_inventory_levels()
    return {
        item: level
        for item, level in inventory.items()
        if level < threshold
    }

def main():
    """Inicia el servidor MCP remoto"""
    port = 8000
    logger.info(f"🚀 Iniciando servidor MCP remoto en http://0.0.0.0:{port}")
    logger.info("🛠️  Herramientas disponibles:")
    logger.info("   - get_inventory_levels()")
    logger.info("   - get_weekly_sales()")
    logger.info("   - get_critical_items(threshold)")

    # FastMCP incluye soporte para SSE cuando se ejecuta con uvicorn
    # Esto inicia el servidor en modo SSE automáticamente
    mcp.run(transport="sse", host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
