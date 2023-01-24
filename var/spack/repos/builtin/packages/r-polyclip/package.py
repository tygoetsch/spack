# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPolyclip(RPackage):
    """Polygon Clipping.

    R port of Angus Johnson's open source library Clipper. Performs polygon
    clipping operations (intersection, union, set minus, set difference) for
    polygonal regions of arbitrary complexity, including holes. Computes offset
    polygons (spatial buffer zones, morphological dilations, Minkowski
    dilations) for polygonal regions and polygonal lines. Computes Minkowski
    Sum of general polygons. There is a function for removing
    self-intersections from polygon data."""

    cran = "polyclip"

    version("1.10-4", sha256="84d2c9778771d3759b49d7d16fb54c8ddc5397da3b1d21074bc4aa42c02e6f56")
    version("1.10-0", sha256="74dabc0dfe5a527114f0bb8f3d22f5d1ae694e6ea9345912909bae885525d34b")

    depends_on("r@3.0.0:", type=("build", "run"))
