from __future__ import absolute_import
from setuptools import setup, find_packages
import re
from io import open


# ------------------
def find_version():
    result = re.search(ur'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(u"__version__"), open(u'neurokit/__init__.py').read())
    return result.group(1)
# ------------------



# ------------------
setup(
name = u"neurokit",
description = (u"A Python Toolbox for Statistics and Signal Processing (EEG, EDA, ECG, EMG...)."),
version = find_version(),
license = u"MIT",
author = u"Dominique Makowski",
author_email = u"dom.makowski@gmail.com",
maintainer = u"Dominique Makowski",
maintainer_email = u"dom.makowski@gmail.com",
packages = find_packages(),
package_data = {
        u"neurokit.materials":[u"*.model"]},
install_requires = [
        u'numpy',
        u'pandas',
        u'scipy',
        u'sklearn',
        u'matplotlib',
        u'mne',
        u'bioread',
        u'nolds',
        u'biosppy',
        u'Pillow',
        u'cvxopt'],
dependency_links=[],
long_description = open(u'README.md').read(),
keywords = u"python signal processing EEG EDA ECG hrv rpeaks biosignals complexity",
url = u"https://github.com/neuropsychology/NeuroKit.py",
download_url = u'https://github.com/neuropsychology/NeuroKit.py/tarball/master',
test_suite=u"nose.collector",
tests_require=[
        u'pytest',
        u'nose',
        u'coverage'],
classifiers = [
        u'Intended Audience :: Science/Research',
        u'Intended Audience :: Developers',
        u'Programming Language :: Python',
        u'Topic :: Software Development',
        u'Topic :: Scientific/Engineering',
        u'Operating System :: Microsoft :: Windows',
        u'Operating System :: Unix',
        u'Operating System :: MacOS',
        u'Programming Language :: Python :: 2.7']
)
