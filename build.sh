#!/usr/bin/python3

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
Build script for the SEED installer utility.
"""

# Platform Imports
import logging
import json
import subprocess

from string import Template

# Dependency Imports
import coloredlogs

## ============================================================================
##      >>> GENERATOR INPUT DATA <<<
## ============================================================================

VERSION_CONSTANTS_FILE = \
'## ============================================================================\n'\
'##                   **** SEED Virtual Reality Platform ****\n'\
'##                Copyright (C) 2019-2020, Suisei Entertainment\n'\
'## ============================================================================\n'\
'##\n'\
'##  This program is free software: you can redistribute it and/or modify\n'\
'##  it under the terms of the GNU General Public License as published by\n'\
'##  the Free Software Foundation, either version 3 of the License, or\n'\
'##  (at your option) any later version.\n'\
'##\n'\
'##  This program is distributed in the hope that it will be useful,\n'\
'##  but WITHOUT ANY WARRANTY; without even the implied warranty of\n'\
'##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n'\
'##  GNU General Public License for more details.\n'\
'##\n'\
'##  You should have received a copy of the GNU General Public License\n'\
'##  along with this program.  If not, see <http://www.gnu.org/licenses/>.\n'\
'##\n'\
'## ============================================================================\n'\
'\n'\
'\"\"\"\n'\
'Contains the version data of the package.\n'\
'\"\"\"\n'\
'\n'\
'## ============================================================================\n'\
'##     THIS IS A GENERATED FILE. DO NOT MODIFY IT MANUALLY.\n'\
'## ============================================================================\n'\
'\n'\
'SEED_INSTALLER_MAJOR_VERSION = ${major_version}\n'\
'SEED_INSTALLER_MINOR_VERSION = ${minor_version}\n'\
'SEED_INSTALLER_PATCH_LEVEL = ${patch_level}\n'\
'SEED_INSTALLER_BUILD = ${build_num}\n'\
'SEED_INSTALLER_RELEASE_LEVEL = \'${release_level}\'\n'\
'SEED_INSTALLER_RELEASE_CODENAME = \'${release_codename}\'\n'\
'SEED_INSTALLER_SCM_ID = \'${scm_id}\'\n'

## ============================================================================
##      >>> BUILD LOGIC <<<
## ============================================================================

def bump_version_number() -> None:

    """
    Loads the version configuration file, increases the build number and saves
    it to be used by the rest of the build script.

    Authors:
        Attila Kovacs
    """

    logger = logging.getLogger('suisei.seed.installer.builder')
    logger.debug('[STEP #1] Increase build number in version.conf...')

    version_data = None

    # Open configuration file
    try:
        with open('./version.conf', 'r') as config_file:
            version_data = json.load(config_file)
    except OSError:
        logger.error('[STEP #1]     - Failed to read the contents of version.conf.')
        raise SystemExit
    except json.JSONDecodeError:
        logger.error('[STEP #1]     - Failed to parse the content of version.conf.')
        raise SystemExit

    # Bump the build number
    build_num = int(version_data['meta']['build'])
    build_num = build_num + 1
    version_data['meta']['build'] = str(build_num)
    logger.debug(f'[STEP #1]    - New build number is {build_num}.')

    # Save the version configuration
    try:
        with open('./version.conf', 'w+') as config_file:
            json.dump(version_data,
                      config_file,
                      indent=4,
                      separators=(',', ': '))
    except OSError:
        logger.error('[STEP #1]     - Failed to update version.conf.')
        raise SystemExit

    logger.debug('[STEP #1] Build number has been updated.')

def create_constants_file() -> None:

    """
    Creates the version constants file to be included in the installer.

    Authors:
        Attila Kovacs
    """

    logger = logging.getLogger('suisei.seed.installer.builder')
    logger.debug('[STEP #2] Creating version constants file...')

    # Retrieving version data
    version_data = None
    major_version = None
    minor_version = None
    patch_level = None
    build_num = None
    release_level = None
    release_codename = None
    scm_id = None

    # Open configuration file
    try:
        with open('./version.conf', 'r') as config_file:
            version_data = json.load(config_file)
    except OSError:
        logger.error('[STEP #2]     - Failed to read the contents of version.conf.')
        raise SystemExit
    except json.JSONDecodeError:
        logger.error('[STEP #2]     - Failed to parse the content of version.conf.')
        raise SystemExit

    try:
        major_version = version_data['major']
        logger.debug(f'[STEP #2]     - Major version: {major_version}')
    except KeyError:
        logger.error('[STEP #2]     - No major version was found in version.conf')
        raise SystemExit

    try:
        minor_version = version_data['minor']
        logger.debug(f'[STEP #2]     - Minor version: {minor_version}')
    except KeyError:
        logger.error('[STEP #2]     - No minor version was found in version.conf')
        raise SystemExit

    try:
        patch_level = version_data['patch']
        logger.debug(f'[STEP #2]     - Patch level: {patch_level}')
    except KeyError:
        logger.error('[STEP #2]     - No patch level was found in version.conf')
        raise SystemExit

    try:
        build_num = version_data['meta']['build']
        logger.debug(f'[STEP #2]     - Build: {build_num}')
    except KeyError:
        logger.error('[STEP #2]     - No build number was found in version.conf')
        raise SystemExit

    try:
        release_level = version_data['release']
        logger.debug(f'[STEP #2]     - Release level: {release_level}')
    except KeyError:
        logger.error('[STEP #2]     - No release level was found in version.conf')
        raise SystemExit

    try:
        release_codename = version_data['meta']['codename']
        logger.debug(f'[STEP #2]     - Release codename: {release_codename}')
    except KeyError:
        logger.error('[STEP #2]     - No release codename was found in version.conf')
        raise SystemExit

    # Retrieving SCM version
    try:
        scm_id = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD']).strip().decode('ascii')
        logger.debug(f'[STEP #2]     - Git commit hash: {scm_id}')
    except subprocess.CalledProcessError:
        logger.error('Failed to determine the git commit hash.')
        raise SystemExit

    # Create file content
    template = Template(VERSION_CONSTANTS_FILE)
    version_content_string = template.safe_substitute(
        major_version=major_version,
        minor_version=minor_version,
        patch_level=patch_level,
        build_num=build_num,
        release_level=release_level,
        release_codename=release_codename,
        scm_id=scm_id)

    # Write the file
    with open('./suisei/seed/installer/version.py', 'w+') as version_file:
        version_file.write(version_content_string)

    logger.debug('[STEP #2] Version constants are added to the framework.')

def create_binary() -> None:

    """
    Creates the installer binary.

    Authors:
        Attila Kovacs
    """

    logger = logging.getLogger('suisei.seed.installer.builder')

    build_command = \
    [
        'pyinstaller',
        '--onefile',
        '--clean',
        '--noconfirm',
        '--name=seed.installer',
        './suisei/seed/installer/__main__.py'
    ]

    logger.debug('[STEP #3]     Running pyinstaller...')
    try:
        subprocess.check_call(build_command)
    except subprocess.CalledProcessError:
        logger.error('Failed to create binary.')
        raise SystemExit

    logger.debug('[STEP #3]     Binary created.')

def do_release() -> None:

    """
    Creates a realease from the current build on GitHub.

    Authors:
        Attila Kovacs
    """

    logger = logging.getLogger('suisei.seed.installer.builder')

def main() -> None:

    """
    The main build script logic.

    Authors:
        Attila Kovacs
    """

    # Initialize logging
    logger = logging.getLogger('suisei.seed.installer.builder')
    logger.setLevel(logging.DEBUG)
    coloredlogs.install(level='DEBUG')

    # Bump the version number
    bump_version_number()

    # Create constants file
    create_constants_file()

    # Create the binary
    create_binary()

    # Create a release
    do_release()

if __name__ == '__main__':
    main()