from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='check-the-possibilities',
    version='0.0.16',
    author='alexander_petrenko',
    author_email='gd@reseco.ru',
    description='PPL - Python Prototype Library',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/AlexanderPetrenko83/prototype_python_library.git',
    packages=find_packages(),
    install_requires=[
         'pandas>=2.2.0'
    ],
    python_requires='>=3.12'
)
