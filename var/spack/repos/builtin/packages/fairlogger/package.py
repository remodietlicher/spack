# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
#   Spack Project Developers. See the top-level COPYRIGHT file for details.
# Copyright 2020 GSI Helmholtz Centre for Heavy Ion Research GmbH,
#   Darmstadt, Germany
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fairlogger(CMakePackage):
    """Lightweight and fast C++ Logging Library"""

    homepage = 'https://github.com/FairRootGroup/FairLogger'
    url = "https://github.com/FairRootGroup/FairLogger/archive/v1.2.0.tar.gz"
    git = 'https://github.com/FairRootGroup/FairLogger.git'
    maintainers = ['dennisklein', 'ChristianTackeGSI']
    # generator = 'Ninja'

    version('develop', branch='dev')
    version('1.6.1', sha256='3894580f4c398d724ba408e410e50f70c9f452e8cfaf7c3ff8118c08df28eaa8')
    version('1.6.0', sha256='721e8cadfceb2f63014c2a727e098babc6deba653baab8866445a772385d0f5b')
    version('1.5.0', sha256='8e74e0b1e50ee86f4fca87a44c6b393740b32099ac3880046bf252c31c58dd42')
    version('1.4.0', sha256='75457e86984cc03ce87d6ad37adc5aab1910cabd39a9bbe5fb21ce2475a91138')
    version('1.3.0', sha256='5cedea2773f7091d69aae9fd8f724e6e47929ee3784acdd295945a848eb36b93')
    version('1.2.0', sha256='bc0e049cf84ceb308132d8679e7f22fcdca5561dda314d5233d0d5fe2b0f8c62')
    version('1.1.0', sha256='e185e5bd07df648224f85e765d18579fae0de54adaab9a194335e3ad6d3d29f7')
    version('1.0.6', sha256='2fc266a6e494adda40837be406aef8d9838f385ffd64fbfafb1164833906b4e0')

    variant('build_type', default='RelWithDebInfo',
            values=('Debug', 'Release', 'RelWithDebInfo'),
            multi=False,
            description='CMake build type')
    variant('cxxstd', default='11',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')
    variant('pretty',
            default=False,
            description='Use BOOST_PRETTY_FUNCTION macro.')
    conflicts('+pretty', when='@:1.3.99')

    depends_on('cmake@3.9.4:', type='build')
    depends_on('git', type='build', when='@develop')
    depends_on('boost', when='+pretty')
    depends_on('fmt@5.3.0:', when='@1.6.0:')

    def patch(self):
        """FairLogger gets its version number from git.
           But the tarball doesn't have that information, so
           we patch the spack version into CMakeLists.txt"""
        if not self.spec.satisfies("@develop"):
            filter_file(r'(get_git_version\(.*)\)',
                        r'\1 DEFAULT_VERSION %s)' % self.spec.version,
                        'CMakeLists.txt')

    def cmake_args(self):
        cxxstd = self.spec.variants['cxxstd'].value
        args = []
        args.append('-DCMAKE_CXX_STANDARD=%s' % cxxstd)
        args.append('-DUSE_BOOST_PRETTY_FUNCTION=%s' %
                    ('ON' if '+pretty' in self.spec else 'OFF'))
        if self.spec.satisfies('@1.6:'):
            args.append('-DUSE_EXTERNAL_FMT=ON')
        return args
