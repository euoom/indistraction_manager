import datetime
import logging
import multiprocessing
import os
import signal
import sys
import time
import typing

import psutil
import win32api

logging.basicConfig(filename='app.log', level=logging.INFO)


class ProcessBlocker:
    def __init__(self):
        self.state: typing.Optional[str] = None
        self.process: typing.Optional[multiprocessing.Process] = None

    @staticmethod
    def _block_process(block_names: list[str]):
        while True:
            all_process = list({x.name() for x in psutil.process_iter()})
            for block in block_names:
                for process in all_process:
                    if block in process:
                        os.system(f'taskkill /f /im "{process}"')
                        win32api.MessageBox(0, f"{block}을 하려고 했군! \n 본업에 집중하라구!", '', 0x1000)

            time.sleep(3)

    def block(self, process_names: list[str]):
        if self.state == 'block':
            return
        logging.info(f'[{datetime.datetime.now()}] {self.__class__.__name__}.block')
        self.state = 'block'

        self.process = multiprocessing.Process(target=self._block_process, kwargs={'block_names': process_names})
        self.process.start()

    def free(self):
        if self.process:
            logging.info(f'[{datetime.datetime.now()}] {self.__class__.__name__}.free')
            self.process.terminate()
            self.process.join()
            self.state = 'free'


class SiteBlocker:
    def __init__(self):
        self.state: typing.Optional[str] = None
        self.path_hosts = r'C:\Windows\System32\drivers\etc\hosts'
        self.path_original = r'assets\hosts.original'
        self.path_blocked = r'assets\hosts.blocked'

    @staticmethod
    def _read_file(full_path: str) -> list[str] | None:
        try:
            with open(full_path, 'r') as file:
                return file.readlines()
        except FileNotFoundError as e:
            logging.error(f'[{datetime.datetime.now()}] {full_path} 파일을 찾을 수 없습니다. \n{str(e)}')
        except IOError as e:
            logging.error(f'[{datetime.datetime.now()}] {full_path} 파일을 읽는 동안 오류가 발생했습니다. \n{str(e)}')
        finally:
            file.close()
        return None

    @staticmethod
    def _write_file(full_path: str, lines: list[str]) -> bool:
        try:
            with open(full_path, 'w') as file:
                file.writelines(lines)
                return True
        except FileNotFoundError as e:
            logging.error(f'[{datetime.datetime.now()}] {full_path} 파일을 찾을 수 없습니다. \n{str(e)}')
        except IOError as e:
            logging.error(f'[{datetime.datetime.now()}] {full_path} 파일을 읽는 동안 오류가 발생했습니다. \n{str(e)}')
        return False

    def block(self, sites: list[str]):
        if self.state == 'block':
            return
        logging.info(f'[{datetime.datetime.now()}] {self.__class__.__name__}.block')
        self.state = 'block'

        texts = self._read_file(self.path_original)
        texts.append('\n')
        if texts:
            for each in sites:
                line = f'127.0.0.1\t{each}\n'
                texts.append(line)

        self._write_file(self.path_blocked, texts)
        self._write_file(self.path_hosts, texts)

    def free(self):
        if self.state == 'free':
            return
        logging.info(f'[{datetime.datetime.now()}] {self.__class__.__name__}.free')
        self.state = 'free'

        texts = self._read_file(self.path_original)
        self._write_file(self.path_hosts, texts)


def exit_gracefully(signal, frame):
    ProcessBlocker().free()
    SiteBlocker().free()

    logging.info(f"[{datetime.datetime.now()}] 프로그램이 종료되었습니다.")
    sys.exit(0)


signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

if __name__ == '__main__':
    ...
    # check_admin()

    process_blocker = ProcessBlocker()
    process_blocker.block([
        'EZ2ON',
        'DJMAX',
        'Steam',
        'StarCraft',
        'Battle.net'
    ])

    site_blocker = SiteBlocker()
    site_blocker.block([
        'www.youtube.com',
        'www.facebook.com',
        'comic.naver.com',
        'game.naver.com',
        'www.op.gg',
    ])
