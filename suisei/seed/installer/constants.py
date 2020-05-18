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
Contains common constants used by the SEED installer utility.
"""

# Path to the default directory containing the configuration of the utility.
DEFAULT_CONFIG_DIRECTORY = '.'

# Path to the directory where application data used by the utility is stored.
DEFAULT_DATA_DIRECTORY = './data'

# Path to the directory where the utility will store its log files.
DEFAULT_LOG_DIRECTORY = '/var/logs'

# The description string to use in the CLI help.
CLI_DESCRIPTION_STRING = \
    'SEED installer utility. It manages the transformation of a regular Unix'\
    'system to a SEED node.'

# The usage string to use in the CLI help.
CLI_USAGE_STRING = \
    'seed.installer [-h|--help] [--debug] [-c|--config-directory] '\
    '[-l|--log-directory] [--key]'

# The epilogue string to use in the CLI help.
CLI_EPILOGUE_STRING = ''

# The CLI commands used by the application
CLI_COMMAND_MAP = \
[
    {
        'type': 'group',
        'name': 'Configuration',
        'description': 'Contains options to customize the configuration of the SEED installer.',
        'commands':
        [
            {
                'type': 'config',
                'shortkey': '-c',
                'command': '--config-directory',
                'help': 'Allows the specification of a custom configuration directory.',
                'metavar': 'PATH'
            },
            {
                'type': 'config',
                'shortkey': '',
                'command': '--data-directory',
                'help': 'Allows the specification of a custom data directory.',
                'metavar': 'PATH'
            },
            {
                'type': 'config',
                'shortkey': '-l',
                'command': '--log-directory',
                'help': 'Allows the specification of a custom log directory.',
                'metavar': 'PATH'
            },
            {
                'type': 'config',
                'shortkey': '',
                'command': '--key',
                'help': 'Allows the specification of the decryption key to use when loading the configuration',
                'metavar': 'KEY'
            }
        ]
    },
    {
        'type': 'group',
        'name': 'Miscellaneous Options',
        'description': 'Contains miscellaneous options for the SEED installer utility.',
        'commands':
        [
            {
                'type': 'switch',
                'shortkey': '-d',
                'command': '--debug',
                'help': 'Starts the daemon in debug mode.',
                'default': 'False'
            }
        ]
    }
]