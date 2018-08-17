#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# 路径配置
HORIZON_HOME = "/home/dengjy/horizon"
PUBLIC_LOCAL_SETTINGS = "/usr/share/openstack-dashboard/openstack_dashboard/local/local_settings.py"
COPY_LOCAL_SETTINGS = "/home/horizon/local_settings.py"

# 属性配置
SERVER_PORT = "8093"
USER_GROUP = "dengjy:dengjy"

# 选项配置
IS_ROOT = True
IS_NEED_IP_NETNS = False
IS_NEED_CHOWN = True

# 常量
HORIZON_LOCAL_SETTINGS = "%s/openstack_dashboard/local/local_settings.py" % (HORIZON_HOME,)
HORIZON_SETTINGS = "%s/openstack_dashboard/settings.py" % (HORIZON_HOME,)
HORIZON_SCRIPTS = "%s/horizon/templates/horizon/_scripts.html" % (HORIZON_HOME,)
HORIZON_CONF = "%s/horizon/templates/horizon/_conf.html" % (HORIZON_HOME,)


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


def chown_proj():
    if IS_NEED_CHOWN:
        system("chown %s %s -R" % (USER_GROUP, HORIZON_HOME))


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


def run_proj():
    os.chdir(HORIZON_HOME)
    if IS_NEED_IP_NETNS:
        system("ip netns exec haproxy python manage.py runserver 0:%s" % (SERVER_PORT,))
    else:
        system("python manage.py runserver 0:%s" % (SERVER_PORT,))


def set_sso_login(flag):
    old_str = "SSO_LOGIN = True"
    new_str = "SSO_LOGIN = False"
    if flag:
        old_str = "SSO_LOGIN = False"
        new_str = "SSO_LOGIN = True"
    replace_file_str(
        HORIZON_SETTINGS,
        "HORIZON_CONFIG['captcha_disabled'] = False",
        "HORIZON_CONFIG['captcha_disabled'] = True"
    )
    replace_file_str(HORIZON_LOCAL_SETTINGS, old_str, new_str)


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
    sys.exit(0)

if len(sys.argv) > 2:
    print("Error: Unknow Command!")
    sys.exit(1)


if sys.argv[1] == "1" or sys.argv[1] == "cpl":
    compile_proj()
    compress_proj()
    chown_proj()
    run_proj()

elif sys.argv[1] == "2" or sys.argv[1] == "cpr":
    compress_proj()
    chown_proj()
    run_proj()

elif sys.argv[1] == "3" or sys.argv[1] == "run":
    chown_proj()
    run_proj()

elif sys.argv[1] == "4" or sys.argv[1] == "reset_local_setting":
    # 拷贝 local_settings.py 文件
    if IS_ROOT:
        system("cat %s > %s" % (PUBLIC_LOCAL_SETTINGS, HORIZON_LOCAL_SETTINGS,))
    else:
        system("cat %s > %s" % (COPY_LOCAL_SETTINGS, HORIZON_LOCAL_SETTINGS,))
    # 修改 DEBUG
    replace_file_str(HORIZON_LOCAL_SETTINGS, "DEBUG = False", "DEBUG = True")
    # 修改 SECRET_KEY
    if not IS_ROOT:
        replace_file_str(HORIZON_SETTINGS, "SECRET_KEY = None", "SECRET_KEY = 'SECRET_KEY'")
    # 禁止验证码校验
    replace_file_str(
        HORIZON_SETTINGS,
        "HORIZON_CONFIG['captcha_disabled'] = False",
        "HORIZON_CONFIG['captcha_disabled'] = True",
    )
    # 修改目录权限
    chown_proj()

elif sys.argv[1] == "5" or sys.argv[1] == "edit_local_setting":
    system("vim %s" % (HORIZON_LOCAL_SETTINGS,))

elif sys.argv[1] == "6" or sys.argv[1] == "edit_setting":
    system("vim %s" % (HORIZON_SETTINGS,))

elif sys.argv[1] == "7" or sys.argv[1] == "enable_sso_login":
    set_sso_login(True)

elif sys.argv[1] == "8" or sys.argv[1] == "disable_sso_login":
    set_sso_login(False)

elif sys.argv[1] == "9" or sys.argv[1] == "enable_compress":
    set_compress(True)

elif sys.argv[1] == "10" or sys.argv[1] == "disable_compress":
    set_compress(False)

else:
    print("Error: Unknow Command!")
    sys.exit(1)

