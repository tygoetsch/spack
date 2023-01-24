# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFastica(RPackage):
    """FastICA Algorithms to Perform ICA and Projection Pursuit.

    Implementation of FastICA algorithm to perform Independent Component
    Analysis (ICA) and Projection Pursuit."""

    cran = "fastICA"

    version("1.2-3", sha256="e9ef82644cb64bb49ae3b7b6e0885f4fb2dc08ae030f8c76fe8dd8507b658950")
    version("1.2-2", sha256="32223593374102bf54c8fdca7b57231e4f4d0dd0be02d9f3500ad41b1996f1fe")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@1.2-3:")
