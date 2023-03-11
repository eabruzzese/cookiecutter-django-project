import os
import sys

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "{{ cookiecutter.package_name }}"
copyright = "2022, {{ cookiecutter.author_name }}"
author = "{{ cookiecutter.author_name }}"
release = "0.1.0"

# Configure the PYTHONPATH to include our package.
sys.path.insert(0, os.path.abspath(".."))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # Add support for parsing .md files as Markdown.
    "myst_parser",
    # Generate API docs from docstrings, with support for the Google and NumPy
    # docstring styles via Napoleon.
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    # Collect documentation coverage statistics.
    "sphinx.ext.coverage",
    # Support the official ReadTheDocs.io theme.
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
