#!/usr/bin/env python3.6
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

    import django
    from django.core.management import execute_from_command_line

    django.setup()
    execute_from_command_line(sys.argv)
