import setuptools

__version__ = '0.0.8'

setuptools.setup(
    name='octodns-sync-action',
    version=__version__,
    author='Christian Funkhouser',
    author_email='christian@funkhouse.rs',
    description='OctoDNS Sync Action for GitHub',
    url='https://github.com/cfunkhouser/octodns-sync-action',
    packages=['octosync'],
    project_urls={
        'Bug Tracker':
            'https://github.com/cfunkhouser/octodns-sync-action/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'octodns~=0.9',
        'fire~=0.4',
    ],
)
