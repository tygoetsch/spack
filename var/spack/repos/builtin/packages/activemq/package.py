# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Activemq(Package):
    """
    Apache ActiveMQ is a high performance Apache 2.0 licensed Message Broker
    and JMS 1.1 implementation.
    """

    homepage = "https://archive.apache.org/dist/activemq"
    url = "https://archive.apache.org/dist/activemq/5.14.0/apache-activemq-5.14.0-bin.tar.gz"

    version("5.17.3", sha256="a4cc4c3a2f136707c2c696f3bb3ee2a86dbeff1b9eb5e237b14edc0c5e5a328f")

    # https://nvd.nist.gov/vuln/detail/CVE-2018-11775
    version(
        "5.14.0",
        sha256="81c623465af277dd50a141a8d9308d6ec8e1b78d9019b845873dc12d117aa9a6",
        deprecated=True,
    )

    depends_on("java")

    def install(self, spec, prefix):
        install_tree(".", prefix)
