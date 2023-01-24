# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMlbench(RPackage):
    """Machine Learning Benchmark Problems.

    A collection of artificial and real-world machine learning benchmark
    problems, including, e.g., several data sets from the UCI repository."""

    cran = "mlbench"

    version("2.1-3", sha256="b1f92be633243185ab86e880a1e1ac5a4dd3c535d01ebd187a4872d0a8c6f194")
    version("2.1-1", sha256="748141d56531a39dc4d37cf0a5165a40b653a04c507e916854053ed77119e0e6")

    depends_on("r@2.10:", type=("build", "run"))
