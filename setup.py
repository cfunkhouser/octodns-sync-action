import setuptools

__version__ = '0.0.1'

setuptools.setup(
    name='sync_action',
    version=__version__,
    author='Christian Funkhouser',
    author_email='christian@funkhouse.rs',
    description='OctoDNS Sync Action for GitHub',
    url='https://github.com/cfunkhouser/octodns-sync-action',
    project_urls={
        'Bug Tracker':
            'https://github.com/cfunkhouser/octodns-sync-action/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
