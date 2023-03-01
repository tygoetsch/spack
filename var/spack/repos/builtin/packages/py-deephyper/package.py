# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDeephyper(PythonPackage):
    """Scalable asynchronous neural architecture and hyperparameter
    search for deep neural networks."""

    homepage = "https://deephyper.readthedocs.io/"
    pypi = "deephyper/deephyper-0.4.2.tar.gz"
    git = "https://github.com/deephyper/deephyper.git"

    maintainers("mdorier", "Deathn0t")

    version("master", branch="master")
    version("0.4.2", sha256="ee1811a22b08eff3c9098f63fbbb37f7c8703e2f878f2bdf2ec35a978512867f")

    depends_on("python@3.7:3.9", type=("build", "run"))

    depends_on("py-setuptools@40:49.1", type="build")
    depends_on("py-wheel@0.36.2", type="build")
    depends_on("py-cython@0.29.24:2", type="build")

    depends_on("py-configspace@0.4.20:", type=("build", "run"))
    depends_on("py-dm-tree", type=("build", "run"))
    depends_on("py-jinja2@:3.0", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas@0.24.2:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-scikit-learn@0.23.1:", type=("build", "run"))
    depends_on("py-scipy@0.19.1:", type=("build", "run"))
    depends_on("py-tqdm@4.64.0:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-tinydb", type=("build", "run"))
