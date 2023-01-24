# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFracdiff(RPackage):
    """Fractionally Differenced ARIMA aka ARFIMA(P,d,q) Models.

    Maximum likelihood estimation of the parameters of a fractionally
    differenced ARIMA(p,d,q) model (Haslett and Raftery, Appl.Statistics,
    1989); including inference and basic methods.  Some alternative algorithms
    to estimate "H"."""

    cran = "fracdiff"

    version("1.5-2", sha256="ac5f881330287f5bc68b5cdce4fb74156a95356ffb875ee171538bc44200f437")
    version("1.5-1", sha256="b8103b32a4ca3a59dda1624c07da08ecd144c7a91a747d1f4663e99421950eb6")
    version("1.4-2", sha256="983781cedc2b4e3ba9fa020213957d5133ae9cd6710bc61d6225728e2f6e850e")
