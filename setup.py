from setuptools import setup


VERSION = '0.12'


setup(
    name='wildfire',
    version=VERSION,
    description='A library for automatically generating HTTP services',
    url='https://github.com/floscha/floscha',
    author='Florian Schäfer',
    author_email='florian.joh.schaefer@gmail.com',
    license='Apache Software License',
    packages=['wildfire'],
    install_requires=[line for line
                      in open('requirements.txt', 'r').readlines() if line],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development'
    ]
)
