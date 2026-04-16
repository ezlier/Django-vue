from rest_framework_simplejwt.tokens import RefreshToken

class AuthService:
    @staticmethod
    def generate_tokens_for_user(user):
        """为指定用户生成 JWT 令牌"""
        refresh = RefreshToken.for_user(user)
        return {
            'token': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username,
            'expires_in': refresh.access_token.lifetime.total_seconds(),
        }