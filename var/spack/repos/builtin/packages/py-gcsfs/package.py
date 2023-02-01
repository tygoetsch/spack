# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGcsfs(PythonPackage):
    """Pythonic file-system for Google Cloud Storage."""

    homepage = "https://github.com/fsspec/gcsfs"
    pypi = "gcsfs/gcsfs-2023.1.0.tar.gz"

    version("2023.1.0", sha256="0a7b7ca8c1affa126a14ba35d7b7dff81c49e2aaceedda9732c7f159a4837a26")

    depends_on("py-setuptools", type="build")
    depends_on("py-aiohttp", type=("build", "run"))
    depends_on("py-decorator@4.1.3:", type=("build", "run"))
    depends_on("py-fsspec@2023.1.0", type=("build", "run"))
    depends_on("py-google-auth@1.2:", type=("build", "run"))
    depends_on("py-google-auth-oauthlib", type=("build", "run"))
    depends_on("py-google-cloud-storage", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
