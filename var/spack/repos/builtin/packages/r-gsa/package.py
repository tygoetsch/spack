# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGsa(RPackage):
    """Gene Set Analysis."""

    cran = "GSA"

    version("1.03.2", sha256="177d6059fc645d3d8883806d2dea1c5dfc68efdada9aadde8a96b6d57acf35b8")
    version("1.03.1", sha256="e192d4383f53680dbd556223ea5f8cad6bae62a80a337ba5fd8d05a8aee6a917")
