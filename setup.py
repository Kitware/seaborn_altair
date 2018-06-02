from distutils.core import setup

setup(
    name='seaborn_altair',
    version='0.1.0',
    description='Seaborn-compatible API for interactive Vega-Lite plots via Altair',
    author='Kitware, Inc.',
    author_email='kitware@kitware.com',
    license='BSD (3-clause)',
    url='https://github.com/Kitware/seaborn_altair',
    packages=['seaborn_altair'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    install_requires=[
        'altair',
        'seaborn'
    ]
)
