# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySchema(PythonPackage):
    """Simple data validation library"""

    homepage = "https://github.com/keleshev/schema"
    pypi = "schema/schema-0.7.5.tar.gz"

    version("0.7.5", sha256="f06717112c61895cabc4707752b88716e8420a8819d71404501e114f91043197")

    depends_on("py-setuptools", type="build")
    depends_on("py-contextlib2@0.5.5:", type=("build", "run"))
