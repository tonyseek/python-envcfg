from setuptools import setup, find_packages


with open('README.rst') as readme:
    next(readme)  # skip the first line
    long_description = ''.join(readme).strip()


setup(
    name='python-envcfg',
    version='0.2.0',
    author='Jiangge Zhang',
    author_email='tonyseek@gmail.com',
    description='Accessing environment variables with a magic module.',
    long_description=long_description,
    platforms=['Any'],
    url='https://github.com/tonyseek/python-envcfg',
    license='MIT',
    packages=find_packages(),
    keywords=['env', 'config', '12-factor'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries',
    ]
)
