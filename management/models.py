from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse  # Used to generate urls by reversing the URL patterns
from django.db.models.signals import post_save


class Item(models.Model):
    title = models.CharField(max_length=25)
    category = models.CharField(max_length=25)
    price = models.IntegerField()
    pic = models.ImageField(blank=True, null=True, upload_to='images')

#return canonical url for an object
    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])

    ##  __str__ method is used to override default string returnd by an object
    def __str__(self):
        return self.title


def create_user(sender, *args, **kwargs):
    if kwargs['created']:
        user = User.objects.create(username=kwargs['instance'],password="dummypass")


class Customer(models.Model):
    cust_id = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=10)
    contact_no = models.CharField(max_length=10)
    email=models.EmailField(unique=True)

    def __str__(self):
        return str(self.cust_id)


post_save.connect(create_user, sender=Customer)

class Order(models.Model):
    order_id = models.CharField(max_length=10,unique=True)
    cust_id = models.ForeignKey('Customer', on_delete=models.CASCADE)
    order_date = models.DateTimeField(null=True,blank=True)
    price = models.IntegerField()
    def __str__(self):
        return self.Customer.name+" ordered "+self.Item.title

