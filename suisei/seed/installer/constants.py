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

# Path to the directory where the utility will store its log files.
DEFAULT_LOG_DIRECTORY = '/var/logs/seed/'

# Path to the directory that the application will use as a working directory.
DEFAULT_WORKING_DIRECTORY = '/opt/seed/installer/'

# The Sentry DSN to use.
SEED_SENTRY_DSN = 'https://4b8f879e7c714743914c916a4d794a47@o376010.ingest.sentry.io/5196306'

# The public key required to validate license files.
SEED_LICENSE_PUBLIC_KEY = \
    '-----BEGIN PUBLIC KEY-----\n'\
    'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAuRzNWYzX+rYKn65s2Xz6\n'\
    'H1zZGxtZB8MpIcGZpjePLI1ivnXRylqp3wbw2J+BYpyWyIhtK22utrgDSzB99qHX\n'\
    'QyyuiYDO56ZcwZbaowJBkgBwQy2DyOIGItTulW6qupFiWPQ0/fhvmtMDXahbienY\n'\
    '/MEQLg9SN2zqSwmdEIxCR2LrzdH6EpflDEQ99WAPxUfGN/G4WrKGfQfHMysD5qfE\n'\
    'pDCrIg3VndcllqyK9Ots+84koFEAjQ63bJ/+Q6hZfQwupWq60WHxOSR52uwT0h0W\n'\
    'XWtTPru7uuCu7EVRwF0ZQIDflldBLcbkSXmEe61GRDF21+ungqXfTYdHfYNHgQqs\n'\
    '9qRdZqM6xQZMfTHvWzbdVDyk8qNk67eUeQLCLYFGhmGdGokckfayOu3Wr+OjiSCh\n'\
    'aHa4n2xCLMYIS15uZ4Fa3GT2ENUs0nHyFyI9Jmry82DmsoB2j+8zTmwRgGN8fNLD\n'\
    '2g7uKW8DADsgMKJr6wF4QhVFLiMBWdhdtPmqwzt+ZROl/KMtKaQf043CtyspSvPe\n'\
    'TJM+y5h71fJakUaBdq9DFu8jTk2TawEd6A0DxR2A4hezNeObSLUGw49k6Okjhiuq\n'\
    'Ruu1HkkFeXfE5JNhg7b/n1ZEh5DPpNE9hNlhUg7TjpHfjkGZJnwCBDxxEkvJE5mB\n'\
    'rtE9uLwlUmqNtgutNoQnpm0CAwEAAQ==\n'\
    '-----END PUBLIC KEY-----'

# The description string to use in the CLI help.
CLI_DESCRIPTION_STRING = \
    'SEED installer utility. It manages the transformation of a regular Unix'\
    'system to a SEED node.'

# The usage string to use in the CLI help.
CLI_USAGE_STRING = \
    'seed.installer [-h|--help] [-d|--debug] [-k|--license-key]'

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
                'shortkey': '-l',
                'command': '--log-directory',
                'help': 'Allows the specification of a custom log directory.',
                'metavar': 'PATH'
            },
            {
                'type': 'config',
                'shortkey': '-k',
                'command': '--license-key',
                'help': 'Allows the specification of the license key to be used.',
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