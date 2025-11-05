# Servidor MCP Remoto Personalizado - Gestión de Inventario Aeronáutico

## 🔍 Problema Original

El error que encontraste:

```
TypeError: FastMCP.run() got an unexpected keyword argument 'host'
```

Ocurre porque hay **dos paquetes diferentes de FastMCP**:

1. **`mcp.server.fastmcp`** - Versión incluida en el paquete `mcp`, usada en los ejercicios locales
   - ❌ No soporta `transport="sse"`, `host="0.0.0.0"`, `port=8000`
   - ✅ Solo funciona con `mcp.run()` (sin parámetros) para modo stdio local

2. **`fastmcp`** - Paquete standalone más moderno
   - ✅ Soporta `transport="sse"`, `host`, `port` para servidores remotos
   - ❌ Requiere dependencias adicionales (`cffi`, `cryptography`) que pueden tener conflictos

## 📁 Soluciones Proporcionadas

Este directorio contiene tres implementaciones:

### 1. `remote_mcp_server.py` (Original - Requiere fastmcp standalone)

```python
from fastmcp import FastMCP  # Paquete standalone

mcp = FastMCP("AeroInventoryRemote")
# ... definir herramientas ...

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

**Requisitos:**
```bash
pip install fastmcp
```

**Uso:**
```bash
python remote_mcp_server.py [port]
```

### 2. `remote_mcp_server_simple.py` (Modo Local/Stdio)

```python
from mcp.server.fastmcp import FastMCP  # Versión incluida en mcp

mcp = FastMCP("AeroInventoryRemote")
# ... definir herramientas ...

if __name__ == "__main__":
    mcp.run()  # Sin parámetros - modo stdio
```

**Uso con MCPStdioTool:**
```python
from agent_framework import MCPStdioTool

async with MCPStdioTool(
    name="aeroinventory",
    command="python",
    args=["remote_mcp_server_simple.py"]
) as mcp_server:
    # Usar con tu agente
    pass
```

### 3. `remote_mcp_server_fastapi.py` (Recomendado para acceso remoto)

Servidor HTTP usando FastAPI + uvicorn, compatible con `mcp.server.fastmcp`.

**Requisitos:**
```bash
pip install fastapi uvicorn
```

**Uso:**
```bash
python remote_mcp_server_fastapi.py [port]
```

**Conectar desde un agente:**
```python
from agent_framework import MCPStreamableHTTPTool

async with MCPStreamableHTTPTool(
    name="aeroinventory",
    url="http://localhost:8000"
) as mcp_server:
    # Usar con tu agente
    pass
```

## 🛠️ Herramientas Disponibles

Todas las implementaciones exponen las mismas herramientas:

| Herramienta | Descripción | Parámetros |
|-------------|-------------|------------|
| `get_inventory_levels()` | Niveles actuales de inventario | Ninguno |
| `get_weekly_sales()` | Consumo semanal de componentes | Ninguno |
| `get_critical_items(threshold)` | Componentes con inventario bajo | `threshold: int = 10` |

## 📊 Datos de Inventario

### Componentes Aeronáuticos

El servidor gestiona los siguientes componentes:

- Álabe de turbina (AP)
- Carcasa del compresor
- Conjunto de sello
- Álabe guía de tobera
- Carcasa del rodamiento
- Eje
- Difusor
- Revestimiento del combustor
- Bastidor frontal
- Carcasa del ventilador

## 🚀 Inicio Rápido

### Opción A: Servidor Local (Más Simple)

```bash
# 1. Iniciar servidor
python remote_mcp_server_simple.py

# 2. En tu notebook/script Python
from agent_framework import ChatAgent, MCPStdioTool
from agent_framework.openai import OpenAIChatClient

async with MCPStdioTool(
    name="inventory",
    command="python",
    args=["remote_mcp_server_simple.py"]
) as mcp_server:
    async with ChatAgent(
        chat_client=client,
        name="InventoryAgent",
        instructions="Eres un asistente de inventario aeronáutico."
    ) as agent:
        result = await agent.run(
            "¿Qué componentes tienen menos de 10 unidades?",
            tools=mcp_server
        )
        print(result)
```

### Opción B: Servidor HTTP Remoto

```bash
# Terminal 1: Iniciar servidor HTTP
python remote_mcp_server_fastapi.py 8000

# Terminal 2: Cliente
from agent_framework import MCPStreamableHTTPTool

async with MCPStreamableHTTPTool(
    name="inventory",
    url="http://localhost:8000"
) as mcp_server:
    # ... usar con tu agente
```

## 🔧 Solución de Problemas

### Error: "TypeError: FastMCP.run() got an unexpected keyword argument 'host'"

**Causa:** Estás usando `mcp.server.fastmcp` pero intentando pasar parámetros de `fastmcp` standalone.

**Solución:**
- Opción 1: Cambiar a `from fastmcp import FastMCP` e instalar `pip install fastmcp`
- Opción 2: Usar `remote_mcp_server_simple.py` sin parámetros
- Opción 3: Usar `remote_mcp_server_fastapi.py` con FastAPI

### Error: "ModuleNotFoundError: No module named '_cffi_backend'"

**Causa:** Problemas de dependencias con el paquete `fastmcp` standalone.

**Solución:**
```bash
pip install cffi cryptography --upgrade
```

O usar las alternativas `remote_mcp_server_simple.py` o `remote_mcp_server_fastapi.py`.

## 📚 Referencias

- [FastMCP Documentation](https://gofastmcp.com/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Agent Framework Documentation](https://github.com/microsoft/agent-framework)

## 💡 Recomendaciones

1. **Para desarrollo local:** Usa `remote_mcp_server_simple.py` con `MCPStdioTool`
2. **Para producción/remoto:** Usa `remote_mcp_server_fastapi.py` con `MCPStreamableHTTPTool`
3. **Para máxima compatibilidad:** Evita el paquete `fastmcp` standalone si tienes problemas de dependencias

---

**Nota:** Este código es parte del módulo 10 de los ejercicios de AMAIA-AI-Agents sobre servidores MCP personalizados.
