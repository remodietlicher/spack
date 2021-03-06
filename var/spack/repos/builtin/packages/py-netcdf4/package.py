# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNetcdf4(PythonPackage):
    """Python interface to the netCDF Library."""

    homepage = "https://github.com/Unidata/netcdf4-python"
    url      = "https://pypi.io/packages/source/n/netCDF4/netCDF4-1.2.7.tar.gz"

    version('1.4.2',   sha256='b934af350459cf9041bcdf5472e2aa56ed7321c018d918e9f325ec9a1f9d1a30')
    version('1.2.7',   sha256='0c449b60183ee06238a8f9a75de7b0eed3acaa7a374952ff9f1ff06beb8f94ba')
    version('1.2.3.1', sha256='55edd74ef9aabb1f7d1ea3ffbab9c555da2a95632a97f91c0242281dc5eb919f')

    depends_on('py-setuptools',   type='build')
    depends_on('py-cython@0.19:', type='build')

    depends_on('py-numpy@1.7:', type=('build', 'run'))
    depends_on('py-cftime', type=('build', 'run'))

    depends_on('netcdf-c')
    depends_on('hdf5@1.8.0:+hl')

    def setup_build_environment(self, env):
        """Ensure installed netcdf and hdf5 libraries are used"""
        # Explicitly set these variables so setup.py won't erroneously pick up
        # system versions
        env.set('USE_SETUPCFG', '0')
        env.set('HDF5_INCDIR', self.spec['hdf5'].prefix.include)
        env.set('HDF5_LIBDIR', self.spec['hdf5'].prefix.lib)
        env.set('NETCDF4_INCDIR', self.spec['netcdf-c'].prefix.include)
        env.set('NETCDF4_LIBDIR', self.spec['netcdf-c'].prefix.lib)
