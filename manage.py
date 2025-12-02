#!/usr/bin/env python
"""
Точка входа для администрирования Django-проекта.
"""
import os
import sys


def main() -> None:
    """Запуск команд Django с предустановленными настройками."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
