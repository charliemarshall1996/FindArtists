# FindArtists - Python app to find information on artists and export to a spreadsheet
# Copyright (C) 2023 Charlie Marshall

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import file_management
import main


def get_user_input(prompt, default):
    user_input = input(f"{prompt} [{default}]: ")
    return user_input.strip() or default

input_filename = get_user_input("Enter input filename", "input.txt")
input_filepath = get_user_input("Enter input filepath", os.getcwd())
output_filename = get_user_input("Enter output filename", "output.txt")
output_filepath = get_user_input("Enter output filepath", os.getcwd())

# Set user inputs as values in file_management module
file_management.input_filename = input_filename
file_management.input_filepath = input_filepath
file_management.output_filename = output_filename
file_management.output_filepath = output_filepath

# Call main module
main.run()