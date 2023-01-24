# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Tuple

import spack.builder
import spack.directives
import spack.package_base

from ._checks import BaseBuilder, apply_macos_rpath_fixups


class Package(spack.package_base.PackageBase):
    """General purpose class with a single ``install`` phase that needs to be
    coded by packagers.
    """

    #: This attribute is used in UI queries that require to know which
    #: build-system class we are using
    build_system_class = "Package"
    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "generic"

    spack.directives.build_system("generic")


@spack.builder.builder("generic")
class GenericBuilder(BaseBuilder):
    """A builder for a generic build system, that require packagers
    to implement an "install" phase.
    """

    #: A generic package has only the "install" phase
    phases = ("install",)

    #: Names associated with package methods in the old build-system format
    legacy_methods: Tuple[str, ...] = ()

    #: Names associated with package attributes in the old build-system format
    legacy_attributes: Tuple[str, ...] = ("archive_files",)

    # On macOS, force rpaths for shared library IDs and remove duplicate rpaths
    spack.builder.run_after("install", when="platform=darwin")(apply_macos_rpath_fixups)
