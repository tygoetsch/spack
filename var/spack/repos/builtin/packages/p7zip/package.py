# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class P7zip(MakefilePackage):
    """A Unix port of the 7z file archiver"""

    maintainers = ["vmiheer"]
    homepage = "http://p7zip.sourceforge.net"
    url = "https://downloads.sourceforge.net/project/p7zip/p7zip/16.02/p7zip_16.02_src_all.tar.bz2"

    version("16.02", sha256="5eb20ac0e2944f6cb9c2d51dd6c4518941c185347d4089ea89087ffdd6e2341f")

    patch(
        "gcc10.patch",
        when="%gcc@10:",
        sha256="96914025b9f431fdd75ae69768162d57751413634622f9df1a4bc4960e7e8fe1",
    )

    # Replace boolean increments with assignments of true (which is
    # semantically equivalent). Use of increment operators on booleans is
    # forbidden by C++17, the default standard targeted by GCC 11.
    patch(
        "gcc11.patch",
        when="%gcc@11:",
        sha256="39dd15f2dfc86eeee8c3a13ffde65c2ca919433cfe97ea126fbdc016afc587d1",
    )

    # all3 includes 7z, 7za, and 7zr
    build_targets = ["all3"]

    depends_on("yasm", type="build", when="%clang")

    def edit(self, spec, prefix):
        # Use the suggested makefile
        for tgt, makefile in {
            "platform=linux %clang": "makefile.linux_clang_amd64_asm",
            "platform=darwin %gcc": "makefile.macosx_gcc_64bits",
            "platform=darwin %apple-clang": "makefile.macosx_llvm_64bits",
            "platform=darwin %clang": "makefile.macosx_llvm_64bits",
        }.items():
            if tgt in self.spec:
                copy(makefile, "makefile.machine")
                break
        # Silence an error about -Wc++11-narrowing in clang.
        if "@16.02 %clang" in spec:
            with open("makefile.machine", "a") as f:
                f.write("ALLFLAGS += -Wno-c++11-narrowing")

    @property
    def install_targets(self):
        return ["DEST_HOME={0}".format(self.prefix), "install"]
