from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import *

def createCustomerProfile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)

        Customer.objects.create(
            user=instance,
            name = instance.username,
            email = instance.email 
        )

        print('profile created')

post_save.connect(createCustomerProfile, sender=User)