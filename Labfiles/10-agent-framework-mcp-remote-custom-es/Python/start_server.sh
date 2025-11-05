#!/bin/bash

# Script de inicio para el servidor MCP remoto
# Uso: ./start_server.sh [puerto]

set -e

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Puerto por defecto
PORT=${1:-8000}

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Servidor MCP Remoto - Gestión de Inventario Aeronáutico${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Verificar que Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python 3 no está instalado${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python 3 encontrado: $(python3 --version)"

# Verificar que el servidor existe
if [ ! -f "remote_mcp_server.py" ]; then
    echo -e "${RED}❌ Error: No se encontró remote_mcp_server.py${NC}"
    echo -e "${YELLOW}   Asegúrate de ejecutar este script desde el directorio Python/${NC}"
    exit 1
fi

# Verificar si el puerto está en uso
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠️  Advertencia: El puerto $PORT ya está en uso${NC}"
    echo -e "${YELLOW}   Deteniendo proceso existente...${NC}"
    lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Instalar dependencias si es necesario
echo ""
echo -e "${BLUE}📦 Verificando dependencias...${NC}"
pip3 install -q mcp uvicorn starlette 2>/dev/null || {
    echo -e "${YELLOW}⚠️  Instalando dependencias faltantes...${NC}"
    pip3 install mcp uvicorn starlette
}

echo -e "${GREEN}✓${NC} Dependencias verificadas"
echo ""

# Iniciar el servidor
echo -e "${GREEN}🚀 Iniciando servidor MCP remoto...${NC}"
echo ""
echo -e "${BLUE}   URL del servidor:${NC} http://localhost:$PORT"
echo -e "${BLUE}   Endpoint SSE:${NC}     http://localhost:$PORT/sse"
echo ""
echo -e "${YELLOW}   Presiona Ctrl+C para detener el servidor${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Ejecutar el servidor
exec python3 remote_mcp_server.py
