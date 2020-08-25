#!/usr/bin/env python

from utils.conoha import ConoHaSwift
from utils.params import load_params_for_backup_db_dump
from utils.db import DbDumpBase
from utils.db import MySqlDumpCli
from datetime import datetime
from pathlib import Path


def _main():

    # 設定ファイルからパラメータ取得
    conoha_params, app_params, db_params = load_params_for_backup_db_dump(
        Path(__file__).parent.joinpath('settings.json')
    )

    db: DbDumpBase = MySqlDumpCli(db_params)
    base_name = app_params['base_name']
    name_suffix = datetime.now().strftime('_%Y%m%d_%H%M%S')
    outfilepath = Path(__file__).parent.joinpath(
        'work', f'{base_name}{name_suffix}.zip')
    container = app_params['backup_dest_container']
    num_of_backup = app_params['num_of_backup']
    ret = db.create_dump_file(
        Path(__file__).parent.joinpath('work'), outfilepath)
    if ret and container:
        openswift = ConoHaSwift(conoha_params)
        openswift.put_object(container, outfilepath)
        print(f'"{outfilepath}" saved to "{container}: {outfilepath.name}"')
        if isinstance(num_of_backup, str) and num_of_backup.isdigit():
            num_of_backup = int(num_of_backup)
            objs = openswift.get_objects(container)
            if isinstance(objs, list):
                objs = sorted(
                    objs, key=lambda x: x['last_modified'], reverse=True)
                for obj in [x for x in objs if x['name'].startswith(base_name)][num_of_backup:]:
                    obj_name = obj['name']
                    openswift.delete_object(container, obj_name)
                    print(f'{obj_name} has deleted.')
        outfilepath.unlink()


if __name__ == '__main__':
    _main()
