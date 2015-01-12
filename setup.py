from setuptools import setup

with open('README') as readme:
    long_description = readme.read()

setup(
    name='pokercore',
    version='0.1.3',
    description='A poker engine core, in Python',
    long_description=long_description,
    author='Aristotelis Mikropoulos',
    author_email='amikrop@gmail.com',
    url='https://pypi.python.org/pypi/pokercore',
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
