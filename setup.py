from setuptools import setup, find_packages

setup(
    name='backwards_beats_services',  # or any project-wide name
    version='0.1.2',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'requests',
        'python-dotenv',
        'openai-whisper',
        'numpy>=1.21.6,<1.28.0',
        'pydub'
    ],
    author='Dan Woodard',
    description='Shared services for podcast automation, including Spotify, Podbean, Last.FM, and secret management.',
)

