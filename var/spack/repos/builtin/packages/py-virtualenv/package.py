# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVirtualenv(PythonPackage):
    """virtualenv is a tool to create isolated Python environments."""

    homepage = "https://virtualenv.pypa.io/"
    pypi = "virtualenv/virtualenv-16.7.6.tar.gz"
    git = "https://github.com/pypa/virtualenv.git"

    version("20.17.1", sha256="f8b927684efc6f1cc206c9db297a570ab9ad0e51c16fa9e45487d36d1905c058")
    version("20.16.4", sha256="014f766e4134d0008dcaa1f95bafa0fb0f575795d07cae50b1bee514185d6782")
    version("20.10.0", sha256="576d05b46eace16a9c348085f7d0dc8ef28713a2cabaa1cf0aea41e8f12c9218")
    version("16.7.6", sha256="5d370508bf32e522d79096e8cbea3499d47e624ac7e11e9089f9397a0b3318df")
    version("16.4.1", sha256="5a3ecdfbde67a4a3b3111301c4d64a5b71cf862c8c42958d30cf3253df1f29dd")
    version("16.0.0", sha256="ca07b4c0b54e14a91af9f34d0919790b016923d157afda5efdde55c96718f752")
    version("15.1.0", sha256="02f8102c2436bb03b3ee6dede1919d1dac8a427541652e5ec95171ec8adbc93a")
    version("15.0.1", sha256="1a74278b8adb383ce4c7619e33c753b1eb7b58dc1e449601c096ca4b76125f84")
    version("13.0.1", sha256="36c2cfae0f9c6462264bb19c478fc6bab3478cf0575f1027452e975a1ed84dbd")
    version("1.11.6", sha256="3e7a4c151e2ee97f51db0215bfd2a073b04a91e9786df6cb67c916f16abe04f7")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:", when="@20.10.0:", type=("build", "run"))
    depends_on("python@3.6:", when="@20.16.4:", type=("build", "run"))

    # not just build-time, requires pkg_resources
    depends_on("py-setuptools@40.6.3:", type=("build", "run"))
    depends_on("py-setuptools@41.00.03:", when="@20.10.0:", type=("build", "run"))
    depends_on("py-setuptools@59.6:", when="@20.16.4:", type=("build", "run"))
    depends_on("py-setuptools-scm@2:", when="@20.10.0:", type="build")
    depends_on("py-setuptools-scm@6.4.2:", when="@20.16.4:", type="build")

    depends_on("py-distlib@0.3.1:0", when="@20.10.0:", type=("build", "run"))
    depends_on("py-distlib@0.3.5:0", when="@20.16.4:", type=("build", "run"))
    depends_on("py-distlib@0.3.6:0", when="@20.16.6:", type=("build", "run"))
    depends_on("py-filelock@3.2:3", when="@20.10.0:", type=("build", "run"))
    depends_on("py-filelock@3.4.1:3", when="@20.16.4:", type=("build", "run"))
    depends_on("py-platformdirs@2:2", when="@20.10.0:", type=("build", "run"))
    depends_on("py-platformdirs@2.4:2", when="@20.16.4:", type=("build", "run"))
    depends_on("py-importlib-metadata@0.12:", when="@20.10.0: ^python@:3.7", type=("build", "run"))
    depends_on(
        "py-importlib-metadata@4.8.3:", when="@20.16.4: ^python@:3.7", type=("build", "run")
    )

    # dependencies of old versions
    depends_on(
        "py-backports-entry-points-selectable @1.0.4:", when="@20.10.0", type=("build", "run")
    )
    depends_on("py-six@1.9.0:1", when="@20.10.0", type=("build", "run"))
