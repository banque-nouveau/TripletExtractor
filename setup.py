import os
import re
from setuptools import setup


PACKAGENAME = 'trextractor'
packageDir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          PACKAGENAME)

# Obtain the package version
versionFile = os.path.join(packageDir, 'version.py')
with open(versionFile, 'r') as f:
          s = f.read()
# Look up the string value assigned to __version__ in version.py using regexp
versionRegExp = re.compile("__VERSION__ = \"(.*?)\"")
# Assign to __version__
__version__ =  versionRegExp.findall(s)[0]
print(__version__)

# create requirements file
setupDir = os.path.join(packageDir, '..', 'setup')
genRequirements = os.path.join(setupDir, 'generate_requirements.py')
print(genRequirements)


setup(
      name=PACKAGENAME,
      version=__version__,
      description='a package to perform triplet extraction',
      long_description=''' ''',
      # What code to include as packages
      packages=[PACKAGENAME],
      # What data to include as packages
      package_data=dict(textractor=['prompts/blackrock_prompt.txt']),
      include_package_data=True,
     )
