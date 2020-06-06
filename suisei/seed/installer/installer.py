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
Contains the implementation of the SEED Installer's business logic.
"""

# Platform Imports
import os
import traceback

# Dependency Imports
import urwid
from termcolor import colored

# Murasame Imports
from murasame.application import (
    BusinessLogic,
    StartupConfiguration,
    CliApplication,
    ApplicationReturnCodes)
from murasame.exceptions import InvalidLicenseKeyError
from murasame.pal.host import HostDescriptor

# SEED Imports
from .constants import (
    DEFAULT_LOG_DIRECTORY,
    DEFAULT_WORKING_DIRECTORY,
    SEED_SENTRY_DSN,
    SEED_LICENSE_PUBLIC_KEY)

from .version import (
    SEED_INSTALLER_MAJOR_VERSION,
    SEED_INSTALLER_MINOR_VERSION,
    SEED_INSTALLER_PATCH_LEVEL,
    SEED_INSTALLER_BUILD)

class Installer(BusinessLogic):

    """
    Contains the top level business logic of the SEED installer.

    Authors:
        Attila Kovacs
    """

    def __init__(self) -> None:

        """
        Creates a new Installer instance.

        Authors:
            Attila Kovacs
        """

        self._main_loop = None
        """
        The urwid main loop object.
        """

        self._host = None
        """
        The host descriptor object.
        """

    @staticmethod
    def cb_process_command_line(arguments: 'argparse.Namespace') -> None:

        """
        Processing logic for command line arguments.

        Args:
            arguments:  Processed command line arguments.

        Authors:
            Attila Kovacs
        """

        # Process command line options
        log_directory = DEFAULT_LOG_DIRECTORY
        debug_mode = False
        license_path = None

        if arguments.log_directory is not None:
            log_directory = os.path.abspath(
                os.path.expanduser(arguments.log_directory))

        if arguments.debug:
            debug_mode = True

        if arguments.license_key is not None:
            license_path = os.path.abspath(
                os.path.expanduser(arguments.license_key))

        if not license_path:
            print('No license file provided.')
            license_path = 'test.lic'
            #raise InvalidLicenseKeyError(
            #    'A valid license key is required to install a SEED node.')

        # Configure working directory
        working_directory = os.path.abspath(
            os.path.expanduser(DEFAULT_WORKING_DIRECTORY))

        license_key = f'{working_directory}/license.pem'

        # Create startup configuration.
        startup_configuration = StartupConfiguration()
        startup_configuration.set_business_logic(Installer())
        startup_configuration.set_working_directory(
            working_directory=working_directory,
            force_create_working_directory=True)
        startup_configuration.set_log_directory(
            log_directory=DEFAULT_LOG_DIRECTORY,
            force_create_log_directory=True)
        startup_configuration.set_debug_mode(debug_mode=debug_mode)
        startup_configuration.set_license(
            #license_required=True,
            license_required=False,
            license_key=license_key,
            license_path=license_path)
        startup_configuration.set_sentry_dsn(
            sentry_dsn=SEED_SENTRY_DSN)

        # Write the license key to disk
        Installer._write_license_key(license_key=license_key)

        # Create the application
        application = CliApplication(
            startup_configuration=startup_configuration)

        # Start execution
        application.execute(arguments=arguments)

    @staticmethod
    def cb_retrieve_license_key() -> str:

        """
        Callback function that is called to retrieve the decryption key of
        the license file.

        Returns:
            The key for the license file.

        Authors:
            Attila Kovacs
        """

        return None

    def main_loop(self, *args, **kwargs) -> ApplicationReturnCodes:

        """
        Contains the main loop (or the main business execution logic of
        the application.

        Args:
            args:       List of unnamed arguments.
            kwargs:     List of named arguments.

        Returns:
            The overall return code of the application.
            ApplicationReturnCodes.SUCCESS for successful execution, or an
            integer value to indicate issues.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del args
        del kwargs

        palette = \
        [
            ('banner', 'black', 'dark red'),
            ('streak', 'black', 'dark red'),
            ('bg', 'black', 'dark blue'),
            ('normal', 'black', 'dark blue')
        ]

        try:
            banner_text = urwid.Text(
                ('banner', f'SEED Installer ({SEED_INSTALLER_MAJOR_VERSION}.'
                           f'{SEED_INSTALLER_MINOR_VERSION}.'
                           f'{SEED_INSTALLER_PATCH_LEVEL} '
                           f'Build: {SEED_INSTALLER_BUILD})'),
                align='center')
            banner = urwid.AttrWrap(banner_text, 'streak')

            intro_text = urwid.Text(
                ('normal', 'This utility will transform your Linux system to '
                           'a SEED node.'))

            press_key_text = urwid.Text(
                ('normal', 'Press Q to quit, or any other key to continue...'),
                align='right')

            host_info = urwid.Text(
                ('normal', f'CPU: {self._host.Hardware.CPU.Name}\n'
                           f'Memory: {int(self._host.Hardware.Memory.TotalSystemMemory/1024/1024)} MB\n'
                           f'Public IP: {self._host.Hardware.Networking.PublicIP}\n'
                           f'OS: {self._host.OS.Name}({self._host.OS.Version})\n'
                           f'Python version: {self._host.Python.PythonVersion}'))

            blank = urwid.Divider()

            content_list = \
            [
                blank,
                intro_text,
                blank,
                host_info
            ]

            content = urwid.ListBox(urwid.SimpleListWalker(content_list))

            frame = urwid.Frame(urwid.AttrWrap(content, 'bg'),
                                header=banner,
                                footer=press_key_text)

            self._main_loop = urwid.MainLoop(
                frame,
                palette,
                unhandled_input=Installer.show_on_exit)
            self._main_loop.run()
        except:
            traceback.print_exc()

        return ApplicationReturnCodes.SUCCESS

    @staticmethod
    def show_on_exit(key: str) -> None:

        """
        Key handler function for the main loop.

        Args:
            key:        The key that has been pressed.

        Authors:
            Attila Kovacs
        """

        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def before_main_loop(self, *args, **kwargs) -> None:

        """
        Function that is called before the application enters its main loop.

        Args:
            args:       List of unnamed arguments.
            kwargs:     List of named arguments.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del args
        del kwargs

        print('Detecting host system...', end=' ')
        self._host = HostDescriptor()
        print(colored('DONE', 'green'))

    def after_main_loop(self, *args, **kwargs) -> None:

        """
        Function that is called after the application exited the main loop in
        a normal way.

        Args:
            args:       List of unnamed arguments.
            kwargs:     List of named arguments.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del args
        del kwargs

    def initialize_services(self,
                            startup_configuration: 'StartupConfiguration') -> None:

        """
        Initializes the services used by the application. It is called by the
        application upon initialization.

        Args:
            startup_configuration:      The startup configuration of the
                                        application.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del startup_configuration

    def on_uncaught_exception(self, exception: Exception) -> None:

        """
        Handler function called when the application encounters an uncaught
        exception.

        Args:
            exception:      The exception that was not handled properly.

        Authors:
            Attila Kovacs
        """

        #pylint: disable=no-self-use

        del exception

    @staticmethod
    def _write_license_key(license_key: str) -> None:

        """
        Writes the RSA public key required to decrypt the license file.

        Args:
            license_key:    Path to the file where the RSA public key will be
                            saved.

        Authors:
            Attila Kovacs
        """

        with open(license_key, 'w') as license_file:
            license_file.write(SEED_LICENSE_PUBLIC_KEY)