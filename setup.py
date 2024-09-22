from setuptools import setup, find_packages

setup(
    name='music_services',
    version='0.1',
    packages=find_packages(),
    install_requires=['requests, python-dotenv'],
    author='Dan Woodard',
    description='A package to interact with Spotify, Discogs, Last.FM and MusicBrainz APIs.',
)

