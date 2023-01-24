# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RabbitmqC(CMakePackage):
    """This is a C-language AMQP client library for use with v2.0+ of the
    RabbitMQ broker."""

    homepage = "https://github.com/alanxz/rabbitmq-c"
    url = "https://github.com/alanxz/rabbitmq-c/archive/refs/tags/v0.11.0.tar.gz"
    git = "https://github.com/alanxz/rabbitmq-c.git"

    maintainers = ["lpottier"]

    version("0.11.0", sha256="437d45e0e35c18cf3e59bcfe5dfe37566547eb121e69fca64b98f5d2c1c2d424")

    variant("ssl", default=True, description="Required to connect to RabbitMQ using SSL/TLS")
    variant("shared", default=True, description="Build shared library")
    variant("static", default=True, description="Build static library")
    variant("doc", default=False, description="Build the documentation")

    depends_on("cmake@3.12:", type="build")
    depends_on("openssl@1.1.1:", when="+ssl", type=("build", "link", "run"))
    depends_on("doxygen", when="+doc", type="build")

    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_SSL_SUPPORT", "ssl"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_STATIC_LIBS", "static"),
            # Tests can only be built against static libraries
            self.define_from_variant("BUILD_TESTS", "static"),
            self.define_from_variant("BUILD_API_DOCS", "doc"),
        ]
        return args
