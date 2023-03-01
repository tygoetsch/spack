# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


class NfTowerCli(Package):
    """Tower on the Command Line brings Nextflow Tower concepts
    including Pipelines, Actions and Compute Environments
    to the terminal.
    """

    homepage = "https://github.com/seqeralabs/tower-cli"
    maintainers("marcodelapierre")

    if platform.machine() == "x86_64":
        if platform.system() == "Darwin":
            version(
                "0.7.2",
                sha256="b72093af9c8d61e0150eb9d56cedb67afc982d2432221ae0819aaa0c8826ff2b",
                url="https://github.com/seqeralabs/tower-cli/releases/download/v0.7.2/tw-0.7.2-osx-x86_64",
                expand=False,
            )
            version(
                "0.7.1",
                sha256="a4731d0d7f2c2d4219758126a8ee0b22a0a68464329d4be0a025ad7eb191e5c0",
                url="https://github.com/seqeralabs/tower-cli/releases/download/v0.7.1/tw-0.7.1-osx-x86_64",
                expand=False,
            )
            version(
                "0.7.0",
                sha256="b1b3ade4231de2c7303832bac406510c9de171d07d6384a54945903f5123f772",
                url="https://github.com/seqeralabs/tower-cli/releases/download/v0.7.0/tw-0.7.0-osx-x86_64",
                expand=False,
            )
            version(
                "0.6.5",
                sha256="8e7369611f3617bad3e76264d93fe467c6039c86af9f18e26142dee5df1e7346",
                url="https://github.com/seqeralabs/tower-cli/releases/download/v0.6.5/tw-0.6.5-osx-x86_64",
                expand=False,
            )
            version(
                "0.6.2",
                sha256="2bcc17687d58d4c888e8d57b7f2f769a2940afb3266dc3c6c48b0af0cb490d91",
                url="https://github.com/seqeralabs/tower-cli/releases/download/v0.6.2/tw-0.6.2-osx-x86_64",
                expand=False,
            )
        elif platform.system() == "Linux":
            version(
                "0.7.2",
                sha256="a66d1655d2f3d83db160a890e6b3f20f4573978aa9e8ea5d6e505958a2980e72",
                url="https://github.com/seqeralabs/tower-cli/releases/download/v0.7.2/tw-0.7.2-linux-x86_64",
                expand=False,
            )
            version(
                "0.7.1",
                sha256="f3f8cf6b241f8935d4d90bd271809ca4cd7157ac476822483f458edbe54a1fa8",
                url="https://github.com/seqeralabs/tower-cli/releases/download/v0.7.1/tw-0.7.1-linux-x86_64",
                expand=False,
            )
            version(
                "0.7.0",
                sha256="651f564b80585c9060639f1a8fc82966f81becb0ab3e3ba34e53baf3baabff39",
                url="https://github.com/seqeralabs/tower-cli/releases/download/v0.7.0/tw-0.7.0-linux-x86_64",
                expand=False,
            )
            version(
                "0.6.5",
                sha256="0d1f3a6f53694000c1764bd3b40ce141f4b8923d477e2bdfdce75c66de95be00",
                url="https://github.com/seqeralabs/tower-cli/releases/download/v0.6.5/tw-0.6.5-linux-x86_64",
                expand=False,
            )
            version(
                "0.6.2",
                sha256="02c6d141416b046b6e8b6f9723331fe0e39d37faa3561c47c152df4d33b37e50",
                url="https://github.com/seqeralabs/tower-cli/releases/download/v0.6.2/tw-0.6.2-linux-x86_64",
                expand=False,
            )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(self.stage.archive_file, join_path(prefix.bin, "tw"))
        set_executable(join_path(prefix.bin, "tw"))
