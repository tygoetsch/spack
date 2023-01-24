# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLeaps(RPackage):
    """Regression Subset Selection.

    Regression subset selection, including exhaustive search."""

    cran = "leaps"

    version("3.1", sha256="3d7c3a102ce68433ecf167ece96a7ebb4207729e4defd0ac8fc00e7003f5c3b6")
    version("3.0", sha256="55a879cdad5a4c9bc3b5697dd4d364b3a094a49d8facb6692f5ce6af82adf285")
