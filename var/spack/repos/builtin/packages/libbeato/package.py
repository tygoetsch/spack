# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libbeato(AutotoolsPackage):
    """libbeato is a C library containing routines for various uses in Genomics,
    and includes a copy of the freeware portion of the C library
    from UCSC's Genome Browser Group."""

    homepage = "https://github.com/CRG-Barcelona/libbeato"
    git = "https://github.com/CRG-Barcelona/libbeato.git"

    version("master", branch="master")
