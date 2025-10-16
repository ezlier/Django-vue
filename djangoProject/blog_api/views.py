from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import os
import yaml
import markdown

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

    # 分离 YAML front matter
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

    # 转成 HTML（如果你要在前端直接展示）
    html_body = markdown.markdown(body, extensions=['fenced_code', 'tables'])

    return {
        "title": meta.get("title", "无标题"),
        "date": meta.get("date", ""),
        "tags": meta.get("tags", []),
        "image": meta.get("image", ""),
        "content": html_body,
        "raw": body
    }


@require_GET
def list_articles(request):
    files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.md')]
    data = []

    for f in files:
        file_path = os.path.join(ARTICLES_DIR, f)
        article = parse_markdown_file(file_path)
        article["slug"] = f.replace(".md", "")
        article.pop("content")  # 列表不需要正文
        data.append(article)

    return JsonResponse(data, safe=False)


@require_GET
def get_article(request, slug):
    file_path = os.path.join(ARTICLES_DIR, slug + ".md")
    if not os.path.exists(file_path):
        return JsonResponse({"error": "not found"}, status=404)
    data = parse_markdown_file(file_path)
    return JsonResponse(data)