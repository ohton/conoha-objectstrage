#!/usr/bin/env python

from utils.conoha import ConoHaSwift
from utils.params import load_params_for_conoha_cli
from pathlib import Path
import click


@click.group(invoke_without_command=False)
@click.pass_context
def cli(ctx):
    # 設定ファイルからパラメータ取得
    conoha_params, app_params = load_params_for_conoha_cli(
        Path(__file__).parent.joinpath('settings.json')
    )
    ctx.obj['conoha_params'] = conoha_params
    ctx.obj['app_params'] = app_params


@cli.command()
@click.argument('container_name')
@click.argument('obj_name')
@click.pass_context
def download(ctx, container_name, obj_name):
    openswift = ConoHaSwift(ctx.obj['conoha_params'])
    download_path = Path(ctx.obj['app_params']['download_path'])
    if not download_path.is_absolute():
        download_path = Path(__file__).absolute().parent.joinpath(
            ctx.obj['app_params']['download_path'])
    ret = openswift.download_object(
        container_name, obj_name, download_path)
    if ret is False:
        print('[download_object] failure')


@cli.command()
@click.argument('container_name')
@click.argument('file_paths', nargs=-1)
@click.pass_context
def upload(ctx, container_name, file_paths):
    openswift = ConoHaSwift(ctx.obj['conoha_params'])
    for file_path in file_paths:
        ret = openswift.put_object(
            container_name, file_path)
        if ret is False:
            print('[put_object] failure')


@cli.command()
@click.argument('container_name')
@click.argument('obj_names', nargs=-1)
@click.pass_context
def delete(ctx, container_name, obj_names):
    openswift = ConoHaSwift(ctx.obj['conoha_params'])
    for obj_name in obj_names:
        ret = openswift.delete_object(
            container_name, obj_name)
        if ret is False:
            print('[delete_object] failure')


@ cli.command()
@ click.argument('container_name', required=False, default=False)
@click.option('--limit', nargs=1, type=int, help='objects limit')
@click.option('--single', '-1', is_flag=True, help='single line')
@ click.pass_context
def ls(ctx, container_name, limit, single):
    openswift = ConoHaSwift(ctx.obj['conoha_params'])
    if container_name:
        openswift.print_objects(
            container_name=container_name, limit=limit, single=single)
    else:
        openswift.print_containers()


@ cli.command()
@ click.argument('container_name')
@ click.pass_context
def create_container(ctx, container_name):
    openswift = ConoHaSwift(ctx.obj['conoha_params'])
    ret = openswift.create_container(container_name)
    if ret is False:
        print('[create_container] failure')


@ cli.command()
@ click.argument('container_name')
@click.option('--force', '-f', is_flag=True, help='force delete')
@ click.pass_context
def delete_container(ctx, container_name, force):
    openswift = ConoHaSwift(ctx.obj['conoha_params'])
    if force:
        objs = []
        while(isinstance(objs, list)):
            prv_objs = objs
            objs = openswift.get_objects(container_name, limit=30)
            if isinstance(objs, list):
                for obj in objs:
                    ret = openswift.delete_object(container_name, obj['name'])
                    if ret is False:
                        print('[delete_object] failure')
                if len(objs) == 0:
                    break
            if prv_objs == objs:
                break
    ret = openswift.delete_container(container_name)
    if ret is False:
        print('[delete_container] failure')


if __name__ == '__main__':
    cli(obj={})
