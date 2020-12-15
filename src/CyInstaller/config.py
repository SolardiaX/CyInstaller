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
    'app': 'CyInstaller Application',
    'root': '.',
    'compiles': [],
    'packages': [],
    'datas': [],
    'binaries': [],
    'cython_binaries': True,
    'relates': [],
    'hiddenimports': [],
    'modules': [],
    'auto_hiddenimports': True,

    'stage': {
        'path': '_build',
        'debug': True,
        'cython': {
            'path_tmp': 'compile',
            'path': 'cython',
            'options': {
                'compiler_directives': {
                    'always_allow_keywords': True
                },
                'nthreads': 0,
                'language_level': 3,
            }
        },
        'pyinstaller': {
            'path': 'package',
            'template': None,
        },
        'dist': 'target'
    }
}


def merge_dict(src: dict, default: dict):
    dist = src.copy()

    for k, v in dist.items():
        if v is None:
            dist[k] = default.get(k, None)
            continue

        t = default.get(k, None)
        if t is None:
            continue

        if isinstance(v, dict):
            dist[k] = merge_dict(v, t)
        if isinstance(v, (tuple, list)):
            if isinstance(t, (tuple, list)):
                v.extend(t)
            else:
                v.append(v)
            dist[k] = v
        elif type(v) != type(t):
            raise ValueError('Config %s value type error.' % k)

    for k, v in default.items():
        if k not in dist.keys():
            dist[k] = v

    return dist


class PortableSource:
    def __init__(self, src: str, base=Path(''), to=Path('')) -> None:
        self._exclude = src.startswith('!')

        if self._exclude:
            src = src[1:]

        _mapping = src.split('::')

        self._port = base if len(_mapping) == 1 else base.joinpath(_mapping[0])

        _source = (_mapping[0] if len(_mapping) == 1 else _mapping[1]).split('->')

        self._source = _source[0]
        self._to = to if len(_source) == 1 else to.joinpath(_source[1])
        self._realsource = self._port.joinpath(self._source)

    @property
    def origin(self):
        if self._to is None:
            return '%s::%s' % (self._port, self._source)
        return '%s::%s->%s' % (self._port, self._source, self._to)

    @property
    def realsource(self) -> Path:
        return self._realsource

    @property
    def port(self) -> Path:
        return self._port

    @property
    def source(self) -> str:
        return self._source

    @property
    def to(self) -> Path:
        return self._to

    @property
    def is_exclude(self):
        return self._exclude

    def __eq__(self, other):
        return self.origin == other.origin

    def __hash__(self):
        return self.origin.__hash__()

    def __str__(self):
        return self.origin

    def __repr__(self):
        return self.origin


class SourceList:
    def __init__(self, sources: [Union[str, PortableSource]]) -> None:
        item = sources[0] if len(sources) > 0 else None

        if isinstance(item, str):
            s = [PortableSource(x) for x in sources]
        else:
            s = sources

        self._list = list(s)

    def extend(self, others):
        self._list.extend(others.all)

    @property
    def all(self) -> [PortableSource]:
        return self._list

    @property
    def includes(self) -> [PortableSource]:
        return [x for x in self._list if not x.is_exclude]

    @property
    def raw_includes(self) -> [str]:
        return [str(x.realsource) for x in self.includes]

    @property
    def excludes(self) -> [PortableSource]:
        return [x for x in self._list if x.is_exclude]

    @property
    def raw_excludes(self) -> [str]:
        return [str(x.realsource) for x in self.excludes]

    @property
    def pures(self) -> [PortableSource]:
        includes = list()
        for inc in self.includes:
            for src in inc.port.glob(inc.source):
                includes.append(PortableSource('%s::%s->%s' % (inc.port, src.relative_to(inc.port), inc.to)))
        excludes = list()
        for exc in self.excludes:
            for src in exc.port.glob(exc.source):
                includes.append(PortableSource('%s::%s->%s' % (exc.port, src.relative_to(exc.port), exc.to)))

        return [item for item in includes if item not in excludes]

    def mappings(self, to=None) -> [PortableSource]:
        includes = list()
        for inc in self.includes:
            to = inc.to if to is None else to
            if isinstance(to, str):
                to = Path(to)

            for src in inc.port.glob(inc.source):
                includes.append(PortableSource('%s::%s->%s' % (inc.port, src.relative_to(inc.port), to)))

        excludes = list()
        for exc in self.excludes:
            to = exc.to if to is None else to
            if isinstance(to, str):
                to = Path(to)

            for src in exc.port.glob(exc.source):
                includes.append(PortableSource('%s::%s->%s' % (exc.port, src.relative_to(exc.port), to)))

        return [item for item in includes if item not in excludes]

    def __str__(self):
        return str([x for x in self.all])


class ModuleConfig:
    def __init__(self, config: dict) -> None:
        self._base = Path(config.get('base', None))
        self._package = config.get('package', None)
        self._package_from_base = config.get('package_from_base', True)

        if self._base is None:
            raise SyntaxError('The base path of module is None.')

        if self._package is None:
            raise SyntaxError('The package name of module in % is None.' % self._base)

        if not self._package_from_base:
            self._packagebase = self._base.joinpath(self._package)

        self._compiles = SourceList(
            [PortableSource(x, self._packagebase, self._package) for x in config.get('compiles') or []])
        self._packages = SourceList(
            [PortableSource(x, self._base, self._package) for x in config.get('packages') or []])
        self._binaries = SourceList(
            [PortableSource(x, self._base, self._package) for x in config.get('binaries') or []])
        self._datas = SourceList(
            [PortableSource(x, self._base, self._package) for x in config.get('datas') or []])
        self._relates = SourceList(
            [PortableSource(x, self._base, self._package) for x in config.get('relates') or []])

    @property
    def base(self) -> Path:
        return self._base

    @property
    def package(self) -> str:
        return self._package

    @property
    def package_from_base(self):
        return self._package_from_base

    @property
    def compiles(self) -> SourceList:
        return self._compiles

    @property
    def packages(self) -> SourceList:
        return self._packages

    @property
    def binaries(self) -> SourceList:
        return self._binaries

    @property
    def datas(self) -> SourceList:
        return self._datas

    @property
    def relates(self) -> SourceList:
        return self._relates


class Config:
    def __init__(self, yaml_file='setup.yml') -> None:
        if not os.path.exists(yaml_file):
            raise EnvironmentError('CyInstaller yaml file not exists.')

        try:
            with open(Path(os.getcwd()).joinpath(yaml_file), 'r') as cfg:
                config = yaml.safe_load(cfg)
                self._config = merge_dict(config.get('setup', {}), _default_config)

                self._modules = []
                for m in self._config['modules']:
                    self._modules.append(ModuleConfig(m))

                if self._config.get('entrypoint', None) is None:
                    raise ValueError('The entrypoint not set.')

                self._entrypoint = PortableSource(self._config['entrypoint'])

        except Exception as e:
            raise SyntaxError('Error load CyInstaller configuration from yaml - %s' % e)

    @property
    def name(self) -> str:
        return self._config['name']

    @property
    def root(self) -> Path:
        return Path(self._config['root'])

    @property
    def compiles(self) -> SourceList:
        collection = SourceList([])
        for module in self._modules:
            collection.extend(module.compiles)
        collection.extend(SourceList([PortableSource(x) for x in self._config['compiles']]))
        return collection

    @property
    def packages(self) -> SourceList:
        collection = SourceList([])
        for module in self._modules:
            collection.extend(module.packages)
        collection.extend(SourceList([PortableSource(x) for x in self._config['packages']]))
        return collection

    @property
    def binaries(self) -> SourceList:
        collection = SourceList([])
        for module in self._modules:
            collection.extend(module.binaries)
        collection.extend(SourceList([PortableSource(x) for x in self._config['binaries']]))
        return collection

    @property
    def cython_binaries(self) -> bool:
        return self._config['cython_binaries']

    @property
    def datas(self) -> SourceList:
        collection = SourceList([])
        for module in self._modules:
            collection.extend(module.datas)
        collection.extend(SourceList([PortableSource(x) for x in self._config['datas']]))
        return collection

    @property
    def relates(self) -> SourceList:
        collection = SourceList([])
        for module in self._modules:
            collection.extend(module.relates)
        collection.extend(SourceList([PortableSource(x) for x in self._config['relates']]))
        return collection

    @property
    def hiddenimports(self) -> [str]:
        return self._config['hiddenimports']

    @property
    def auto_hiddenimports(self) -> bool:
        return self._config['auto_hiddenimports']

    @property
    def modules(self) -> [ModuleConfig]:
        return self._modules

    @property
    def entrypoint(self) -> PortableSource:
        return self._entrypoint

    @property
    def stage_path(self) -> Path:
        return Path(self._config['stage']['path'])

    @property
    def stage_debug(self) -> bool:
        return self._config['stage']['debug']

    @property
    def stage_cython_path(self) -> Path:
        return self.stage_path.joinpath(self._config['stage']['cython']['path'])

    @property
    def stage_cython_temp_path(self) -> Path:
        return self.stage_path.joinpath(self._config['stage']['cython']['path_tmp'])

    @property
    def stage_cython_options(self) -> dict:
        return self._config['stage']['cython']['options']

    @property
    def stage_pyinstaller_path(self) -> Path:
        return self.stage_path.joinpath(self._config['stage']['pyinstaller']['path'])

    @property
    def stage_pyinstaller_template(self) -> str:
        return self._config['stage']['pyinstaller']['template']

    @property
    def dist(self) -> Path:
        return self.root.joinpath(self._config['dist'])
