#!/usr/bin/env python
import sys

from libs.common.utils import export_env_files

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    export_env_files(
        'configs/env/common.env',
        'configs/env/secret.env',
        'configs/env/dev.env',
    )
    execute_from_command_line(sys.argv)
