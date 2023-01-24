# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RktTestingUtilLib(RacketPackage):
    """Utilities for interoperating between different testing libraries."""

    git = "ssh://git@github.com/racket/rackunit.git"

    maintainers = ["elfprince13"]

    version("8.3", commit="683237bee2a979c7b1541092922fb51a75ea8ca9")  # tag='v8.3'
    depends_on("rkt-base@8.3:", type=("build", "run"), when="@8.3")

    racket_name = "testing-util-lib"
    subdirectory = racket_name
