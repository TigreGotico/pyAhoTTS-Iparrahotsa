from setuptools import setup, find_packages
import os

BASE = os.path.dirname(__file__)
PKG = "pyahotts_iparrahotsa"


def get_version():
    """ Find the package version """
    version_file = os.path.join(BASE, PKG, 'version.py')
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if 'VERSION_MAJOR' in line:
                major = line.split('=')[1].strip()
            elif 'VERSION_MINOR' in line:
                minor = line.split('=')[1].strip()
            elif 'VERSION_BUILD' in line:
                build = line.split('=')[1].strip()
            elif 'VERSION_ALPHA' in line:
                alpha = line.split('=')[1].strip()

            if ((major and minor and build and alpha) or
                    '# END_VERSION_BLOCK' in line):
                break
    version = f"{major}.{minor}.{build}"
    if int(alpha):
        version += f"a{alpha}"
    return version


def get_package_data():
    """Collect all necessary package data files (voices, dicts, .so)."""
    data_files = []
    for root, dirs, files in os.walk(os.path.join(BASE, PKG)):
        for file in files:
            data_files.append(os.path.relpath(os.path.join(root, file), PKG))
    return data_files


setup(
    name='pyahotts_iparrahotsa',
    version=get_version(),
    description='AhoTTS_Iparrahotsa (Northern Basque dialect) - python Text-to-Speech package',
    author='JarbasAI',
    author_email='jarbasai@mailfence.com',
    url='https://github.com/TigreGotico/pyAhoTTS-Iparrahotsa',
    packages=find_packages(include=[PKG, f'{PKG}.*']),
    package_data={
        PKG: get_package_data(),
    },
    install_requires=[
        'numpy'
    ],
    extras_require={
        'test': ['pytest'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6'
)
