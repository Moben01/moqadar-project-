from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import cuurency

@receiver(post_migrate)
def create_default_currencies(sender, **kwargs):
    if sender.name == 'Finance_and_Accounting':  # Replace 'your_app_name' with the name of your app
        required_currencies = ["افغانی", "دالر"]
        for currency_name in required_currencies:
            if not cuurency.objects.filter(curr_name=currency_name).exists():
                cuurency.objects.create(curr_name=currency_name)