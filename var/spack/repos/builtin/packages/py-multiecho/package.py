# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMultiecho(PythonPackage):
    """Combine multi-echoes from a multi-echo fMRI acquisition."""

    homepage = "https://github.com/Donders-Institute/multiecho"
    pypi = "multiecho/multiecho-0.28.tar.gz"

    version("0.28", sha256="d0459bd03398547116d8e989b2d2b7922af0ae7ae77e233794dd7253a2abced3")

    depends_on("python@3.6:3.9", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-coloredlogs", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-nibabel", type=("build", "run"))
