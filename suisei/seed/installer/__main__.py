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

# Murasame Imports
from murasame.utils import CliProcessor

# SEED Imports
from .installer import Installer

from .constants import (
    CLI_COMMAND_MAP,
    CLI_DESCRIPTION_STRING,
    CLI_EPILOGUE_STRING,
    CLI_USAGE_STRING)

def main() -> None:

    """
    The entry point of the SEED installer utility.
    """

    cli_processor = CliProcessor(
        command_map=CLI_COMMAND_MAP,
        description_string=CLI_DESCRIPTION_STRING,
        usage_string=CLI_USAGE_STRING,
        epilog_string=CLI_EPILOGUE_STRING)

    cli_processor.process(
        args=sys.argv[1:],
        cb_argument_processor=Installer.cb_process_command_line)

if __name__ == '__main__':
    main()