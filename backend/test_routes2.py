import sys
sys.path.insert(0, r'C:\Users\santi\Documents\GitHub\PetCare\backend')
from app.main import app
print('All routes:')
for route in app.routes:
    path = getattr(route, 'path', '?')
    methods = getattr(route, 'methods', '?')
    print(f'  {path} - {methods}')