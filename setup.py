import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'Pillow',
    'SQLAlchemy',
    'WebTest',
    'enum',
#    'jsonschema',
#    'loremipsum',
    'pyramid',
    'pyramid_multiauth',
    'pyramid_tm',
    'setuptools',
    'xlrd',
    'xlutils',
    'zope.sqlalchemy',
#    'PyBrowserID',
    'numpy',
 #   'scipy',
    'requests>=1.0',
]

tests_require = [
    'pytest',
]

setup(
    name='chumpblock',
    version='0.1',
    description='MTG Simulator',
    long_description=README + '\n\n' + CHANGES,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    author='Benjamin Hitz',
    author_email='hitz@stanford.edu',
    url='http://chumpblock.com',
    license='MIT',
    install_requires=requires,
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
    entry_points='''
        [console_scripts]
        extract_test_data = chumbblock.commands.extract_test_data:main

        [paste.app_factory]
        main = encoded:main
        ''',
)
