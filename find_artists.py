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

from artist_finder import artist_finder as af
from export_file import export_file
from import_file import import_file

in_filepath = input("Input Filepath:")
print(in_filepath)

in_filename = input("Input Filename (required):")
print(in_filename)

out_filename = input("Output Filename:")
print(out_filename)

out_filepath = input("Output Filepath:")
print(out_filepath)

print('Importing File')
importing = import_file(in_filename, in_filepath)
imported = importing.read()

print('Finding Artists')
af = af(imported)
artist_data = af.find_artists()

print('Exporting File')
export_file = export_file(artist_data)
export_file()