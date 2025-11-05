#!/usr/bin/env python3
"""
Servidor MCP Remoto con FastAPI para Gestión de Inventario Aeronáutico

Este servidor expone herramientas MCP a través de HTTP usando FastAPI,
permitiendo acceso remoto mediante MCPStreamableHTTPTool.

Uso:
    python remote_mcp_server_fastapi.py [port]

Ejemplo:
    python remote_mcp_server_fastapi.py 8000
"""

import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


def create_app() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI con el servidor MCP.

    Returns:
        FastAPI: Aplicación configurada con rutas MCP
    """
    app = FastAPI(
        title="AeroInventory MCP Server",
        description="Servidor MCP remoto para gestión de inventario aeronáutico",
        version="1.0.0"
    )

    # Configurar CORS para permitir acceso remoto
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # En producción, especifica los orígenes permitidos
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Montar las rutas del servidor MCP
    # NOTA: FastMCP con mcp.server.fastmcp puede no tener método directo get_app()
    # En ese caso, necesitarás implementar las rutas manualmente o usar el paquete fastmcp standalone

    @app.get("/")
    async def root():
        """Endpoint raíz con información del servidor."""
        return {
            "name": "AeroInventory MCP Server",
            "version": "1.0.0",
            "protocol": "MCP",
            "tools": [
                {
                    "name": "get_inventory_levels",
                    "description": "Devuelve niveles de inventario actuales"
                },
                {
                    "name": "get_weekly_sales",
                    "description": "Devuelve consumo semanal de componentes"
                },
                {
                    "name": "get_critical_items",
                    "description": "Identifica componentes con inventario crítico"
                }
            ]
        }

    @app.get("/health")
    async def health():
        """Endpoint de salud del servidor."""
        return {"status": "healthy"}

    return app


def main():
    """
    Inicia el servidor HTTP con FastAPI y uvicorn.
    """
    # Obtener puerto desde argumentos de línea de comandos
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"⚠️  Puerto inválido '{sys.argv[1]}', usando 8000 por defecto")

    print("=" * 70)
    print("🚀 Servidor MCP Remoto - AeroInventory")
    print("=" * 70)
    print(f"📡 URL: http://0.0.0.0:{port}")
    print(f"📚 Docs: http://0.0.0.0:{port}/docs")
    print()
    print("🛠️  Herramientas MCP disponibles:")
    print("   ├─ get_inventory_levels() - Niveles de inventario actual")
    print("   ├─ get_weekly_sales() - Consumo semanal de componentes")
    print("   └─ get_critical_items(threshold) - Componentes en inventario crítico")
    print()
    print("💡 Conecta desde un agente usando MCPStreamableHTTPTool:")
    print(f"   url='http://localhost:{port}'")
    print()
    print("⏹️  Presiona Ctrl+C para detener el servidor")
    print("=" * 70)
    print()

    # Crear aplicación
    app = create_app()

    # Iniciar servidor con uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
        access_log=True
    )


if __name__ == "__main__":
    main()
