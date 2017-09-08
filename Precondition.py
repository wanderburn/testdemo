# coding:utf-8
import sys
import os
import re
import subprocess
import threading
import random
import ConfigParser
import paramiko
import time
import logging
reload(sys)
sys.setdefaultencoding('utf-8')
conf = ConfigParser.ConfigParser()
config_file_path = os.getcwd() + os.sep + 'app_test.ini'
conf.read(config_file_path)
host = conf.get("conf", "host")
port = int(conf.get("conf", "port"))
name = conf.get("conf", "name")
password = conf.get("conf", "password")


def input_version_number():
    # Determine whether the input version number format is correct
    global a
    a = raw_input("Please input version number:")
    if not re.findall(r"^V?v?\d(\.\d+)+$", a):
        self._logger.debug("The version number you entered does not conform to the specification,"
                           " for example:v7.7.1")

    # If the input version number begins with a capital V/V, the first letter is removed
    if (a.startswith('v')) or (a.startswith('V')):
        a = a[1:]
        return a
    else:
        return a


def get_devices_id():
    command = 'adb devices'
    s = []
    global j
    j = []
    value = None
    for loop in range(10):
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        value = p.communicate()[0]
        y = value.split('\r\n')
        if y[1] == '':
            logger.debug("No device connected to the computer,please check it")
            break
        elif "daemon not running" not in value.strip() and not value.strip() == "":
            logger.debug("adb startup successfully")
            break
        time.sleep(2)
    device_id = value.split('\r\n')
    for i in device_id:
        if i != '':
            s.append(i)
    for m in s:
        m = m.split('\t')
        if len(m) == 2:
            j.append(m[0])
    return j


def create_logger(filename):
    """
    Create a logger named specified name with the level set in config file.
    name
      string, name for logger

    return the logger instance
    """
    logger = logging.getLogger(filename)
    logger.setLevel("DEBUG")
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d: [%(levelname)s] [%(name)s] [%(funcName)s] [%(lineno)d] %(message)s',
        '%y%m%d %H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def create_folders(device_id):
    path = os.getcwd() + os.sep + str(device_id)
    folder_path = os.path.exists(path)
    if not folder_path:
        os.makedirs(path)
        logger.debug("Create %s folders successfully'" % path)
    else:
        logger.debug("%s folders already exist" % path)
    return True


logger = create_logger("MAIN")


class MySFTP(object):

    def __init__(self, host, port, username, password):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._ssh_fd = None
        self._sftp_fd = None

    def _connect(self):
        """连接服务器
        """
        ssh_fd = None
        try:
            ssh_fd = paramiko.SSHClient()
            ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_fd.connect(self._host, self._port, self._username, self._password)
        except Exception, e:
            logger.debug('ssh %s@%s: %s' % (self._username, self._host, e))
            exit()

        self._ssh_fd = ssh_fd

    def open(self):
        """打开服务
        """
        self._connect()
        return self._ssh_fd.open_sftp()

    def get(self, ftp_handler, remote_file_path, local_file_path):
        """文件下载
        """
        ftp_handler.get(remote_file_path, local_file_path)

    def close(self, ftp_handler):
        """关闭连接
        """
        ftp_handler.close()


def download_files(device_id):
    my_ftp = MySFTP(host, port, name, password)  # 实例化ftp连接的类
    ftp_handler = my_ftp.open()
    send_folders_path = "/data/app_test/MyMoneySms/发版/"
    send_folders = ftp_handler.listdir(send_folders_path)  # 遍历共享服务器的发版的所有文件
    for folder in send_folders:
        if folder[1:] == a:
            remote_path = u"/data/app_test/MyMoneySms/发版/" + folder + '/' + 'market'  # 找到我们需要的渠道包的路径
            local_path = os.getcwd() + os.sep + device_id
            remote_files = ftp_handler.listdir(remote_path)  # 遍历渠道包路径下的所有文件
            for k in remote_files:
                if k.split('_')[0] == '.':
                    remote_files.remove(k)
            random_remote_files = random.sample(remote_files, 3)  # 随机抽取3个渠道包
            for filename in remote_files:
                portion = os.path.splitext(filename)
                if filename in random_remote_files and portion[1] == '.apk':  # 抽样下载3个渠道包
                    file_path = remote_path + '/' + filename
                    local_file_path = local_path + '/' + filename
                    my_ftp.get(ftp_handler, file_path, local_file_path)
    ftp_handler.close()
    logger.debug("Success download the file from the Shared server")


def prediction(device_id):
    create_folders(device_id)
    download_files(device_id)


def thread_prediction():
    input_version_number()
    get_devices_id()
    threads_2 = []
    devices_id_numbers = len(j)
    for i in range(devices_id_numbers):
        m = threading.Thread(target=prediction, args=(j[i],))
        threads_2.append(m)
    for t in threads_2:
        t.start()
        time.sleep(0.5)


if __name__ == '__main__':
    thread_prediction()
