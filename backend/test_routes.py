import sys
sys.path.insert(0, '.')
from app.main import app

print("=== ROUTES ===")
for route in app.routes:
    if hasattr(route, 'path'):
        methods = getattr(route, 'methods', 'N/A')
        print(f"{route.path:30} {methods}")

print("\n=== MIDDLEWARE ===")
for mw in app.user_middleware:
    print(f"{mw.cls.__name__}")
