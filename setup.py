# coding=utf-8
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
    long_description="This is a library which can be used for ListServs which need to be "
                     "DMARC compliant, and can help build DMARC-compliant messages with origin "
                     "points of the ListServ itself from original messages "
                     "that a ListServ would receive.",
    license='AGPLv3+',
    url='https://gitlab.com/teward/dmarcmsg',
    download_url='https://pypi.python.org/pypi/dmarcmsg',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='email dmarc listserv',
    python_requires='>=3.5',
    platforms='any',
    test_suite='tests',
)
