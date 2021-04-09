import setuptools

__version__ = '0.0.15'

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
        'octodns @ https://github.com/octodns/octodns/archive/8668dd3e8b34b0032b0cbb6fa157ed7b182a3ee2.tar.gz#egg=octodns',  # noqa: E501
        'fire~=0.4',
    ],
)
