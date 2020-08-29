# -*- coding: utf-8 -*-
import click
from languageflow.download import download_component


@click.group()
def main(args=None):
    """Console script for languageflow"""
    pass


@main.command()
@click.argument('component')
@click.option('-f', '--force', is_flag=True)
def download(component, force):
    download_component(component, force)


if __name__ == "__main__":
    main()
