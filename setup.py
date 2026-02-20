from setuptools import setup, find_packages

setup(
    name='backwards_beats_services',  # or any project-wide name
    version='0.1',
    packages=find_packages(
        include=[
            'ai_services',
            'ai_services.*',
            'music_services',
            'music_services.*',
            'podbean_services',
            'podbean_services.*',
            'secret_management',
            'secret_management.*',
            'shared_services',
            'shared_services.*',
        ]
    ),
    install_requires=[
        'requests',
        'python-dotenv',
        'openai-whisper',
        'pydub'
    ],
    author='Dan Woodard',
    description='Shared services for podcast automation, including Spotify, Podbean, Last.FM, and secret management.',
)

