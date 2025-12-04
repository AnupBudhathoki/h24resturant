from django.db import models

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    number=models.IntegerField()
    message=models.TextField()


class Category(models.Model):
    title=models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
class Momo(models.Model):
    name=models.CharField(max_length=200)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    image=models.ImageField(upload_to="images")
    price=models.DecimalField(max_digits=8, decimal_places=2)