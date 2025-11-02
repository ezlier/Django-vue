import json
import os
from datetime import datetime
from datetime import timedelta

import markdown
import yaml
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.views.decorators.http import require_GET
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Visitor,Message


def visitor_stats(request):
    total_visits = Visitor.objects.all()
    visitor_list = list(total_visits.values("ip", "visit_time"))

    return JsonResponse(visitor_list, safe=False)


def record_visitor(request):
    ip = get_client_ip(request)
    path = request.path
    user_agent = request.META.get("HTTP_USER_AGENT", "")
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


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_data(request):
    return Response({'message': f'Welcome, {request.user.username}!'})


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

    html_body = markdown.markdown(body, extensions=['fenced_code', 'tables'])

    # 拼接完整图片 URL
    image_path = meta.get("image", "")
    if image_path:
        image_url = f"http://127.0.0.1:8000/static/{image_path.lstrip('/')}"
    else:
        image_url = ""

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


@csrf_exempt
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

    elif request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return JsonResponse({'error': '未接收到文件'}, status=400)

        save_path = os.path.join(ARTICLES_DIR, uploaded_file.name)
        with open(save_path, 'wb+') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        return JsonResponse({'message': '文件上传成功', 'filename': uploaded_file.name})

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            slug = data.get("slug")
            if not slug:
                return JsonResponse({"error": "未提供文件名"}, status=400)

            file_path = os.path.join(ARTICLES_DIR, f"{slug}.md")
            if os.path.exists(file_path):
                os.remove(file_path)
                return JsonResponse({"message": "文件删除成功"})
            else:
                return JsonResponse({"error": "文件不存在"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

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


@csrf_exempt
def get_websetting(request):
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

    elif request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(body, f, ensure_ascii=False, indent=2)
            return JsonResponse({"code": 200, "msg": "更新成功"})
        except Exception as e:
            return JsonResponse({"code": 500, "msg": f"保存失败: {e}"})


@csrf_exempt
def get_message(request):
    if request.method == "GET":
        messageList = Message.objects.all()

        messageList = list(messageList.values("name", "text"))

        return JsonResponse(messageList, safe=False)
    elif request.method == "POST":
        try:
            ip = get_client_ip(request)
            now = datetime.now()
            body = json.loads(request.body.decode("utf-8"))
            if len(body["message"]) == 0 and len(body["text"]) == 0:
                return
            Message.objects.create(ip=ip, time=now, text=body["message"], name=body["name"])
            return JsonResponse({"code": 200})
        except Exception as e:
            print("2")