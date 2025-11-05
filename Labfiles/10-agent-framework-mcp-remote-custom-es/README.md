# Módulo 10: Agente con MCP Remoto Personalizado

## 📋 Descripción General

Este módulo demuestra cómo crear y desplegar un **servidor MCP (Model Context Protocol) remoto personalizado** para gestión de inventario aeronáutico, diseñado específicamente para ejecutarse en **GitHub Codespaces** u otros entornos de desarrollo en la nube.

### 🆚 Diferencias con el Módulo 7 (MCP Local)

| Característica | Módulo 7 (MCP Local) | Módulo 10 (MCP Remoto) |
|----------------|----------------------|------------------------|
| **Protocolo** | stdio (procesos) | HTTP/SSE (red) |
| **Herramienta** | `MCPStdioTool` | `MCPStreamableHTTPTool` |
| **Despliegue** | Proceso local Python | Servidor HTTP en puerto 8000 |
| **Escalabilidad** | 1 cliente por servidor | Múltiples clientes simultáneos |
| **Ubicación** | Mismo proceso | Servidor independiente (local/remoto) |
| **Uso ideal** | Desarrollo local rápido | Producción, cloud, multi-cliente |

## 🏗️ Arquitectura

```
┌─────────────────────┐
│   Jupyter Notebook  │
│  (Cliente Agente)   │
└──────────┬──────────┘
           │
           │ HTTP/SSE
           │
           ▼
┌─────────────────────┐
│   Servidor MCP      │
│   (Puerto 8000)     │
├─────────────────────┤
│  Herramientas:      │
│  • get_inventory    │
│  • get_weekly_sales │
│  • get_critical     │
└─────────────────────┘
```

## 📁 Estructura de Archivos

```
10-agent-framework-mcp-remote-custom-es/
├── README.md                                    # Este archivo
├── Python/
│   ├── remote_mcp_server.py                     # Servidor MCP remoto
│   ├── mcp-remote-custom-inventory-agent.ipynb  # Cliente notebook
│   └── start_server.sh                          # Script de inicio (opcional)
```

## 🚀 Inicio Rápido

### Opción 1: Inicio Manual (Recomendado para aprendizaje)

#### 1. Iniciar el Servidor MCP Remoto

Abre una **terminal separada** y ejecuta:

```bash
cd Labfiles/10-agent-framework-mcp-remote-custom-es/Python
python remote_mcp_server.py
```

Deberías ver:
```
🚀 Iniciando servidor MCP remoto en http://0.0.0.0:8000
🛠️  Herramientas disponibles:
   - get_inventory_levels()
   - get_weekly_sales()
   - get_critical_items(threshold)
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 2. Ejecutar el Notebook Cliente

En otra terminal o en Jupyter/VS Code:

```bash
cd Labfiles/10-agent-framework-mcp-remote-custom-es/Python
jupyter notebook mcp-remote-custom-inventory-agent.ipynb
```

O abre el archivo `.ipynb` directamente en VS Code y ejecuta las celdas secuencialmente.

### Opción 2: Inicio con Script

```bash
cd Labfiles/10-agent-framework-mcp-remote-custom-es/Python
chmod +x start_server.sh
./start_server.sh
```

El servidor se ejecutará en segundo plano. Para detenerlo:
```bash
pkill -f remote_mcp_server.py
```

## 🛠️ Herramientas Disponibles

El servidor MCP expone tres herramientas:

### 1. `get_inventory_levels()`
Devuelve el inventario actual de componentes aeronáuticos clave.

**Ejemplo de respuesta:**
```json
{
  "Álabe de turbina (AP)": 6,
  "Carcasa del compresor": 8,
  "Conjunto de sello": 28,
  ...
}
```

### 2. `get_weekly_sales()`
Devuelve el consumo semanal de componentes de la última semana.

**Ejemplo de respuesta:**
```json
{
  "Álabe de turbina (AP)": 22,
  "Carcasa del compresor": 18,
  "Conjunto de sello": 3,
  ...
}
```

### 3. `get_critical_items(threshold: int = 10)`
Devuelve componentes con inventario por debajo del umbral especificado.

**Parámetros:**
- `threshold` (int): Nivel mínimo de inventario (por defecto: 10)

**Ejemplo de uso:**
```python
get_critical_items(threshold=15)
```

## 📊 Ejemplos de Consultas

### Ejemplo 1: Componentes con inventario bajo
```
"Lista los componentes con inventario < 15 y su consumo semanal."
```

### Ejemplo 2: Análisis de riesgo
```
"¿Qué piezas podrían agotarse esta semana considerando el consumo semanal y el inventario actual?"
```

### Ejemplo 3: Análisis completo
```
"Dame un análisis completo del inventario:
1) Componentes con mayor demanda vs inventario disponible
2) Prioridad de reorden basada en días de cobertura
3) Componentes con sobre-stock"
```

## 🌐 Uso en GitHub Codespaces

### Exponer el Puerto Públicamente

1. En Codespaces, ve a la pestaña **PORTS**
2. Busca el puerto `8000`
3. Click derecho → **Port Visibility** → **Public**
4. Copia la URL generada (ej: `https://username-repo-xxx.githubpreview.dev`)

### Conectar desde Otro Cliente

Modifica el notebook para usar la URL pública:

```python
async with (
    MCPStreamableHTTPTool(
        name="aeroinventory_remote",
        url="https://tu-codespace-url.githubpreview.dev/sse",
    ) as mcp_server,
    ...
)
```

## 🔧 Configuración Avanzada

### Cambiar el Puerto del Servidor

Edita `remote_mcp_server.py`:

```python
def main():
    port = 9000  # Cambia aquí
    mcp.run(transport="sse", host="0.0.0.0", port=port)
```

### Agregar Autenticación

Para producción, agrega headers de autenticación:

**Servidor (`remote_mcp_server.py`):**
```python
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

# Agregar validación de tokens
```

**Cliente (notebook):**
```python
MCPStreamableHTTPTool(
    name="aeroinventory_remote",
    url="http://localhost:8000/sse",
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)
```

### Conectar a Base de Datos Real

Modifica las herramientas en `remote_mcp_server.py` para consultar una DB:

```python
import sqlite3

@mcp.tool()
def get_inventory_levels() -> dict:
    conn = sqlite3.connect('inventory.db')
    cursor = conn.execute("SELECT component, quantity FROM inventory")
    return dict(cursor.fetchall())
```

## 🐛 Solución de Problemas

### Error: "Servidor MCP remoto NO está disponible"

**Causa:** El servidor no está ejecutándose.

**Solución:**
```bash
python remote_mcp_server.py
```

### Error: "Connection refused on port 8000"

**Causa:** Otro proceso está usando el puerto 8000.

**Solución:**
```bash
# Encontrar el proceso
lsof -i :8000

# Matar el proceso
kill -9 <PID>

# O cambiar el puerto en remote_mcp_server.py
```

### Error: "ModuleNotFoundError: No module named 'mcp'"

**Causa:** Librerías no instaladas.

**Solución:**
```bash
pip install -r ../../../requirements.txt
```

### El servidor se ejecuta pero no responde

**Causa:** Firewall o configuración de red en Codespaces.

**Solución:**
- Verifica que el puerto 8000 esté visible en la pestaña PORTS
- Intenta cambiar `0.0.0.0` por `localhost` en el servidor

## 📚 Recursos Adicionales

- [Documentación de MCP](https://modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [GitHub Codespaces Docs](https://docs.github.com/en/codespaces)

## 🎯 Próximos Pasos

1. **Dockerizar el servidor**: Crear un `Dockerfile` para despliegue en contenedores
2. **CI/CD**: Automatizar el despliegue en Azure Container Instances
3. **Monitoring**: Agregar Prometheus/Grafana para métricas
4. **Seguridad**: Implementar autenticación OAuth2
5. **Persistencia**: Migrar de datos estáticos a PostgreSQL/MongoDB

## 📝 Notas

- Este módulo está optimizado para **GitHub Codespaces** pero funciona en cualquier entorno con Python 3.8+
- El servidor usa **SSE (Server-Sent Events)** sobre HTTP para comunicación bidireccional
- Para producción, considera usar **HTTPS** y **autenticación**
- El servidor puede manejar **múltiples clientes concurrentes**

---

¿Preguntas o problemas? Revisa la sección de [Solución de Problemas](#-solución-de-problemas) o consulta la documentación oficial de MCP.
