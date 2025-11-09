import json
import os
from datetime import datetime
from datetime import timedelta
import bleach

import markdown
import yaml
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import IsAdminUser
from django.utils.text import get_valid_filename
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Visitor, Message, Bannedwords


@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({"detail": "CSRF cookie set"})


def visitor_stats(request):
    total_visits = Visitor.objects.all()
    visitor_list = list(total_visits.values("ip", "visit_time"))
    return JsonResponse(visitor_list, safe=False)


def record_visitor(request):
    ip = get_client_ip(request)
    path = request.path
    user_agent = escape(request.META.get("HTTP_USER_AGENT", "")[:256])
    now = timezone.now()

    # 查找该IP在最近10分钟是否访问过
    recent_visit = Visitor.objects.filter(ip=ip, path=path, visit_time__gte=now - timedelta(minutes=10)).exists()
    if not recent_visit:
        Visitor.objects.create(ip=ip, path=path, user_agent=user_agent)


def get_client_ip(request):
    """获取真实客户端IP"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_data(request):
    return Response({'message': f'Welcome, {request.user.username}!'})


@api_view(['POST'])
@ratelimit(key='ip', rate='10/m', block=True)
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': '用户名或密码错误'}, status=400)

    # 生成 JWT token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response({
        'token': access_token,
        'refresh': str(refresh),
        'username': user.username,
        'expires_in': refresh.access_token.lifetime.total_seconds(),  # 例如3600秒
    })


ARTICLES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'articles')


def parse_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) > 2:
            meta = yaml.safe_load(parts[1])
            body = parts[2].strip()
        else:
            meta = {}
            body = content
    else:
        meta = {}
        body = content

    allowed_tags = [
        "p", "pre", "code", "img", "h1", "h2", "h3", "h4", "h5",
        "table", "thead", "tbody", "tr", "th", "td", "blockquote", "ul", "ol", "li", "a", "strong", "em"
    ]
    allowed_attrs = {
        "img": ["src", "alt", "title"],
        "a": ["href", "title", "target"]
    }

    html_body = bleach.clean(
        markdown.markdown(body, extensions=["fenced_code", "tables"]),
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )

    # 拼接完整图片 URL
    image_path = meta.get("image", "")
    image_url = image_path

    raw_date = meta.get("date", "")
    formatted_date = ""

    # 情况1：YAML 自动识别成 datetime 类型
    if isinstance(raw_date, datetime):
        formatted_date = raw_date.strftime("%Y-%m-%d")

    # 情况2：字符串格式（带空格或T）
    elif isinstance(raw_date, str):
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
            try:
                formatted_date = datetime.strptime(raw_date, fmt).strftime("%Y-%m-%d")
                break
            except ValueError:
                continue

    # 没法识别的就原样返回
    else:
        formatted_date = str(raw_date)

    return {
        "title": meta.get("title", "无标题"),
        "date": formatted_date,
        "tags": meta.get("tags", []),
        "image": image_url,
        "content": html_body,
        "raw": body
    }


def list_articles(request):
    record_visitor(request)
    if request.method == 'GET':
        files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.md')]
        data = []
        for f in files:
            file_path = os.path.join(ARTICLES_DIR, f)
            article = parse_markdown_file(file_path)
            article["slug"] = f.replace(".md", "")
            article.pop("content")  # 列表不需要正文
            data.append(article)

        return JsonResponse(data, safe=False)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAdminUser])
@csrf_exempt
def admin_articles(request):
    record_visitor(request)
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return JsonResponse({'error': '未接收到文件'}, status=400)

        filename = os.path.basename(get_valid_filename(uploaded_file.name))
        if not filename.endswith(".md"):
            return JsonResponse({'error': '只允许上传 Markdown 文件'}, status=400)

        save_path = os.path.join(ARTICLES_DIR, filename)
        with open(save_path, 'wb+') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        return JsonResponse({'message': '文件上传成功', 'filename': uploaded_file.name})

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            slug = data.get("slug")
            slug = os.path.basename(slug)
            if not slug.endswith(".md"):
                slug += ".md"
            file_path = os.path.join(ARTICLES_DIR, slug)
            if os.path.exists(file_path):
                os.remove(file_path)
                return JsonResponse({"message": "文件删除成功"})
            else:
                return JsonResponse({"error": "文件不存在"}, status=404)
        except Exception as e:
            return JsonResponse({"error": "操作失败"}, status=500)

    else:
        return JsonResponse({"error": "滚"}, status=405)


@require_GET
def get_article(request, slug):
    file_path = os.path.join(ARTICLES_DIR, slug + ".md")
    if not os.path.exists(file_path):
        return JsonResponse({"error": "not found"}, status=404)
    data = parse_markdown_file(file_path)
    return JsonResponse(data)


def get_about_text(request):
    about_path = os.path.join(settings.BASE_DIR, 'static', 'text', 'about.md')
    try:
        with open(about_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        html = markdown.markdown(md_content)
        return JsonResponse({'html': html})
    except FileNotFoundError:
        return JsonResponse({'error': 'about.md not found'}, status=404)


SETTINGS_FILE = "static/config/websetting.json"


@api_view(['POST', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_websetting(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(body, f, ensure_ascii=False, indent=2)
            return JsonResponse({"code": 200, "msg": "更新成功"})
        except Exception as e:
            return JsonResponse({"code": 500, "msg": f"保存失败"})


@api_view(['GET'])
def getwebsetting(request):
    if request.method == "GET":
        # 读取配置文件
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {
                "name": "your name",
                "blog_name": "your blog name",
                "date": "2025-07-17",
                "footer_text1": "山海自有归期，风雨自有相逢",
                "footer_text2": "备案*********",
            }
        return JsonResponse(data)


@api_view(['POST', 'GET'])
@ratelimit(key='ip', rate='10/m', block=True)
def get_message(request):
    if request.method == "GET":
        messageList = Message.objects.all()
        messageList = list(messageList.values("name", "text", "time", "id"))
        return JsonResponse(messageList, safe=False)
    elif request.method == "POST":
        try:
            bannedwords = Bannedwords.objects.all()
            bannedwords = list(bannedwords.values("word"))
            ip = get_client_ip(request)
            now = timezone.now()
            body = json.loads(request.body.decode("utf-8"))
            if len(body["message"]) == 0 or len(body["name"]) == 0 or len(body["message"]) > 400 or len(body["name"]) > 10:
                return JsonResponse({"code": 400, "error": "内容不能为空"})
            for i in bannedwords:
                if i['word'] in body["message"] or i['word'] in body["name"]:
                    return JsonResponse({"code": 400, "error": "内容包含违禁词"}, status=400)
            Message.objects.create(ip=ip, time=now, text=body["message"], name=body["name"])
            return JsonResponse({"code": 200})
        except Exception as e:
            return JsonResponse({"code": 500})


@api_view(['GET', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_message(request):
    if request.method == "GET":
        messageList = Message.objects.all()
        messageList = list(messageList.values("name", "text", "time", "id", "ip"))
        return JsonResponse(messageList, safe=False)

    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            Message.objects.filter(id=data["id"]).delete()
            return JsonResponse({"code": 200})
        except Exception as e:
            return JsonResponse({"code": 500})


@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAdminUser])
def bannedwords_setting(request):
    if request.method == "GET":
        # 获取全部违禁词
        bannedwords = Bannedwords.objects.all().values("id", "word")
        return JsonResponse(list(bannedwords), safe=False)

    elif request.method == "POST":
        # 添加违禁词
        try:
            data = json.loads(request.body.decode("utf-8"))
            word = data.get("word", "").strip()
            if not word:
                return JsonResponse({"code": 400, "error": "违禁词不能为空"}, status=400)

            # 检查是否重复
            if Bannedwords.objects.filter(word=word).exists():
                return JsonResponse({"code": 409, "error": "该违禁词已存在"}, status=409)

            Bannedwords.objects.create(word=word)
            return JsonResponse({"code": 200, "msg": "添加成功"})
        except Exception as e:
            return JsonResponse({"code": 500, "error": "error"}, status=500)

    elif request.method == "DELETE":
        # 删除违禁词
        try:
            data = json.loads(request.body.decode("utf-8"))
            word_id = data.get("id")
            if not word_id:
                return JsonResponse({"code": 400, "error": "缺少id"}, status=400)

            deleted, _ = Bannedwords.objects.filter(id=word_id).delete()
            if deleted == 0:
                return JsonResponse({"code": 404, "error": "未找到该违禁词"}, status=404)
            return JsonResponse({"code": 200, "msg": "删除成功"})
        except Exception as e:
            return JsonResponse({"code": 500, "error": "error"}, status=500)

    else:
        return JsonResponse({"code": 405, "error": "Method Not Allowed"}, status=405)
