import json


class ConoHaAuthParams:
    def __init__(self, username, apikey, tenant_name, authurl):
        self.username = username
        self.key = apikey
        self.tenant_name = tenant_name
        self.authurl = authurl


class DbParams:
    def __init__(self, db_user, db_passwd, db_host, db_port, db_name):
        self.db_user = db_user
        self.db_passwd = db_passwd
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name


def load_params_for_backup_db_dump(jsonpath):
    with open(jsonpath, 'r') as f:
        json_data = json.load(f)
        conoha_params = ConoHaAuthParams(
            username=json_data.get('USERID'),
            apikey=json_data.get('APIKEY'),
            tenant_name=json_data.get('TENANTNAME'),
            authurl=json_data.get('AUTHURL')
        )
        app_params = {
            'backup_dest_container': json_data.get(
                'APP_BACKUP_DEST_CONTAINER_NAME'),
            'base_name': json_data.get(
                'APP_BACKUP_FILE_BASE_NAME'),
            'num_of_backup': json_data.get(
                'APP_BACKUP_NUM_OF_BACKUP'),
        }

        db_params = DbParams(
            db_user=json_data.get('DB_USER'),
            db_passwd=json_data.get('DB_PASSWD'),
            db_host=json_data.get('DB_HOST'),
            db_port=json_data.get('DB_PORT'),
            db_name=json_data.get('DB_NAME')
        )
    return conoha_params, app_params, db_params


def load_params_for_conoha_cli(jsonpath):
    with open(jsonpath, 'r') as f:
        json_data = json.load(f)
        conoha_params = ConoHaAuthParams(
            username=json_data.get('USERID'),
            apikey=json_data.get('APIKEY'),
            tenant_name=json_data.get('TENANTNAME'),
            authurl=json_data.get('AUTHURL')
        )
        app_params = {
            'download_path': json_data.get('APP_DLPATH')
        }
    return conoha_params, app_params
