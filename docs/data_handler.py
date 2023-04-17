import file_management

#Input Data
read_file = file_management.ReadFile()
artist_names = read_file.read(sample=True, sample_size=100)

#Wiki IDs
artist_pages = []

#Output Data
data = []