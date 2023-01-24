# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTester(RPackage):
    """Tests and checks characteristics of R objects.

    tester allows you to test characteristics of common R objects."""

    cran = "tester"

    version("0.1.7", sha256="b9c645119c21c69450f3d366c911ed92ac7c14ef61652fd676a38fb9d420b5f4")

    depends_on("r@3.0:", type=("build", "run"))
