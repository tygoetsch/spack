# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgnewscale(RPackage):
    """Multiple Fill and Colour Scales in 'ggplot2'.

    Use multiple fill and colour scales in 'ggplot2'."""

    cran = "ggnewscale"

    version("0.4.8", sha256="c7fefa6941ecbc789507e59be13fa96327fe2549681a938c43beb06ca22a9700")

    depends_on("r-ggplot2@3.0.0:", type=("build", "run"))
