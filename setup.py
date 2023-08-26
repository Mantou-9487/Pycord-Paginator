from setuptools import find_packages, setup

setup(
    name='pycord-Paginator',
    version='1.0.0',
    url="https://github.com/Mantou-9487/Pycord-Paginator",
    author="Mantou-9487",
    license='MIT',
    packages=find_packages(),
    packages=['Paginator'],
    include_package_data=True,
    keywords=['Paginator', "pycord", "discord"],
    zip_safe=False,
    install_requires=[
        'disnake',
    ],
)