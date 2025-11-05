#!/usr/bin/env python3
"""
Servidor MCP Remoto Simplificado para Gestión de Inventario Aeronáutico

Este servidor usa el paquete mcp.server.fastmcp que ya está disponible
en el entorno. Para uso remoto, necesitarás usar un proxy reverso o
FastAPI wrapper.
"""

from mcp.server.fastmcp import FastMCP

# Crear instancia del servidor MCP
mcp = FastMCP("AeroInventoryRemote")


@mcp.tool()
def get_inventory_levels() -> dict:
    """
    Devuelve el inventario actual de componentes aeronáuticos clave en las plantas.

    Returns:
        dict: Diccionario con nombres de componentes y sus niveles de inventario actuales
    """
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
    """
    Devuelve el consumo semanal por órdenes de trabajo de la última semana.

    Returns:
        dict: Diccionario con nombres de componentes y su consumo semanal
    """
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
    Identifica componentes con niveles de inventario por debajo del umbral especificado.

    Args:
        threshold: Nivel mínimo de inventario para considerar un componente como crítico

    Returns:
        dict: Diccionario con componentes críticos y sus niveles actuales
    """
    inventory = get_inventory_levels()
    critical = {
        item: level
        for item, level in inventory.items()
        if level < threshold
    }
    return critical


def main():
    """
    Inicia el servidor MCP en modo local/stdio.

    Para acceso remoto, este servidor debe ser envuelto con FastAPI o similar.
    Ver remote_mcp_server_fastapi.py para una implementación completa con HTTP.
    """
    print("🚀 Iniciando servidor MCP (modo local/stdio)")
    print("🛠️  Herramientas disponibles:")
    print("   - get_inventory_levels()")
    print("   - get_weekly_sales()")
    print("   - get_critical_items(threshold)")
    print("\n📝 NOTA: Este servidor corre en modo stdio (comunicación estándar)")
    print("   Para acceso remoto HTTP/SSE, usa remote_mcp_server_fastapi.py\n")

    # Modo stdio (estándar) - usado con MCPStdioTool
    mcp.run()


if __name__ == "__main__":
    main()
