import re

# Project --------------------------------------------------------------
with open("../src/CyInstaller/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

project = "CyInstaller"
copyright = "2020 SolardiaX"
author = "SolardiaX"
release = version

# General --------------------------------------------------------------

master_doc = "index"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.log_cabinet",
    "sphinx_material",
    "sphinx_issues",
]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}
issues_github_path = "solardiax/cyinstaller"

# HTML -----------------------------------------------------------------
templates_path = ["_templates"]

html_sidebars = {
    "**": ["globaltoc.html", "localtoc.html", "searchbox.html"]
}

html_theme = 'sphinx_material'
html_title = 'CyInstaller'
html_theme_options = {
    'nav_title': 'CyInstaller',
    'google_analytics_account': '',
    'base_url': 'https://solardiax.github.io/cyinstaller',
    'color_primary': 'indigo',
    'color_accent': 'indigo',
    'repo_url': 'https://github.com/solardiax/cyinstaller/',
    'repo_name': 'solardiax/CyInstaller',
    'globaltoc_depth': 0,
    'globaltoc_collapse': False,
    'globaltoc_includehidden': True,
    'version_dropdown': False,
    'master_doc': False,
    'nav_links': [
        {'href': 'index', 'title': 'About', 'internal': True},
        {'href': 'configration', 'title': 'Configration', 'internal': True},
        {'href': 'portablesource', 'title': 'PortableSource', 'internal': True},
        {'href': 'modules', 'title': 'Modules', 'internal': True},
    ]
}

html_logo = '_static/images/favicon.png'
html_show_sourcelink = False

html_static_path = ['_static']
html_css_files = [
    'stylesheets/custom.css',
]
