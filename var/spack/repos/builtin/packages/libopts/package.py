# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libopts(AutotoolsPackage):
    """LibOPT is an optimization library developed in C language for the
    development of metaheuristic-based techniques."""

    homepage = "https://github.com/jppbsi/LibOPT/"
    git = "https://github.com/jppbsi/LibOPT.git"

    version("master", branch="master")

    parallel = False

    def install(self, spec, prefix):
        install_tree("lib", prefix.lib)
