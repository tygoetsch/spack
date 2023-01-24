# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRjson(RPackage):
    """JSON for R.

    Converts R object into JSON objects and vice-versa."""

    cran = "rjson"

    version("0.2.21", sha256="982b56d35ccc0c7db0b20c1d3eab5f5f47c620309646fdc278ff1cc3433ea2e2")
    version("0.2.20", sha256="3a287c1e5ee7c333ed8385913c0a307daf99335fbdf803e9dcca6e3d5adb3f6c")
    version("0.2.19", sha256="5c2672461986f2b715416cab92ed262abe9875f31299bc8a1a072ef7c6dd49bc")
    version("0.2.15", sha256="77d00d8f6a1c936329b46f3b8b0be79a165f8c5f1989497f942ecc53dcf6f2ef")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@0.2.21:")
