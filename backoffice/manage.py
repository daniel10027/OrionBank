import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backoffice.settings")
    try:
        from django.core.management import execute_from_command_line
    except Exception as exc:
        raise exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
