# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibcxxwrapJulia(CMakePackage):
    """This is the C++ library component of the CxxWrap.jl package, distributed as a
    regular CMake library for use in other C++ projects."""

    homepage = "https://github.com/JuliaInterop/libcxxwrap-julia"
    url = "https://github.com/JuliaInterop/libcxxwrap-julia/archive/refs/tags/v0.8.3.tar.gz"
    git = "https://github.com/JuliaInterop/libcxxwrap-julia.git"

    maintainers("eloop")

    # note: use the @main branch version if you're building for julia 1.7
    version("main", branch="main")

    version("0.9.1", sha256="d7938d88ae2dbcc6abf505df3ac280dcd7c85fca0954af56911cf510d6161e05")
    version("0.8.3", sha256="b0421d11bdee5ce8af4922de6dfe3b0e5d69b07bb52894e3a22a477bbd27ee9e")
    version("0.8.2", sha256="f8b171def3d61904ba8f9a9052a405c25afbfb9a3c5af3dd30bc36a0184ed539")

    depends_on("julia")
