# coding=utf-8
"""
    @project: qabot
    @file： authenticate.py
    @desc:  keycloak用户认证
"""
from django.db.models import QuerySet

from common.auth.handle.auth_base_handle import AuthBaseHandle
from common.constants.authentication_type import AuthenticationType
from common.constants.permission_constants import RoleConstants, get_permission_list_by_role, Auth
from common.exception.app_exception import AppAuthenticationFailed
from smartdoc.settings import JWT_AUTH
from smartdoc.settings import KEYCLOAK_OPENID
from users.models import User
from django.core import cache

from users.models.user import get_user_dynamics_permission

token_cache = cache.caches['token_cache']


class KeycloakToken(AuthBaseHandle):
    def support(self, request, token: str, get_token_details):
        # 获取request对应header X-KEYCLOAK—AUTH 的内容
        keycloak_auth = request.META.get('HTTP_X_KEYCLOAK_AUTH')
        print(f"keycloak认证: {keycloak_auth}")
        return bool(keycloak_auth) and not str(token).startswith("application-")

    def handle(self, request, token: str, get_token_details):
        print("准备进行keycloak认证")
        cache_token = token_cache.get(token)
        # 缓存token为空则从keycloak获取
        if cache_token is None:
            user_info = KEYCLOAK_OPENID.userinfo(token)
            if user_info is None:
                raise AppAuthenticationFailed(1002, "登录过期")
            user = self.sync_keycloak_user(user_info)
            # 创建token
            token_cache.set(token, user, timeout=JWT_AUTH['JWT_EXPIRATION_DELTA'])
        else:
            user = cache_token
        # 续期
        token_cache.touch(token, timeout=JWT_AUTH['JWT_EXPIRATION_DELTA'].total_seconds())
        rule = RoleConstants[user.role]
        permission_list = get_permission_list_by_role(RoleConstants[user.role])
        # 获取用户的应用和知识库的权限
        permission_list += get_user_dynamics_permission(str(user.id))
        return user, Auth(role_list=[rule],
                          permission_list=permission_list,
                          client_id=str(user.id),
                          client_type=AuthenticationType.KEY_CLOAK.value,
                          current_role=rule)

    def sync_keycloak_user(self, user_info):
        # 查询邮箱是否存在，不存在则自动创建用户
        user = QuerySet(User).filter(email=user_info['email']).first()
        if user is None:
            user = User(
                **{'id': user_info["sub"], 'email': user_info['email'], 'username': user_info['preferred_username'],
                   'role': RoleConstants.USER.name})
            user.save()

        return user