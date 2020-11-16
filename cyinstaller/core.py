# -*- coding: utf-8 -*-

"""
    cyinstall.core
    ~~~~~~~~~~~~~~~~~~~
     The core methods of CyInstaller
    
    :copyright: (c) 2019 by DreamEx Works.
    :license: GPL-3.0, see LICENSE for more details.
"""

import re
import os
import platform

from pathlib import Path
from typing import Union
from shutil import copyfile, move, rmtree
from distutils.dir_util import copy_tree  # for python 3.7

from . import pyinstaller_hidden_imports
from .log import getLogger

_suffix = '.pyd' if platform == 'win32' else '.so'
logger = getLogger(__name__)


def glob_copy(source: Path, target: Path, rglob: str = '*') -> None:
    if source.is_file():
        os.makedirs(target.parent, exist_ok=True)
        copyfile(source, target)
        return

    for x in source.glob(rglob):
        dist = target.joinpath(str(x)[len(str(source)) + 1:], '.')
        if x.is_file():
            os.makedirs(dist.parent, exist_ok=True)
            copyfile(x, dist)
        else:
            copy_tree(str(x), str(dist))


def add_hidden_imports(imports: Union[str, list], hiddenimports: list) -> None:
    if isinstance(imports, str) and str not in hiddenimports:
        hiddenimports.append(imports)
    elif isinstance(imports, list):
        for imp in imports:
            add_hidden_imports(imp, hiddenimports)


def parse_hidden_imports(sources: [str]) -> list:
    imports = []

    regex = re.compile(r"^\s*(?:from|import)\s+(\S+(?:\s*,\s*\w+)*)")
    for x in sources:
        with open(x) as src:
            for line in src.readlines():
                match = regex.search(line)
                if match and len(match.groups()) > 0:
                    if not match.group(1) in imports and not match.group(1).startswith('.'):
                        imports.append(match.group(1))

    return imports


def build(yaml_file='setup.yml'):
    base_dir = Path(os.path.dirname(__file__))

    # read config
    from .config import Config
    config = Config(yaml_file)

    # set build & dist dir
    build_path = config.build_root_path
    if build_path.exists():
        rmtree(build_path)
    build_path.mkdir()

    # run cython build
    from distutils.core import setup
    from Cython.Build import cythonize

    ext_module = cythonize(['%s%s%s' % (config.app_root, os.sep, item) for item in config.cython_sources],
                           exclude=config.cython_excludes, build_dir=str(config.build_temp_path),
                           **config.cython_options)

    script_args = ['build_ext', '-t', str('.'), '-b', str(config.build_cython_path)]
    setup(name=config.app_name, ext_modules=ext_module, script_args=script_args)

    if not config.build_cython_path.exists():
        raise BrokenPipeError('Unable build source code with cython.')

    if not config.is_debug:
        rmtree(config.build_temp_path)

    # copy init files to build dir if exclude
    for item in config.cython_excludes:
        if '__init__' in item:
            glob_copy(config.app_root, config.build_cython_path, '**/__init__.py')
            break

    # copy data files to build dir
    p_datas = []
    for source, target in config.pyinstaller_data_mapping:
        item = Path(str(target)[len(str(config.build_cython_path)) + 1:])
        p_datas.append((str(item), str(item) if source.is_dir() else str(item.parent)))
        glob_copy(source, target)

    # copy pyinstaller sources files to build dir
    for glob in config.pyinstaller_sources:
        glob_copy(config.app_root, config.build_cython_path, glob)

    # setup hidden import
    p_hiddenimports = config.pyinstaller_hiddenimports
    if config.pyinstaller_auto_import:
        sources = []
        for item in config.pyinstaller_sources:
            for file in config.app_root.glob(item):
                sources.append(str(file))

        for item in config.cython_excludes:
            if '__init__' in item:
                for file in config.app_root.glob('**/__init__.py'):
                    sources.append(str(file))

        c_includes = set()
        for item in config.cython_sources:
            for file in config.app_root.glob(item):
                c_includes.add(str(file))

        c_excludes = set()
        for item in config.cython_excludes:
            for file in config.app_root.glob(item):
                c_excludes.add(str(file))

        sources.extend([str(item) for item in (c_includes - c_excludes)])

        for item in config.build_cython_path.glob('**/__init__*[%s|%s]' % (_suffix, '.py')):
            item = str(item.parent)[len(str(config.build_cython_path)) + 1:]
            add_hidden_imports(".".join(Path(item).parts), p_hiddenimports)

        add_hidden_imports(parse_hidden_imports(sources), p_hiddenimports)
        p_hiddenimports = sorted(p_hiddenimports)
        logger.info('Set hiddenimports for pyinstaller: \n%s', '\n'.join(['- %s' % x for x in p_hiddenimports]))

    # setup binary
    p_binaries = config.pyinstaller_binaries
    if config.pyinstaller_cython_binaries:
        for item in config.build_cython_path.glob('**/*%s' % _suffix):
            binary = Path(str(item)[len(str(config.build_cython_path)) + 1:])
            p_binaries.append((str(binary), str(binary.parent)))

    logger.info('Set binaries for pyinstaller: \n%s', '\n'.join(['- %s' % x for x, _ in p_binaries]))

    # run pyinstaller build
    p_template = config.pyinstaller_template
    if p_template is None:
        p_template = Path(os.path.dirname(__file__)).joinpath('template.spec')
        copyfile(p_template, config.build_cython_path.joinpath(p_template.name))
    else:
        p_template = Path(p_template)
        if p_template.is_absolute():
            copyfile(p_template, config.build_cython_path.joinpath(p_template.name))
        else:
            copyfile(config.app_root.joinpath(p_template), config.build_cython_path.joinpath(p_template.name))

    p_template = str(p_template.name)
    logger.info('Use template spec file for pyinstaller: \n%s', ' - %s' % p_template)

    os.chdir(config.build_cython_path)

    with open(p_template, 'r+') as template:
        content = template.read()
        content = re.sub(r'\${app_name}', '"%s"' % config.app_name, content)
        content = re.sub(r'\${sources}', str(config.pyinstaller_sources), content)
        content = re.sub(r'\${datas}', str(p_datas), content)
        content = re.sub(r'\${binaries}', str(p_binaries), content)
        content = re.sub(r'\${hiddenimports}', str(p_hiddenimports), content)
        template.seek(0)
        template.write(content)
        template.truncate()

    from PyInstaller.building.build_main import main
    main(None, p_template, **{
        'distpath': str(config.target_path),
        'workpath': str(config.build_pyinstaller_path),
        'noconfirm': False,
    })

    # copy other distribution files to target dir
    # clean up build dir
    pass
