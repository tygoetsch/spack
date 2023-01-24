# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMitools(RPackage):
    """Tools for Multiple Imputation of Missing Data.

    Tools to perform analyses and combine results from multiple-imputation
    datasets."""

    cran = "mitools"

    version("2.4", sha256="f204f3774e29d79810f579f128de892539518f2cbe6ed237e08c8e7283155d30")

    depends_on("r-dbi", type=("build", "run"))
