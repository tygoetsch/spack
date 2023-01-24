# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyInstaller(PythonPackage):
    """A library for installing Python wheels."""

    homepage = "https://github.com/pradyunsg/installer"
    pypi = "installer/installer-0.4.0.tar.gz"

    version("0.4.0", sha256="17d7ca174039fbd85f268e16042e3132ebb03d91e1bbe0f63b9ec6b40619414a")

    depends_on("python@2.7,3.5:", type=("build", "run"))
    depends_on("py-flit-core@2", type="build")
