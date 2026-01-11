# ChequePass — Gunicorn Configuration

import os

# Bind to Render / Fly.io port
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

# Workers & threads
workers = 2
threads = 4

# Worker type
worker_class = "gthread"

# Timeout for M-Pesa callbacks and QR scans
timeout = 120

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Security
limit_request_line = 8190
limit_request_fields = 100
limit_request_field_size = 8190

# Restart workers automatically
max_requests = 1000
max_requests_jitter = 100

# Preload app (faster cold starts)
preload_app = True
