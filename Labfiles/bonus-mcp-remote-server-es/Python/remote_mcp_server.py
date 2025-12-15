
import asyncio

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "EventManagementService",
    streamable_http_path="/api/mcp",
    host="0.0.0.0",
    port=8000,
    json_response=True,
)

@mcp.tool()
def get_available_rooms() -> dict:
    """Devuelve las salas de eventos disponibles con su capacidad y disponibilidad actual."""
    return {
        "Sala Ejecutiva A": {"capacidad": 20, "disponible": True, "equipamiento": "Proyector, Videoconferencia"},
        "Sala Conferencias B": {"capacidad": 50, "disponible": False, "equipamiento": "Proyector, Sistema de audio"},
        "Sala Reuniones C": {"capacidad": 10, "disponible": True, "equipamiento": "Pizarra digital"},
        "Auditorio Principal": {"capacidad": 200, "disponible": True, "equipamiento": "Escenario, Sonido profesional, Iluminación"},
        "Sala de Formación D": {"capacidad": 30, "disponible": True, "equipamiento": "Ordenadores, Proyector"},
        "Sala Creative Lab": {"capacidad": 15, "disponible": False, "equipamiento": "Pizarra, Material de diseño"},
        "Sala VIP": {"capacidad": 12, "disponible": True, "equipamiento": "Videoconferencia premium, Catering"},
        "Terraza Eventos": {"capacidad": 80, "disponible": True, "equipamiento": "Al aire libre, Toldo"},
    }

@mcp.tool()
def get_upcoming_events() -> dict:
    """Devuelve los eventos programados para la próxima semana con sus detalles."""
    return {
        "Lunes 9:00 - Reunión Junta Directiva": {"sala": "Sala Ejecutiva A", "asistentes": 15, "organizador": "CEO Office"},
        "Lunes 14:00 - Presentación Producto Q4": {"sala": "Auditorio Principal", "asistentes": 150, "organizador": "Marketing"},
        "Martes 10:00 - Capacitación Técnica": {"sala": "Sala de Formación D", "asistentes": 25, "organizador": "RRHH"},
        "Miércoles 11:00 - Workshop Innovación": {"sala": "Sala Creative Lab", "asistentes": 12, "organizador": "I+D"},
        "Jueves 16:00 - Reunión Clientes": {"sala": "Sala VIP", "asistentes": 8, "organizador": "Ventas"},
        "Viernes 12:00 - Team Building": {"sala": "Terraza Eventos", "asistentes": 60, "organizador": "RRHH"},
        "Viernes 15:00 - Conferencia Internacional": {"sala": "Sala Conferencias B", "asistentes": 45, "organizador": "Operaciones"},
    }

if __name__ == "__main__":
    # Run the MCP HTTP server with the specified configuration
    asyncio.run(mcp.run_streamable_http_async())
