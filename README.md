# conoha-objectstrage

pythonのOpenStack Swiftクライアントライブラリを使用してconohaオブジェクトストレージを操作するcliスクリプトと
DB(MySQL)ダンプの指定世代分バックアップをconohaオブジェクトストレージに保存するスクリプト。

## setup

### 1a. pipenv + pyenv

```
pipenv sync
```

### 1b. direnv + pipenv + pyenv

```
# cp dotenv_sample .env
# vim .env
direnv allow
```

### 1c. requirements.txt

```
pip install -r requirements.txt
```

### 2. settings

```
cp settings.json.org settings.json
```

```settings.json
{
    "USERID": "",
    "APIKEY": "",
    "TENANTNAME": "",
    "AUTHURL": "",
    "APP_DLPATH": "./dlfiles",
    "APP_BACKUP_DEST_CONTAINER_NAME": "",
    "APP_BACKUP_FILE_BASE_NAME": "db_name",
    "APP_BACKUP_NUM_OF_BACKUP": "100",
    "DB_USER": "",
    "DB_PASSWD": "",
    "DB_HOST": "127.0.0.1",
    "DB_PORT": "3306",
    "DB_NAME": ""
}
```

## scripts

### conoha.py

```
$ ./conoha.py --help
Usage: conoha.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create-container
  delete
  delete-container
  download
  ls
  upload

$ ./conoha.py create-container --help
Usage: conoha.py create-container CONTAINER_NAME

$ ./conoha.py delete --help
Usage: conoha.py delete CONTAINER_NAME [OBJ_NAMES]...

$ ./conoha.py delete-container --help
Usage: conoha.py delete-container [OPTIONS] CONTAINER_NAME

Options:
  -f, --force  force delete

$ ./conoha.py download --help
Usage: conoha.py download CONTAINER_NAME OBJ_NAME

$ ./conoha.py ls --help
Usage: conoha.py ls [OPTIONS] [CONTAINER_NAME]

Options:
  --limit INTEGER  objects limit
  -1, --single     single line

$ ./conoha.py upload --help
Usage: conoha.py upload CONTAINER_NAME [FILE_PATHS]...
```

### backup_db_dump.py

```
$ ./backup_db_dump.py
```

## swift command auth params

- .env

```
export OS_USERNAME=''
export OS_PASSWORD=''
export OS_TENANT_NAME=''
export OS_AUTH_URL=''
```

- swift command

```
swift stat
# pipenv run conoha stat
swift list
# pipenv run conoha list
```

---

## OpenStack Swift GUI mount tools

- [Cyberduck](https://cyberduck.io): OSS, donation
- [ExpanDrive](https://www.expandrive.com): $49.95 (2020/08/25)
