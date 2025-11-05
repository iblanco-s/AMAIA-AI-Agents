#!/usr/bin/env python3
"""
Servidor MCP Remoto Personalizado para Gestión de Inventario Aeronáutico

Este servidor expone herramientas de inventario a través del protocolo MCP
usando transporte SSE (Server-Sent Events) para acceso remoto.
"""

import sys
from fastmcp import FastMCP

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
    Inicia el servidor MCP con transporte SSE en el puerto especificado.
    """
    # Obtener puerto desde argumentos de línea de comandos o usar 8000 por defecto
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"⚠️  Puerto inválido '{sys.argv[1]}', usando 8000 por defecto")

    print(f"🚀 Iniciando servidor MCP remoto en http://0.0.0.0:{port}")
    print("🛠️  Herramientas disponibles:")
    print("   - get_inventory_levels()")
    print("   - get_weekly_sales()")
    print("   - get_critical_items(threshold)")
    print("\n📡 Servidor listo para recibir conexiones remotas...")
    print("   Presiona Ctrl+C para detener el servidor\n")

    # Iniciar servidor con transporte SSE
    # NOTA: Usando 'fastmcp' (no 'mcp.server.fastmcp') que soporta estos parámetros
    mcp.run(transport="sse", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
