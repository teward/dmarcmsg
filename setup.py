from setuptools import find_packages, setup
from dmarcmsg import __version__ as version

setup(
    name='dmarcmsg',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    author='Thomas Ward',
    author_email='teward@dark-net.io',
    description="DMARC-Compliant Message Constructor Library for List-Servs.",
    long_description="This is a library which can be used for ListServs which need to be DMARC compliant, and can help "
                     "build DMARC-compliant messages with origin points of the ListServ itself from original messages "
                     "that a ListServ would receive.",
    license='AGPLv3+',
    url='https://github.com/teward/dmarcmsg',
    download_url='https://pypi.python.org/pypi/dmarcmsg',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='email dmarc listserv',
    platforms='any'
)