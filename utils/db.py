from pathlib import Path
from abc import abstractmethod
from os import PathLike
from utils.params import DbParams
from zipfile import ZipFile, ZIP_DEFLATED
import shutil
import subprocess
# import pymysql


class DbDumpBase:
    def __init__(self, dbparams: DbParams):
        self.dbparams = dbparams

    @abstractmethod
    def create_dump_file(self, workingdirypath: PathLike, filepath: PathLike) -> bool:
        """create and get dump file path
        Returns:
            PathLike: SQL dump file PathLike object
        """
        raise NotImplementedError()


class MySqlDumpCli(DbDumpBase):
    def create_dump_file(self, workingdirypath: PathLike, filepath: PathLike) -> bool:
        if not isinstance(filepath, Path):
            return False
        ext = filepath.suffix
        if ext not in ['.sql', '.txt', '.dump', '.zip']:
            return False
        if not isinstance(workingdirypath, Path) or not workingdirypath.is_dir:
            return False

        try:
            tmpfilepath = workingdirypath.joinpath(filepath.stem + '.sql')
            cmd = 'mysqldump -h {} -P {} -u {} -p{} --skip-comments {} > {}'.format(
                self.dbparams.db_host,
                self.dbparams.db_port,
                self.dbparams.db_user,
                self.dbparams.db_passwd,
                self.dbparams.db_name,
                str(tmpfilepath.absolute())
            )
            subprocess.check_call(cmd, shell=True)
            if ext == '.zip':
                with ZipFile(filepath, 'w', ZIP_DEFLATED) as outfile:
                    outfile.write(tmpfilepath, tmpfilepath.name)
                tmpfilepath.unlink()
            else:
                shutil.move(str(tmpfilepath.absolute()),
                            str(filepath.absolute()))
        except Exception:
            return False
        return True


class MySqlDumpPy(DbDumpBase):
    pass


class Sqlite3Dump(DbDumpBase):
    pass
