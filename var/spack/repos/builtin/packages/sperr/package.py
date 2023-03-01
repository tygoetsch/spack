# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sperr(CMakePackage):
    """SPERR is a lossy scientific (floating-point) data compressor that can
    perform either error-bounded or size-bounded data compression"""

    homepage = "https://github.com/NCAR/SPERR"
    url = "https://github.com/NCAR/SPERR/archive/refs/tags/v0.5.tar.gz"
    git = homepage

    version("0.5", sha256="20ad48c0e7599d3e5866e024d0c49648eb817f72ad5459f5468122cf14a97171")

    depends_on("git", type="build")
    depends_on("zstd", type=("build", "link"), when="+zstd")
    depends_on("pkgconfig", type=("build"), when="+zstd")

    variant("shared", description="build shared libaries", default=True)
    variant("zstd", description="use Zstd for more compression", default=True)
    variant("openmp", description="use openmp for acceleration", default=True)

    maintainers("shaomeng", "robertu94")

    def cmake_args(self):
        # ensure the compiler supports OpenMP if it is used
        if "+openmp" in self.spec:
            self.compiler.openmp_flag

        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("USE_ZSTD", "zstd"),
            self.define_from_variant("USE_OMP", "openmp"),
            "-DSPERR_PREFER_RPATH=OFF",
            "-DUSE_BUNDLED_ZSTD=OFF",
            "-DBUILD_CLI_UTILITIES=OFF",
            "-DBUILD_UNIT_TESTS=OFF",
        ]
        return args
