#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2016-       Martin Sinn                         m.sinn@gmx.de
#########################################################################
#  This file is part of SmartHomeNG
#  https://github.com/smarthomeNG/smarthome
#  http://knx-user-forum.de/
#
#  SmartHomeNG is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHomeNG is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHomeNG. If not, see <http://www.gnu.org/licenses/>.
#########################################################################

import os

print('')
print(os.path.basename(__file__) + ' - tool to convert shng .conf files to yaml')
print('')

import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '../lib')
import item_conversion


# ==================================================================================
#   Convert all .conf files in a directory
#

def convert_directory(dir):

    for item_file in sorted(os.listdir(dir)):
        if item_file.endswith('.conf'):
            # Remove path and extension
            item_file = os.path.basename(item_file)
            item_file = os.path.splitext(item_file)[0]
            configurationfile = dir+'/'+item_file

            ydata = item_conversion.parse_for_convert(configurationfile+'.conf')
            try:
                if ydata != None:
                    item_conversion.yaml_save(configurationfile, ydata)
            except Exception as e:
                print()
                print("ERROR: Problem reading {0}: {1}".format(dir+'/'+configurationfile, e))


# ==================================================================================
#   Main Converter Routine
#

if __name__ == '__main__':

    # change the working diractory to the directory from which the converter is loaded (../tools)
    os.chdir(os.path.dirname(os.path.abspath(os.path.basename(__file__))))
    
    directory = os.path.abspath('../items')
    etc_dir = os.path.abspath('../etc')
    
    if item_conversion.is_ruamelyaml_installed() == False:
        exit(1)
        
    print('converting .conf-files from the following directories:')
    print('- item-directory  : ' + directory)
    print('- config-directory: ' + etc_dir)
    print('')
    
    ans_item = input('Convert item files (y/n)?: ').upper()
    ans_etc  = input('Convert config files (y/n)?: ').upper()
    print()
    
    if ans_item == 'Y':
        print('Converting item files:')
        convert_directory(directory)
        print('')

    if ans_etc == 'Y':
        print('Convering configuration files:')
        convert_directory(etc_dir)
        print('')

    if ans_item == 'Y' or ans_etc == 'Y':
        print('Conversion finished!')
        print()
        
    if ans_item == 'Y':
        print('You MUST move the old item.conf files out of the directory,')
        print('since SmartHomeNG tries to read all .yaml AND all .conf files')
        print('stored in the item directory.')
        print()

    if ans_etc == 'Y':
        print('You should move the old .conf files out of the etc directory to avoid')
        print('confusion. If both files (.conf and .yaml) exist, SmartHomeNG only reads')
        print('the .yaml file.')
        print()
