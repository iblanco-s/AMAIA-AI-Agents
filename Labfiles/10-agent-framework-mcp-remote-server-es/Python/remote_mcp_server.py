
import asyncio

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "InventoryService",
    streamable_http_path="/api/mcp",
    host="0.0.0.0",
    port=8000,
    json_response=True,
)

@mcp.tool()
def get_inventory_levels() -> dict:
    """Devuelve el inventario actual de productos en el centro de distribución."""
    return {
        "Laptop": 12,
        "Monitor": 25,
        "Teclado inalámbrico": 40,
        "Mouse ergonómico": 34,
        "Router WiFi": 18,
        "Auriculares": 27,
        "Webcam": 15,
        "Disco duro externo": 21,
        "Silla ergonómica": 10,
        "Escritorio ajustable": 8,
    }

@mcp.tool()
def get_weekly_sales() -> dict:
    """Devuelve el consumo semanal por órdenes de trabajo de la última semana."""
    return {
        "Laptop": 9,
        "Monitor": 14,
        "Teclado inalámbrico": 7,
        "Mouse ergonómico": 6,
        "Router WiFi": 5,
        "Auriculares": 11,
        "Webcam": 4,
        "Disco duro externo": 8,
        "Silla ergonómica": 3,
        "Escritorio ajustable": 2,
    }

if __name__ == "__main__":
    # Ejecuta el servidor HTTP de MCP con la configuración indicada
    asyncio.run(mcp.run_streamable_http_async())
