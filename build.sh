#!/usr/bin/env bash
# build.sh

# Aplicar migraciones y recolectar archivos estáticos
python manage.py migrate
python manage.py collectstatic --noinput
