# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Osmesa(BundlePackage):
    """Shim package for the OSMesa OpenGL library."""

    homepage = "https://www.mesa3d.org"

    version("11.2.0")

    depends_on("libosmesa")
    provides("gl@4.5")

    @property
    def home(self):
        return self.spec["libosmesa"].home

    @property
    def headers(self):
        return self.spec["libosmesa"].headers

    @property
    def libs(self):
        return self.spec["libosmesa"].libs

    @property
    def gl_headers(self):
        return find_headers("GL/gl", root=self.gl_home, recursive=True)

    @property
    def gl_libs(self):
        return self.spec["libosmesa"].libs
