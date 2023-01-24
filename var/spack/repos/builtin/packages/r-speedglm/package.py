# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpeedglm(RPackage):
    """Fitting Linear and Generalized Linear Models to Large Data Sets.

    Fitting linear models and generalized linear models to large data sets by
    updating algorithms."""

    cran = "speedglm"

    version("0.3-4", sha256="1a12db7dbceaaf5cf4f9a0c03e2a2b9f32e91b697daf2ccfe81bbae9ac3046ce")
    version("0.3-3", sha256="d065d0ee42fb772760fca8d97ad2aa56cd76b1d9ecb4e97478ec362429e16738")
    version("0.3-2", sha256="5fcaf18324dc754152f528a44894944063303f780d33e58569ea7c306bfc45ac")

    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
