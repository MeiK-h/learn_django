import os
import re
from shutil import rmtree

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Jplag(object):
    file_name = 'jplag.jar'
    jplag_cmd = 'java -jar <file_name> -l <language> -m <percent> -r <result_dir> -s <submit_dir>'
    code_path = 'jplag/jplag/codes/'
    result_path = 'jplag/jplag/result/'

    def __init__(self, checker_id):
        self.run_cmd = self.jplag_cmd
        self.dir_path = None
        self.checker_id = str(checker_id)

    def make_run_cmd(self, language, percent='80%', result_dir=None, submit_dir=None):
        if result_dir is None:
            result_dir = os.path.join(self.result_path, self.checker_id)
        if submit_dir is None:
            submit_dir = os.path.join(self.code_path, self.checker_id)
        self.run_cmd = self.jplag_cmd
        self.run_cmd = self.run_cmd.replace('<file_name>', self.file_name)
        self.run_cmd = self.run_cmd.replace('<language>', language)
        self.run_cmd = self.run_cmd.replace('<percent>', percent)
        self.run_cmd = self.run_cmd.replace('<result_dir>', result_dir)
        self.run_cmd = self.run_cmd.replace('<submit_dir>', submit_dir)
        return self.run_cmd

    def save_code(self, file_name, code):
        self.dir_path = os.path.join(os.path.abspath(
            './'), self.code_path, str(self.checker_id))
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        with open(os.path.join(self.dir_path, str(file_name)), 'w') as fr:
            fr.write(str(code))

    def run_jplag(self):
        assert self.run_cmd != self.jplag_cmd
        jplag = os.popen(self.run_cmd)
        rsts = jplag.readlines()
        rst = ''.join(rsts[0:7])
        return rst

    def __del__(self):
        if self.dir_path and os.path.exists(self.dir_path):
            rmtree(self.dir_path)


class Checker(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    language = models.CharField(max_length=64)
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)  # 状态：0：未开始、1：进行中、2：结束
    message = models.CharField(max_length=1000)


class Code(models.Model):
    checker = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=64, validators=[check_name])
    code = models.FileField(upload_to='codes/')


def check_name(name):
    pattern = re.compile(u'^[.0-9a-zA-Z\u4e00-\u9fa5]+$')
    match = pattern.search(name)
    if not match:
        raise ValidationError(
            _('%(name) 不合法'),
            params={'name': name},
        )
