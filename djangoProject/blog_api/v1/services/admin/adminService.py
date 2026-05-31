from blog_api.models import Bannedwords


class adminService:
    @staticmethod
    def get_bannedword():
        bannedwords = list(Bannedwords.objects.all().values("id", "word"))
        return bannedwords

    @staticmethod
    def create_bannedword(validated_data):
        word = validated_data.get("word")
        if not word:
            return {"msg": "违禁词不能为空", "code": 400}

            # 检查是否重复
        if Bannedwords.objects.filter(word=word).exists():
            return {"msg": "该违禁词已存在", "code": 400}

        Bannedwords.objects.create(word=word)
        return {"msg": "添加成功", "code": 200}

    @staticmethod
    def delete_bannedword(data):
        word_id = data["id"]
        if not word_id:
            return {"msg": "缺少id", "code": 400}
        try:
            Bannedwords.objects.filter(id=word_id).delete()
            return {"msg": "success", "code": 200}
        except Exception:
            return {"msg": "error", "code": 400}
