# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class Pscmc(MakefilePackage):
    """The SCMC and PSCMC programming language
    is designed for multi-platform
    parallel programming."""

    maintainers = ["Bitllion"]

    homepage = "https://github.com/JianyuanXiao/PSCMC"
    git = "https://github.com/JianyuanXiao/PSCMC.git"

    version("master", branch="master")

    def setup_run_environment(self, env):
        env.set("SCMC_COMPILE_ROOT", self.prefix.source)
        env.set("SCMC_ROOT", join_path(self.prefix.source, "runtime_passes"))
        env.set("STDLIB", join_path(self.prefix.source, "stdlib.scm"))

    def build(self, spec, prefix):
        with working_dir("source"):
            make()
        with working_dir("source/scompiler"):
            makefile = FileFilter("Makefile")
            makefile.filter("CC=clang", "CC=gcc")
            make()
            os.system("./gen_pscmc_compiler")

    def install(self, spec, prefix):
        mkdir(prefix.source)
        ln = which("ln")
        ln("-s", prefix.source, prefix.bin)
        install_tree("./", prefix)
