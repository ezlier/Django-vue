from datetime import timedelta
from django.utils import timezone
from .models import Visitor

def clear_old_visitors():
    cutoff = timezone.now() - timedelta(days=30)
    Visitor.objects.filter(visit_time__lt=cutoff).delete()