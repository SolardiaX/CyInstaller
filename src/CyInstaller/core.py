# -*- coding: utf-8 -*-

"""
    cyinstall.core
    ~~~~~~~~~~~~~~~~~~~
     The core methods of CyInstaller
    
    :copyright: (c) 2019 by DreamEx Works.
    :license: GPL-3.0, see LICENSE for more details.
"""

import json
import re
import os
import platform
import sys

from pathlib import Path
from typing import Union
from shutil import copyfile, rmtree, copytree
from PyInstaller.compat import PY3_BASE_MODULES

from .log import getLogger

_suffix = '.pyd' if platform == 'win32' else '.so'
_dotpath = Path('')

PY_BASE_MODULES = PY3_BASE_MODULES
logger = getLogger(__name__)


def glob_copy(source: Path, target: Path, rglob: str = '*') -> None:
    if source.is_file():
        os.makedirs(target.parent, exist_ok=True)
        copyfile(source, target)
        return

    for x in source.glob(rglob):
        dist = target.joinpath(str(x)[len(str(source)) + 1:], '')
        os.makedirs(dist.parent, exist_ok=True)
        if x.is_file():
            copyfile(x, dist)
        else:
            copytree(str(x), str(dist), dirs_exist_ok=True)


def add_hidden_imports(imports: Union[str, list], hiddenimports: list) -> None:
    if isinstance(imports, str) and str not in hiddenimports and str not in PY_BASE_MODULES:
        hiddenimports.append(imports)
    elif isinstance(imports, list):
        for imp in imports:
            add_hidden_imports(imp, hiddenimports)


def parse_hidden_imports(sources: [str]) -> [str]:
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


def find_packages(base: Path, sources: [str]) -> [str]:
    pkgs = []
    scaned = []

    def _detect_package(source: Union[str, Path]) -> str:
        m = Path(source).parent.parts
        for p in m:
            if p in pkgs:
                return '.'.join(m[m.index(p):])
        return '.'.join(m)

    for src in sources:
        src = Path(src)

        if src.exists() and src.name == '__init__.py':
            if src.parent not in scaned:
                pkgs.append(_detect_package(str(src)))
                scaned.append(src.parent)
            continue

        for item in base.glob(str(src)):
            if item.parent in scaned:
                continue

            init_file = item.parent.joinpath('__init__.py')
            if init_file.exists():
                pkgs.append(_detect_package(init_file))
            scaned.append(item.parent)

    pures = []
    for item in pkgs:
        pure = []
        part = Path(os.sep.join(item.split('.')))
        while part.stem != '':
            if not part.joinpath('__init__.py').exists():
                break
            pure.insert(0, part.stem)
            part = part.parent
        if len(pure) > 0:
            pures.append('.'.join(pure))

    return pures


def build(yaml_file='setup.yml'):
    root_dir = os.getcwd()
    sys.stdout = logger

    # read config
    logger.info('[STAGE 01] Read config from yaml file - [%s].', yaml_file)

    from .config import Config
    config = Config(yaml_file)

    # set build dir
    logger.info('[STAGE 02] Prepare building dir - [%s].', config.stage_path)

    build_path = config.stage_path
    if build_path.exists():
        rmtree(build_path)
    build_path.mkdir()

    # set dist dir
    dist_path = Path(root_dir).joinpath(config.dist)
    if dist_path.exists():
        rmtree(dist_path)

    # run cython build
    c_options = {
        'sources': config.compiles.raw_includes,
        'exclude': config.compiles.raw_excludes,
        'build_dir': str(config.stage_cython_temp_path),
        **config.stage_cython_options
    }

    logger.info('[STAGE 03] Execute cython compile with following options: \n %s', json.dumps(c_options, indent='  '))

    from distutils.core import setup
    from Cython.Build import cythonize

    ext_module = cythonize(config.compiles.raw_includes,
                           exclude=config.compiles.raw_excludes, build_dir=str(config.stage_cython_temp_path),
                           **config.stage_cython_options)

    script_args = ['build_ext', '-t', str('.'), '-b', str(config.stage_cython_path)]
    setup(name=config.name, ext_modules=ext_module, script_args=script_args)

    if not config.stage_cython_path.exists():
        raise BrokenPipeError('Unable build source code with cython.')

    if not config.stage_debug:
        rmtree(config.stage_cython_temp_path)

    # prepare soures for PyInstaller
    p_sources = {}

    for item in (config.packages.pures + [config.entrypoint]):
        target = config.stage_cython_path.joinpath(item.to.joinpath(item.source))
        p_sources.update({item.realsource: item.to.joinpath(item.source)})
        glob_copy(item.realsource, target)

    p_sources.pop(config.entrypoint.realsource)  # just copy entrypoint

    logger.loglist('[STAGE 04] Prepare package sources for PyInstaller ...',
                   list('%s->%s' % (k, v) for k, v in p_sources.items()))

    # prepare binaries for PyInstaller
    p_binaries = {}

    for item in config.binaries.pures:
        target = config.stage_cython_path.joinpath(item.to.joinpath(item.source))
        p_binaries.update({item.realsource: item.to.joinpath(item.source)})
        glob_copy(item.realsource, target)

    if config.cython_binaries:
        for item in config.stage_cython_path.rglob('*' + _suffix):
            f = item.relative_to(config.stage_cython_path)
            p_binaries.update({f: f})

    logger.loglist('[STAGE 05] Prepare binaries for PyInstaller ...',
                   list('%s->%s' % (k, v) for k, v in p_binaries.items()))

    # prepare datas for PyInstaller
    p_datas = {}

    for item in config.datas.pures:
        target = config.stage_cython_path.joinpath(item.to.joinpath(item.source))
        p_datas.update({item.realsource: item.to.joinpath(item.source)})
        glob_copy(item.realsource, target)

    logger.loglist('[STAGE 06] Prepare datas for PyInstaller ...', list('%s->%s' % (k, v) for k, v in p_datas.items()))

    # prepare hiddenimports for PyInstaller
    p_hiddenimports = config.hiddenimports
    if config.auto_hiddenimports:
        srcfiles = list(x.realsource for x in (config.compiles.pures + config.packages.pures))
        add_hidden_imports(parse_hidden_imports(srcfiles), p_hiddenimports)

    _app_packages = find_packages(config.root, [x.realsource for x in config.compiles.pures])
    add_hidden_imports(_app_packages, p_hiddenimports)

    logger.loglist('[STAGE 07] Prepare hiddenimports for PyInstaller ...', p_hiddenimports)

    # prepare PyInstaller spec file
    p_template = config.stage_pyinstaller_template
    if p_template is None:
        p_template = Path(os.path.dirname(__file__)).joinpath('template.spec')
    else:
        p_template = Path(p_template)
    copyfile(p_template, config.stage_cython_path.joinpath('setup.spec'))

    os.chdir(config.stage_cython_path)

    with open('setup.spec', 'r+') as template:
        content = template.read()
        content = re.sub(r'\${app_name}', '"%s"' % config.name, content)
        content = re.sub(r'\${sources}', str([config.entrypoint.source]), content)
        content = re.sub(r'\${hiddenimports}', str(p_hiddenimports), content)
        content = re.sub(r'\${datas}',
                         str([(str(x), str(x.parent if x.is_file() else x)) for x in p_datas.values()]), content)
        content = re.sub(r'\${binaries}',
                         str([(str(x), str(x.parent if x.is_file() else x)) for x in p_binaries.values()]), content)
        template.seek(0)
        template.write(content)
        template.truncate()

    logger.info('[STAGE 08] Generate template spec file for PyInstaller: [%s]',
                config.stage_cython_path.joinpath('setup.sepc'))

    # run PyInstaller with built arguments
    logger.info('[STAGE 09] Execute PyInstaller, detail options see the spec file.')

    from PyInstaller.building.build_main import main

    main(None, 'setup.spec', **{
        'distpath': str(dist_path),
        'workpath': str(Path(root_dir).joinpath(config.stage_pyinstaller_path)),
        'noconfirm': False,
    })

    # copy other distribution files to target dir
    os.chdir(root_dir)
    relates = {}

    for item in config.relates.pures:
        target = config.dist.joinpath(item.to.joinpath(item.source))
        relates.update({item.realsource: item.to.joinpath(item.source)})
        glob_copy(item.realsource, target)

    logger.loglist('[STAGE 10] Copy relates to dist...', list('%s->%s' % (k, v) for k, v in relates.items()))

    # clean up build dir
    if not config.stage_debug:
        rmtree(config.stage_cython_path)
        rmtree(config.stage_pyinstaller_path)

    logger.info('[FINISHED] CyInstaller execute finished, distribution files are in - [%s]', config.dist.absolute())

    # restore stdout
    sys.stdout = sys.__stdout__
