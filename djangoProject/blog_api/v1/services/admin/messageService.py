from blog_api.models import Comment, Message


class MessageService:

    @staticmethod
    def adminGetComment():
        comments = Comment.objects.all()
        return list(comments)

    @staticmethod
    def adminGetMessage():
        Messages = Message.objects.all()
        return list(Messages)
