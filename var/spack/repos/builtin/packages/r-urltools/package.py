# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RUrltools(RPackage):
    """Vectorised Tools for URL Handling and Parsing.

    A toolkit for all URL-handling needs, including encoding and decoding,
    parsing, parameter extraction and modification. All functions are designed
    to be both fast and entirely vectorised. It is intended to be useful for
    people dealing with web-related datasets, such as server-side logs,
    although may be useful for other situations involving large sets of
    URLs."""

    cran = "urltools"

    version("1.7.3", sha256="6020355c1b16a9e3956674e5dea9ac5c035c8eb3eb6bbdd841a2b5528cafa313")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-triebeard", type=("build", "run"))
