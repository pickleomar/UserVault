from waitress import serve
from app import create_app

app = create_app()

serve(
    app,
    host='0.0.0.0',
    port=8080,
    threads=8,
    connection_limit=100,  # Prevents DDoS
    cleanup_interval=30,    # Reclaims resources
    channel_timeout=60      # Kills stale connections
)