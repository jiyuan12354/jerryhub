#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# horizon工程目录
HORIZON_HOME = "/home/dengjy/horizon"
# runserver时使用的端口
SERVER_PORT = "8093"
# runserver时是否启用: ip netns exec haproxy ...
IS_NEED_IP_NETNS = True

# 常量
PUBLIC_LOCAL_SETTINGS = "/usr/share/openstack-dashboard/openstack_dashboard/local/local_settings.conf"
HORIZON_LOCAL_SETTINGS = "{}/openstack_dashboard/local/local_settings.conf".format(HORIZON_HOME)
HORIZON_SETTINGS = "{}/openstack_dashboard/settings.py".format(HORIZON_HOME)
HORIZON_SCRIPTS = "{}/horizon/templates/horizon/_scripts.html".format(HORIZON_HOME)
HORIZON_CONF = "{}/horizon/templates/horizon/_conf.html".format(HORIZON_HOME)


def system(cmd):
    if os.system(cmd) != 0:
        sys.exit(1)


def replace_file_str(filename, old_str, new_str):
    data = ""
    is_exist = False
    with open(filename, mode="r") as f:
        for line in f:
            if old_str in line:
                is_exist = True
                line = line.replace(old_str, new_str)
            data += line
    if is_exist:
        with open(filename, mode="w") as f:
            f.write(data)


def compile_proj():
    os.chdir(HORIZON_HOME + "/horizon")
    system("django-admin compilemessages")
    os.chdir(HORIZON_HOME + "/openstack_dashboard")
    system("django-admin compilemessages")
    os.chdir(HORIZON_HOME)
    system("python manage.py compilejsi18n")


def compress_proj():
    os.chdir(HORIZON_HOME)
    system("python manage.py compress")


def run_proj(nohup):
    os.chdir(HORIZON_HOME)
    if IS_NEED_IP_NETNS:
        command = "ip netns exec haproxy python manage.py runserver 0:{}".format(SERVER_PORT)
    else:
        command = "python manage.py runserver 0:{}".format(SERVER_PORT)
    if nohup:
        command = "nohup {} > {}_log 2>&1 &".format(command, HORIZON_HOME)
    system(command)


def set_sso_login(flag):
    if flag:
        value = "True"
    else:
        value = "False"
    system("openstack-config --set {} ccas sso_login {}".format(HORIZON_LOCAL_SETTINGS, value))
    replace_file_str(
        HORIZON_SETTINGS,
        "HORIZON_CONFIG['captcha_disabled'] = False",
        "HORIZON_CONFIG['captcha_disabled'] = True"
    )


def set_compress(flag):
    old_str1 = "{% compress js %}"
    old_str2 = "{% endcompress %}"
    new_str1 = "{#% compress js %#}"
    new_str2 = "{#% endcompress %#}"
    if flag:
        old_str1 = "{#% compress js %#}"
        old_str2 = "{#% endcompress %#}"
        new_str1 = "{% compress js %}"
        new_str2 = "{% endcompress %}"
    replace_file_str(HORIZON_SCRIPTS, old_str1, new_str1)
    replace_file_str(HORIZON_SCRIPTS, old_str2, new_str2)
    replace_file_str(HORIZON_CONF, old_str1, new_str1)
    replace_file_str(HORIZON_CONF, old_str2, new_str2)


def stop_runserver():
    show_cmd = "ps aux | grep 'runserver 0:" + SERVER_PORT + "' | grep -v grep | awk '{print $2}'"
    # print("Done: {}".format(show_cmd))
    # noinspection PyBroadException
    try:
        process_ids = os.popen(show_cmd).read().split("\n")
        for process_id in process_ids:
            if process_id != "":
                kill_cmd = "kill -9 {}".format(process_id)
                print("Done: {}".format(kill_cmd))
                system(kill_cmd)
    except Exception:
        print("Error: Kill Process Fail!")


if len(sys.argv) == 1:
    print("    1.cpl                     Compile, compress and run server")
    print("    2.cpr                     Compress and run server")
    print("    3.run                     Only run server")
    print("    4.reset_local_setting     Reset openstack_dashboard/local/local_settings.py")
    print("    5.edit_local_setting      Edit openstack_dashboard/local/local_settings.py")
    print("    6.edit_setting            Edit openstack_dashboard/settings.py")
    print("    7.enable_sso_login        Enable SSO login")
    print("    8.disable_sso_login       Disable SSO login")
    print("    9.enable_compress         Enable JS compress")
    print("   10.disable_compress        Disable JS compress")
    print("   11.run_nohup               Run with nohup")
    print("   12.stop_nohup              Stop the nohup runserver")
    sys.exit(0)

if len(sys.argv) > 2:
    print("Error: Unknow Command!")
    sys.exit(1)

if sys.argv[1] == "1" or sys.argv[1] == "cpl":
    compile_proj()
    compress_proj()
    run_proj(False)

elif sys.argv[1] == "2" or sys.argv[1] == "cpr":
    compress_proj()
    run_proj(False)

elif sys.argv[1] == "3" or sys.argv[1] == "run":
    run_proj(False)

elif sys.argv[1] == "4" or sys.argv[1] == "reset_local_setting":
    # 拷贝 local_settings.py 文件
    system("cat %s > %s" % (PUBLIC_LOCAL_SETTINGS, HORIZON_LOCAL_SETTINGS,))
    # 修改 DEBUG
    system("openstack-config --set {} DEFAULT True".format(HORIZON_LOCAL_SETTINGS))
    # 禁止验证码校验
    replace_file_str(
        HORIZON_SETTINGS,
        "HORIZON_CONFIG['captcha_disabled'] = False",
        "HORIZON_CONFIG['captcha_disabled'] = True",
    )

elif sys.argv[1] == "5" or sys.argv[1] == "edit_local_setting":
    system("vim {}".format(HORIZON_LOCAL_SETTINGS))

elif sys.argv[1] == "6" or sys.argv[1] == "edit_setting":
    system("vim {}".format(HORIZON_SETTINGS))

elif sys.argv[1] == "7" or sys.argv[1] == "enable_sso_login":
    set_sso_login(True)

elif sys.argv[1] == "8" or sys.argv[1] == "disable_sso_login":
    set_sso_login(False)

elif sys.argv[1] == "9" or sys.argv[1] == "enable_compress":
    set_compress(True)

elif sys.argv[1] == "10" or sys.argv[1] == "disable_compress":
    set_compress(False)

elif sys.argv[1] == "11" or sys.argv[1] == "run_nohup":
    stop_runserver()
    commond = "nohup {} 1 > {}_log 2>&1 &".format(__file__, HORIZON_HOME)
    # print("Done: {}".format(commond))
    print("The log file is: {}_log".format(HORIZON_HOME))
    system(commond)

elif sys.argv[1] == "12" or sys.argv[1] == "stop_nohup":
    stop_runserver()

else:
    print("Error: Unknow Command!")
    sys.exit(1)
