import os
import sys
from setuptools import setup, find_packages


readme_file = os.path.abspath(os.path.join(os.path.dirname(__file__),
    'README.md'))

try:
    long_description = open(readme_file).read()
except IOError as err:
    sys.stderr.write("[ERROR] Cannot find file specified as "
        "long_description (%s)\n" % readme_file)
    sys.exit(1)

frogress = __import__('frogress')

setup(
    name='frogress',
    version=frogress.get_version(),
    url='https://github.com/lukaszb/frogress',
    author='Lukasz Balcerzak',
    author_email='lukaszbalcerzak@gmail.com',
    description="A progress tool for humans",
    long_description=long_description,
    long_description_content_type='text/markdown',
    zip_safe=False,
    packages=find_packages(),
    license='MIT',
    scripts=[],
    test_suite='frogress.tests.collector',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)

