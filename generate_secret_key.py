#!/usr/bin/env python
"""
Script para generar una SECRET_KEY de Django
Uso: poetry run python generate_secret_key.py
"""
from django.core.management.utils import get_random_secret_key

if __name__ == "__main__":
    secret_key = get_random_secret_key()
    print("\n" + "=" * 60)
    print("SECRET_KEY generada:")
    print("=" * 60)
    print(secret_key)
    print("=" * 60)
    print("\nCopia este valor y úsalo en las variables de entorno de Vercel")
    print("como SECRET_KEY\n")

