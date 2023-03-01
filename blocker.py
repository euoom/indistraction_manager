import json
import os
import subprocess
import sys
import time

import psutil
import win32api
import win32com.shell.shell as shell

with open('private/block_process.json') as f:
    block_list = json.load(f)


class ProcessBlocker:
    @staticmethod
    def _get_block_process():
        all_process = set(map(lambda x: x.name(), psutil.process_iter()))
        matched_list = []

        for block_process_name in block_list:
            for each_process in all_process:
                if block_process_name in each_process:
                    matched_list.append([block_process_name, each_process])
        return matched_list

    @staticmethod
    def block():
        matched_list = ProcessBlocker._get_block_process()
        while matched_list:
            name, matched_name = matched_list[0]
            os.system(f'taskkill /f /im "{matched_name}"')
            win32api.MessageBox(0, f"{name}을 하려고 했군! \n 일에 집중하라구!", '', 0x1000)
            matched_list = ProcessBlocker._get_block_process()

    @staticmethod
    def free():
        pass


class SiteBlocker:
    @staticmethod
    def _is_running():
        running_process = set()
        for proc in psutil.process_iter():
            running_process.add(proc.name())
        if 'BlockSite.exe' in running_process:
            return True
        return False

    @staticmethod
    def block():
        if SiteBlocker._is_running():
            return

        process = subprocess.Popen('cmd /k ', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
        process.stdin.write(b"cd %LOCALAPPDATA%\\BlockSite\n")
        process.stdin.write(b"BlockSite\n")
        # stdOutput, stdError = process.communicate()
        process.stdin.close()

    @staticmethod
    def free():
        if not SiteBlocker._is_running():
            return

        os.system('taskkill /f /im BlockSite.exe')


if __name__ == '__main__':
    ...
    # check_admin()

    ProcessBlocker.block()
    SiteBlocker.block()
