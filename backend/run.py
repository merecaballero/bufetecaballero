import sys
import socket
import uvicorn
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.app.config import settings

def is_port_in_use(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        try:
            s.bind((host, port))
            return False
        except OSError:
            return True

def find_available_port(host: str, start_port: int) -> int:
    port = start_port
    while is_port_in_use(host, port) and port < start_port + 50:
        port += 1
    return port

def main():
    host = settings.HOST
    port = settings.PORT
    
    if is_port_in_use(host, port):
        # Find next available port
        available_port = find_available_port(host, port)
        print(f"[*] El puerto {port} estaba ocupado o no disponible. Usando puerto alternativo: {available_port}")
        port = available_port

    print("=" * 68)
    print("  BUFETE CABALLERO -- DESPACHO DE ABOGADOS (ALICANTE, 1947)")
    print("  Servidor FastAPI + ASGI Uvicorn iniciado con exito")
    print("=" * 68)
    print(f"  Sitio Web Frontend:     http://{host}:{port}/")
    print(f"  Documentacion Swagger:  http://{host}:{port}/docs")
    print(f"  Panel Administrativo:   http://{host}:{port}/admin.html")
    print(f"  Health Check API:       http://{host}:{port}/api/v1/health")
    print("=" * 68)
    print("  Presiona CTRL+C para detener el servidor.\n")

    uvicorn.run(
        "backend.app.main:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
