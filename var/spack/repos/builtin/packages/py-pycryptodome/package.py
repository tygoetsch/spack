# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPycryptodome(PythonPackage):
    """Cryptographic library for Python"""

    homepage = "https://www.pycryptodome.org"
    pypi = "pycryptodome/pycryptodome-3.16.0.tar.gz"

    version("3.16.0", sha256="0e45d2d852a66ecfb904f090c3f87dc0dfb89a499570abad8590f10d9cffb350")

    depends_on("py-setuptools", type="build")
