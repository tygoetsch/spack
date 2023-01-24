# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRle(RPackage):
    """Common Functions for Run-Length Encoded Vectors.

    Common 'base' and 'stats' methods for 'rle' objects, aiming to make it
    possible to treat them transparently as vectors."""

    cran = "rle"

    version("0.9.2", sha256="803cbe310af6e882e27be61d37d660dbe5910ac1ee1eff61a480bcf724a04f69")

    depends_on("r@3.5:", type=("build", "run"))
