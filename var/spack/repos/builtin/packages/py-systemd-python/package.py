# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySystemdPython(PythonPackage):
    """Python interface for libsystemd"""

    homepage = "https://github.com/systemd/python-systemd"
    pypi = "systemd-python/systemd-python-234.tar.gz"

    version("234", sha256="fd0e44bf70eadae45aadc292cb0a7eb5b0b6372cd1b391228047d33895db83e7")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
