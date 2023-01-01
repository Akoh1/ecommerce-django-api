#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from decouple import config


def main():
    """Run administrative tasks."""
    # print(f"sys argvs: {sys.argv}")
    # if str(sys.argv[-1] == '--dev'):
    ENVIRONMENT = os.environ.get("ENV")
    if ENVIRONMENT == "dev":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings.dev')
    elif ENVIRONMENT == "prod":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings.prod')
    else:
        print("-> Missing ENV variable (dev | prod)")
        sys.exit(1)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
