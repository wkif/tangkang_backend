# 初始化
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.settings")
django.setup()

from dvadmin.system.views.admin.user import UsersInitSerializer
from dvadmin.system.views.admin.menu import MenuInitSerializer
from dvadmin.utils.core_initialize import CoreInitialize
from dvadmin.system.views.admin.role import RoleInitSerializer
from dvadmin.system.views.admin.api_white_list import ApiWhiteListInitSerializer
from dvadmin.system.views.admin.dept import DeptInitSerializer
from dvadmin.system.views.admin.dictionary import DictionaryInitSerializer
from dvadmin.system.views.admin.system_config import SystemConfigInitSerializer
from miniapp.serializers import integralDetailModelserializers, pagePathListModelserializers, tabListModelserializers


class Initialize(CoreInitialize):

    def init_dept(self):
        """
        初始化部门信息
        """
        self.init_base(DeptInitSerializer, unique_fields=['name', 'parent'])

    def init_role(self):
        """
        初始化角色信息
        """
        self.init_base(RoleInitSerializer, unique_fields=['key'])

    def init_users(self):
        """
        初始化用户信息
        """
        self.init_base(UsersInitSerializer, unique_fields=['username'])

    def init_menu(self):
        """
        初始化菜单信息
        """
        self.init_base(MenuInitSerializer, unique_fields=['name', 'web_path', 'component', 'component_name'])

    def init_api_white_list(self):
        """
        初始API白名单
        """
        self.init_base(ApiWhiteListInitSerializer, unique_fields=['url', 'method', ])

    def init_dictionary(self):
        """
        初始化字典表
        """
        self.init_base(DictionaryInitSerializer, unique_fields=['value', 'parent', ])

    def init_system_config(self):
        """
        初始化系统配置表
        """
        self.init_base(SystemConfigInitSerializer, unique_fields=['key', 'parent', ])

    def init_integral(self):
        """
        初始化积分表
        """
        self.init_base(integralDetailModelserializers, unique_fields=['name', 'integral', ])

    def init_pagepathlist(self):
        """
        初始化页面路径表
        """
        self.init_base(pagePathListModelserializers, unique_fields=['name', 'path', ])

    def init_tablist(self):
        """
        初始化页面tab表
        """
        self.init_base(tabListModelserializers,
                       unique_fields=['name', 'pagePath', 'iconPath', 'selectedIconPath', 'is_active', ])

    def run(self):
        self.init_dept()
        self.init_role()
        self.init_users()
        self.init_menu()
        self.init_api_white_list()
        self.init_dictionary()
        self.init_system_config()
        self.init_integral()
        self.init_pagepathlist()
        self.init_tablist()


if __name__ == "__main__":
    Initialize(app='dvadmin.system').run()
