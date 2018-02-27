import os
import re
from shutil import rmtree, copy

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

class Jplag(object):
    file_name = 'jplag.jar'
    jplag_cmd = 'java -jar <file_name> -l <language> -m <percent> -r <result_dir> -s <code_dir>'
    base_code_path = 'jplag/uploads/tmp/'
    base_result_path = 'jplag/uploads/result/'

    language_list = ['java17', 'java15', 'java15dm', 'java12',
                     'java11', 'python3', 'c/c++', 'c#', 'char', 'text', 'scheme']

    def __init__(self, checker_id):
        self.run_cmd = self.jplag_cmd
        self.code_path = os.path.join(self.base_code_path, str(checker_id))
        self.result_path = os.path.join(self.base_result_path, str(checker_id))
        self.checker_id = str(checker_id)
        if os.path.exists(self.code_path):
            rmtree(self.code_path)
        os.mkdir(self.code_path)

    def make_run_cmd(self, language, percent='80%'):
        assert language in self.language_list
        self.run_cmd = self.jplag_cmd
        self.run_cmd = self.run_cmd.replace('<file_name>', self.file_name)
        self.run_cmd = self.run_cmd.replace('<language>', language)
        self.run_cmd = self.run_cmd.replace('<percent>', percent)
        self.run_cmd = self.run_cmd.replace('<result_dir>', self.result_path)
        self.run_cmd = self.run_cmd.replace('<code_dir>', self.code_path)
        return self.run_cmd

    def copy_file_to_jplag_tmp(self, filepath):
        copy(filepath, self.code_path)

    def run(self):
        assert self.run_cmd != self.jplag_cmd
        jplag = os.popen(self.run_cmd)
        rsts = jplag.readlines()
        rst = ''.join(rsts[0:7])
        rst += '\n下略 {} 行\n'.format(len(rsts) - 7)
        state = rsts[-2]
        if state.startswith('Error'):
            return {'state': False, 'message': rst}
        return {'state': True, 'message': rst}

    def __del__(self):
        if self.code_path and os.path.exists(self.code_path):
            rmtree(self.code_path)


class Checker(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Code(models.Model):
    checker = models.ForeignKey(Checker, on_delete=models.CASCADE)
    code = models.FileField(upload_to='code/')
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)

    access_type = ['c', 'cpp', 'cc', 'java', 'cs', 'py', 'txt']

    def __str__(self):
        return self.code.name
