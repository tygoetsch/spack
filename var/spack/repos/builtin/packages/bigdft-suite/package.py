# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BigdftSuite(BundlePackage):
    """BigDFT-suite: the complete suite of BigDFT for electronic structure calculation
    based on Daubechies wavelets."""

    homepage = "https://bigdft.org/"
    url = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.2/bigdft-suite-1.9.2.tar.gz"
    git = "https://gitlab.com/l_sim/bigdft-suite.git"

    version("develop", branch="devel")
    version("1.9.2", sha256="dc9e49b68f122a9886fa0ef09970f62e7ba21bb9ab1b86be9b7d7e22ed8fbe0f")
    version("1.9.1", sha256="3c334da26d2a201b572579fc1a7f8caad1cbf971e848a3e10d83bc4dc8c82e41")
    version("1.9.0", sha256="4500e505f5a29d213f678a91d00a10fef9dc00860ea4b3edf9280f33ed0d1ac8")

    depends_on("python@3.0:", type=("run"))

    for vers in ["1.9.0", "1.9.1", "1.9.2", "develop"]:
        depends_on("bigdft-futile@{0}".format(vers), when="@{0}".format(vers))
        depends_on("bigdft-psolver@{0}".format(vers), when="@{0}".format(vers))
        depends_on("bigdft-libabinit@{0}".format(vers), when="@{0}".format(vers))
        depends_on("bigdft-chess@{0}".format(vers), when="@{0}".format(vers))
        depends_on("bigdft-core@{0}".format(vers), when="@{0}".format(vers))
        depends_on("bigdft-spred@{0}".format(vers), when="@{0}".format(vers))
        depends_on("bigdft-atlab@{0}".format(vers), when="@{0}".format(vers))
        depends_on("py-bigdft@{0}".format(vers), when="@{0}".format(vers))
