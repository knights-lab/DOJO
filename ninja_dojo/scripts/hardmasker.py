#!/usr/bin/env python
import click
import os
import tempfile

from ninja_utils.scripts.soft_mask2hard_mask import soft_mask2hard_mask

from ninja_dojo.wrappers import dustmasker


@click.command()
@click.option('-i', '--input', type=click.STRING, default='-')
@click.option('-o', '--output', type=click.STRING, default='-')
def hardmasker(input, output):
    # Handle opening the file yourself. This makes clean-up
    # more complex as you must watch out for exceptions
    fd, path = tempfile.mkstemp()
    try:
        dustmasker(input, fd)
        print(soft_mask2hard_mask(fd, output))
    finally:
        os.remove(path)

if __name__ == '__main__':
    hardmasker()
