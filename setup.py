# -*- python -*-
#
#       Copyright 2019 University of Delaware - CIRAD - INRAE
#
#       File author(s):
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
# ==============================================================================
"""
"""
# ==============================================================================
from setuptools import setup, find_packages
# ==============================================================================


setup(
    name="braceroot",
    version="0.0.1",
    description="Brace Root Mechanical Stability",
    long_description="",

    author="* Erin Sparks\n"
           "* Christophe Pradal\n"
           "* & collaborators\n",

    author_email="",
    maintainer="",
    maintainer_email="",

    url="https://github.com/pradal/braceroot",
    keywords='',

    # package installation
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,

    # See MANIFEST.in
    include_package_data=True,
    )

