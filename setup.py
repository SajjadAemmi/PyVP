from pathlib import Path
from setuptools import setup, find_packages


def post_install():
    """ Implement post installation routine """
    with open('./requirements.txt') as f:
        install_requires = f.read().splitlines()

    return install_requires


def pre_install():
    """ Implement pre installation routine """
    # read the contents of your README file
    global long_description
    this_directory = Path(__file__).parent
    long_description = (this_directory / "README.md").read_text()


pre_install()


setup(
    name='pyvp',
    version='0.1.1',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["pyvp"],
    setup_requires=[
        'scikit-image',
        'numpy',
        'matplotlib'
    ],
    url='https://github.com/SajjadAemmi/PyVP',
    license='',
    author='Sajjad Aemmi',
    author_email='sajjadaemmi@gmail.com',
    description='Vanishing Point Detector',
    include_package_data=True,
    package_data={"pyvp": ['main.ui']},
    install_requires=post_install(),
    entry_points={
        "console_scripts": [],
    },
)