# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ripgrep(Package):
    """ripgrep is a line-oriented search tool that recursively searches
    your current directory for a regex pattern.  ripgrep is similar to
    other popular search tools like The Silver Searcher, ack and grep.
    """

    homepage = "https://github.com/BurntSushi/ripgrep"
    url = "https://github.com/BurntSushi/ripgrep/archive/11.0.2.tar.gz"

    version("13.0.0", sha256="0fb17aaf285b3eee8ddab17b833af1e190d73de317ff9648751ab0660d763ed2")
    version("11.0.2", sha256="0983861279936ada8bc7a6d5d663d590ad34eb44a44c75c2d6ccd0ab33490055")

    depends_on("rust")

    def install(self, spec, prefix):
        cargo = which("cargo")
        cargo("install", "--root", prefix, "--path", ".")
