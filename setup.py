from setuptools import setup

with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name='pokercore',
    version='0.1.4',
    description='A poker engine core, in Python',
    long_description=long_description,
    author='Aristotelis Mikropoulos',
    author_email='amikrop@gmail.com',
    url='https://github.com/amikrop/pokercore',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Games/Entertainment',
    ],
    packages=['pokercore', 'pokercore.test'],
    package_data={'pokercore.test': ['testcases']},
)
