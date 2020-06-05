## ============================================================================
##                   **** SEED Virtual Reality Platform ****
##                Copyright (C) 2019-2020, Suisei Entertainment
## ============================================================================
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
## ============================================================================

"""
Contains the entry point of the SEED installer utility.
"""

# Platform Imports
import os

# Dependency Imports
from termcolor import colored

# Murasame Imports
try:
    from murasame.utils import CliProcessor
    from murasame.exceptions import InvalidLicenseKeyError
except ImportError:
    print(colored(
        '<ERROR> - The SEED installer requires the Murasame framework to run.',
        'red'))
    raise SystemExit

# SEED Imports
from suisei.seed.installer.installer import Installer

from suisei.seed.installer.constants import (
    CLI_COMMAND_MAP,
    CLI_DESCRIPTION_STRING,
    CLI_EPILOGUE_STRING,
    CLI_USAGE_STRING)

def main() -> None:

    """
    The entry point of the SEED installer utility.
    """

    # Only start the installer if it's executed with root privileges.
    if os.geteuid() != 0:
        print(colored(
            '<ERROR> - The SEED installer has to be exeuted with root '
            'privileges.',
            'red'))
        raise SystemExit

    # Create CLI processor
    cli_processor = CliProcessor(
        command_map=CLI_COMMAND_MAP,
        description_string=CLI_DESCRIPTION_STRING,
        usage_string=CLI_USAGE_STRING,
        epilog_string=CLI_EPILOGUE_STRING)

    # Process command line and start the application.
    try:
        cli_processor.process(
            args=sys.argv[1:],
            cb_argument_processor=Installer.cb_process_command_line)
    except InvalidLicenseKeyError:
        print(colored(
            '<ERROR> - A valid license file is required to run the SEED '
            'installer.',
            'red'))
        raise SystemExit

if __name__ == '__main__':
    main()