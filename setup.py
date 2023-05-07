from setuptools import setup, find_packages

setup(
    name='FindArtists',
    version='1.0.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[

    ],
    entry_points={
        'console_scripts': [
            'find_artists = scripts.main:main'
        ]
    }
)

