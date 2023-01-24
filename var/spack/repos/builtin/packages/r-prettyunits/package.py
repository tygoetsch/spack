# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPrettyunits(RPackage):
    """Pretty, Human Readable Formatting of Quantities.

    Pretty, human readable formatting of quantities. Time intervals: 1337000 ->
    15d 11h 23m 20s. Vague time intervals: 2674000 -> about a month ago. Bytes:
    1337 -> 1.34 kB."""

    cran = "prettyunits"

    version("1.1.1", sha256="9a199aa80c6d5e50fa977bc724d6e39dae1fc597a96413053609156ee7fb75c5")
    version("1.0.2", sha256="35a4980586c20650538ae1e4fed4d80fdde3f212b98546fc3c7d9469a1207f5c")

    depends_on("r-magrittr", type=("build", "run"), when="@:1.0.2")
    depends_on("r-assertthat", type=("build", "run"), when="@:1.0.2")
