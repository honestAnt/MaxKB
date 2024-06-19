# coding=utf-8
"""
    @project: qabot
    @Author：虎
    @file： authenticate.py
    @date：2023/9/4 11:16
    @desc:  认证类
"""
import traceback

from django.core import cache
from django.core import signing
from django.conf import settings
from rest_framework.authentication import TokenAuthentication

from common.auth.handle.impl.application_key import ApplicationKey
from common.auth.handle.impl.public_access_token import PublicAccessToken
from common.auth.handle.impl.user_token import UserToken
from common.auth.handle.impl.keycloak_token import KeycloakToken
from common.exception.app_exception import AppAuthenticationFailed, AppEmbedIdentityFailed, AppChatNumOutOfBoundsFailed

token_cache = cache.caches['token_cache']


class AnonymousAuthentication(TokenAuthentication):
    def authenticate(self, request):
        return None, None


# handles = [KeycloakToken(), UserToken(), PublicAccessToken(), ApplicationKey()]
handles = [PublicAccessToken(), ApplicationKey(), KeycloakToken(), UserToken()]


class TokenDetails:
    token_details = None
    is_load = False

    def __init__(self, token: str):
        self.token = token

    def get_token_details(self):
        if self.token_details is None and not self.is_load:
            try:
                self.token_details = signing.loads(self.token)
            except Exception as e:
                self.is_load = True
        return self.token_details


class TokenAuth(TokenAuthentication):
    # 重新 authenticate 方法，自定义认证规则
    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION')
        # 未认证
        if auth is None:
            raise AppAuthenticationFailed(1003, '未登录,请先登录')
        try:
            token_details = TokenDetails(auth)
            for handle in handles:
                if handle.support(request, auth, token_details.get_token_details):
                    return handle.handle(request, auth, token_details.get_token_details)
            print("未匹配到认证过滤器，认证失败")
            raise AppAuthenticationFailed(1002, "身份验证信息不正确！非法用户")
        except Exception as e:
            print(f"认证过滤器异常，认证失败: {e}")
            traceback.format_exc()
            if isinstance(e, AppEmbedIdentityFailed) or isinstance(e, AppChatNumOutOfBoundsFailed):
                raise e
            raise AppAuthenticationFailed(1002, "身份验证信息不正确！非法用户")
