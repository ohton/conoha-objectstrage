from keystoneclient import session
from keystoneclient.auth.identity import v2
from swiftclient import client
from pathlib import Path
from itertools import chain
from typing import List, Union
from utils.params import ConoHaAuthParams


class ConoHaSwift:
    """

    # refs: https://docs.ceph.com/docs/jewel/radosgw/swift/python/
    """

    def __init__(self, conohaparams: ConoHaAuthParams):
        self.conohaparams = conohaparams

    def _get_openswift_connection(self):
        auth = v2.Password(
            auth_url=self.conohaparams.authurl,
            username=self.conohaparams.username,
            password=self.conohaparams.key,
            tenant_name=self.conohaparams.tenant_name)
        ss = session.Session(auth=auth)
        return client.Connection(session=ss)

    def get_containers(self) -> Union[List[dict], bool]:
        try:
            resp_headers, containers = self._get_openswift_connection().get_account()
        except session.exceptions.Unauthorized:
            return False
        except client.ClientException:
            return False
        if containers:
            return containers
        return []

    def create_container(self, container_name: str) -> bool:
        try:
            self._get_openswift_connection().put_container(
                container_name)
        except session.exceptions.Unauthorized:
            return False
        except client.ClientException:
            return False
        return True

    def delete_container(self, container_name: str) -> bool:
        try:
            self._get_openswift_connection().delete_container(
                container_name)
        except session.exceptions.Unauthorized:
            return False
        except client.ClientException:
            return False
        return True

    def print_containers(
            self, sort_target: str = 'name', reverse: bool = False) -> List[dict]:
        containers = self.get_containers()
        if isinstance(containers, list):
            containers = sorted(
                containers, key=lambda x: x[sort_target], reverse=reverse)
            ret = '\n'.join(
                chain.from_iterable(
                    zip(
                        map(lambda x: f'- container: {x["name"]}', containers),
                        map(lambda x: f'   - count: {x["count"]}', containers),
                        map(lambda x: f'   - bytes: {x["bytes"]}', containers)
                    )),
            )
            print(ret)
            return containers
        else:
            print('empty or failure')
            return []

    def get_objects(self, container_name: str, limit: int = None) -> Union[List[dict], bool]:
        try:
            resp_headers, objects = self._get_openswift_connection().get_container(
                container_name, limit=limit)
        except session.exceptions.Unauthorized:
            return False
        except client.ClientException:
            return False
        if objects:
            return objects
        return []

    def print_objects(
            self, container_name: str, limit: int = None,
            single: bool = False,
            sort_target: str = 'name', reverse: bool = False) -> List[dict]:
        objs = self.get_objects(container_name, limit=limit)
        if isinstance(objs, list):
            objs = sorted(
                objs, key=lambda x: x[sort_target], reverse=reverse)
            if single:
                ret = ' '.join([x['name'] for x in objs])
            else:
                ret = '\n'.join(
                    chain.from_iterable(
                        zip(
                            map(lambda x: f'- object: {x["name"]}', objs),
                            map(lambda x: f'   - bytes: {x["bytes"]}', objs),
                            map(
                                lambda x: f'   - last_modified: {x["last_modified"]}', objs),
                            map(
                                lambda x: f'   - content_type: {x["content_type"]}', objs),
                        )),
                )
            print(ret)
            return objs
        else:
            print('empty or failure')
            return []

    def download_object(self, container_name: str, object_name: str,
                        dirpath: Union[str, Path] = ''):
        dirpath = Path(dirpath)
        try:
            resp_headers, obj_contents = self._get_openswift_connection(
            ).get_object(container_name, object_name)
            with open(dirpath.joinpath(object_name), 'wb') as f:
                f.write(obj_contents)
        except session.exceptions.Unauthorized:
            return False
        except client.ClientException:
            return False
        except FileNotFoundError:
            return False
        return resp_headers

    def put_object(self, container_name: str, filepath: Union[str, Path]):
        try:
            filepath = Path(filepath)
            if filepath.exists():
                with open(filepath, 'rb') as f:
                    self._get_openswift_connection(
                    ).put_object(
                        container=container_name,
                        obj=filepath.name,
                        contents=f)
        except session.exceptions.Unauthorized:
            return False
        except client.ClientException:
            return False
        except FileNotFoundError:
            return False
        return True

    def delete_object(self, container_name: str, object_name: str):
        try:
            self._get_openswift_connection(
            ).delete_object(
                container=container_name,
                obj=object_name)
        except session.exceptions.Unauthorized:
            return False
        except client.ClientException:
            return False
        except FileNotFoundError:
            return False
        return True
