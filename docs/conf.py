# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

sys.path.insert(0, os.path.abspath("../"))

project = 'AISploit'
copyright = '2024, hupe1980'
author = 'hupe1980'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_mdinclude',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autodoc_default_options = {
    "show-inheritance": True,
    "members": True,
    "undoc-members": True,
    "imported-members": True,
    "no-value": True,
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
html_theme_options = {
    'description': 'Mastering the New Threatscape with AI-Driven Precision.',
    'body_max_width': 'auto',
    "fixed_sidebar": True,
    "badge_branch": "main",
    "github_button": False,
    "github_user": "hupe1980",
    "github_repo": "aisploit",
    "show_powered_by": False,
    "sidebar_collapse": False,
}

html_sidebars = {
    "**": [
        "about.html",
        "badges.html",
        "navigation.html",
        "relations.html",
        "searchbox.html",
        "disclaimer.html",
    ],
}

