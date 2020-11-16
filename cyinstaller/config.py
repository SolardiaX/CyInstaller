# -*- coding: utf-8 -*-

"""
    cyinstall.config
    ~~~~~~~~~~~~~~~~~~~
     The custom config loader of CyInstaller

    :copyright: (c) 2019 by DreamEx Works.
    :license: GPL-3.0, see LICENSE for more details.
"""

import os
from pathlib import Path
from typing import Union

import yaml

_default_config = {
    'app': {
        'name': 'CyInstaller Application',
        'root': '.',
    },
    'cython': {
        'compiler_directives': {
            'always_allow_keywords': True
        },
        'nthreads': 0,
        'language_level': 3,
        'sources': [],
        'excludes': ['**/*/__init__.py'],
    },
    'pyinstaller': {
        'datas': [],
        'binaries': [],
        'excludes': [],
        'hiddenimports': [],
        'auto_import': True,
        'cython_binaries': True,
        'sources': []
    },
    'paths': {
        'build': 'build',
        'target': 'target'
    },
    'stages': {
        'cython': True,
        'pyinstaller': True,
        'debug': True,
    }
}


def merge_dict(src: dict, default: dict):
    for k, v in src.items():
        if v is None:
            src[k] = default.get(k, None)
            continue

        t = default.get(k, None)
        if t is None:
            continue

        if isinstance(v, dict):
            src[k] = merge_dict(v, t)
        if isinstance(v, (tuple, list)):
            if isinstance(t, (tuple, list)):
                v.extend(t)
            else:
                v.append(v)
            src[k] = v
        elif type(v) != type(t):
            raise ValueError('Config %s value type error.' % k)

    return src


class Config:
    def __init__(self, yaml_file='setup.yaml') -> None:
        if not os.path.exists(yaml_file):
            raise EnvironmentError('CyInstaller yaml file not exists.')

        with open(Path(os.getcwd()).joinpath(yaml_file), 'r') as cfg:
            config = yaml.safe_load(cfg)
            self._config = merge_dict(config, _default_config)

    @property
    def app_name(self) -> str:
        return self._config.get('app', _default_config['app'])['name']

    @property
    def app_root(self) -> Path:
        return Path(self._config['app']['root'])

    @property
    def cython_sources(self) -> [str]:
        return self._config['cython']['sources']

    @property
    def cython_options(self) -> dict:
        options = self._config['cython'].copy()
        for o in ('sources', 'excludes'):
            options.pop(o)
        return options

    @property
    def cython_excludes(self) -> [str]:
        return self._config['cython']['excludes']

    @property
    def pyinstaller_sources(self) -> [str]:
        return self._config['pyinstaller']['sources']

    @property
    def pyinstaller_datas(self) -> [str]:
        return self._config['pyinstaller']['datas']

    @property
    def pyinstaller_data_mapping(self) -> [(Path, Path)]:
        for data in self.pyinstaller_datas:
            mapping = data.split('::')

            rglob = mapping[0] if len(mapping) == 1 else mapping[1]
            rroot = self.app_root if len(mapping) == 1 else Path(mapping[0])
            rdist = self.build_cython_path if len(mapping) < 3 else self.build_cython_path.joinpath(mapping[2])

            for source in rroot.glob(rglob):
                target = Path(str(source).replace(str(rroot), str(rdist)))
                yield source, target

    @property
    def pyinstaller_binaries(self) -> [str]:
        return self._config['pyinstaller']['binaries']

    @property
    def pyinstaller_hiddenimports(self) -> [str]:
        return self._config['pyinstaller']['hiddenimports']

    @property
    def pyinstaller_auto_import(self) -> bool:
        return self._config['pyinstaller']['auto_import']

    @property
    def pyinstaller_cython_binaries(self) -> bool:
        return self._config['pyinstaller']['cython_binaries']

    @property
    def pyinstaller_template(self) -> Union[str, None]:
        return self._config['pyinstaller']['template']

    @property
    def build_root_path(self) -> Path:
        return Path(self._config['paths']['build'])

    @property
    def build_cython_path(self) -> Path:
        return self.build_root_path.joinpath('cython')

    @property
    def build_pyinstaller_path(self) -> Path:
        return self.build_root_path.joinpath('pack')

    @property
    def build_temp_path(self) -> Path:
        return self.build_root_path.joinpath('tmp')

    @property
    def target_path(self) -> Path:
        return Path(self._config['paths']['target'])

    @property
    def is_debug(self) -> bool:
        return bool(self._config['stages']['debug'])
