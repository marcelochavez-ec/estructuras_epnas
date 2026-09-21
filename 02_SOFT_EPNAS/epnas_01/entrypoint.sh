#!/bin/sh
set -e

# ============================================================
# EPNAS - Inicialización del contenedor Django
# ============================================================

export PYTHONPATH=/app:${PYTHONPATH}

echo "=============================================="
echo "EPNAS - Inicializando aplicación"
echo "=============================================="

echo "1. Verificando schema epnas..."
python scripts/init_db.py

echo "2. Ejecutando migraciones..."
python manage.py migrate --noinput

echo "3. Cargando catálogo S03..."
python manage.py cargar_catalogo_s03

echo "4. Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "5. Iniciando Gunicorn..."
exec gunicorn epnas_01.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --threads 2 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -