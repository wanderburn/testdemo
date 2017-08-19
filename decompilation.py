#coding=utf-8
import xml.dom.minidom
import os

path = 'E:\Program Files\Python\chanel\install_files'
L = ['3gqq', 'anzhi', 'feidee']


def de_compilation():
    """用apktool工具反编译apk"""
    for root, dirs, files in os.walk(path):    #root代表当前的路径，dirs代表路径下的文件夹，files代表当前路径的文件
        for filename in files:
            file_name = os.path.join(root, filename)
            if file_name.endswith(".apk"):
                apk_out_path = file_name.split('.apk')[0]
                apk_out_path_exists = os.path.exists(apk_out_path)
                if not apk_out_path_exists:
                    os.makedirs(apk_out_path)
                file_name = "\"" + file_name + "\""
                apk_out_path = "\"" + apk_out_path + "\""
                apk_tool_command = 'apktool d -f ' + file_name + ' -o ' + apk_out_path
                os.system(apk_tool_command)


def check_chanel_package():
    """去反编译的apk文件夹寻找channel字段"""
    i = 0
    files = os.listdir(path)
    for t in files:
        apk_out_path = os.path.join(path, t)
        if not apk_out_path.endswith(".apk"):
            chanel_path = apk_out_path + '/' + 'AndroidManifest.xml'
            dom = xml.dom.minidom.parse(chanel_path)
            root = dom.documentElement
            meta_node = root.getElementsByTagName("meta-data")
            chanel_info = meta_node[10].getAttribute('android:value')
            if chanel_info == L[i]:
                print ('%s package is right' % L[i])
            elif chanel_info == 'product':
                new_chanel_path = apk_out_path + '\original\META-INF'
                new_chanel_info = os.listdir(new_chanel_path)
                new_chanel_info = new_chanel_info[0].split('_')[-1]
                if new_chanel_info == L[i]:
                    print ('%s package is right' % L[i])
                else:
                    print ('%s package is wrong' % L[i])
                    return False
            else:
                print ('%s package is wrong' % L[i])
                return False
            i += 1

    return True


if __name__ == '__main__':
    de_compilation()
    check_chanel_package()