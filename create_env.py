#!/usr/bin/env python
"""Script para crear el archivo .env con la configuración de ambiente."""

import os

def create_env_file(env_type="local"):
    """Crea un archivo .env con la configuración especificada."""
    content = f"""# Ambiente (local, testing, production)
ENV={env_type}

# WebSocket URLs (ya definidos en config.py, pero pueden sobrescribirse aquí)
# WS_URL_LOCAL=ws://127.0.0.1:8000/ws/quote
# WS_URL_TESTING=wss://rate-quote-assistant-backend.onrender.com/ws/quote
"""
    
    with open(".env", "w") as f:
        f.write(content)
    
    print(f"Archivo .env creado con ambiente {env_type}")

if __name__ == "__main__":
    import sys
    
    env_type = "local"
    if len(sys.argv) > 1:
        env_type = sys.argv[1]
    
    if env_type not in ["local", "testing", "production"]:
        print("Ambiente no válido. Usar: local, testing o production")
        sys.exit(1)
    
    create_env_file(env_type)
    print(f"Para cambiar el ambiente: python create_env.py [local|testing|production]") 