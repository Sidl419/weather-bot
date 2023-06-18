#!usr/bin/env python3
"""Project tasks."""

DOIT_CONFIG = {'default_tasks': ['html']}


def task_html():
    """Build documentation-html for project."""
    return {
        'actions': ['sphinx-build -M html ./doc/ ./doc/_build']
    }

def task_gitclean():
    """Clean untracked files."""
    return {
            'actions': ['git clean -xdf'],
    }