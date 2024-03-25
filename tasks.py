#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from invoke import task

if os.name == "nt":  # Windows
    py = "python"
else:
    py = "python3"


@task
def coverage(c, details=False):
    c.run("coverage erase")
    c.run("coverage run -m pytest")
    if details:
        c.run("coverage html")
        c.run("coverage report", pty=True)


@task
def test(c):
    coverage(c)


@task
def lint(c):
    run_arg = "pylint -j 4 qt_range_slider/__init__.py example.py tests/"
    if os.name == "nt":  # Windows
        c.run(run_arg)
    else:
        c.run(run_arg, pty=True)
