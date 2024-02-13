

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Cars(models.Model):
    car_name = models.CharField(max_length=100, unique=True)
    car_version = models.CharField(max_length=30)
    car_model = models.CharField(max_length=30)
    likes = models.IntegerField(default=0)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    liked_at= models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        super(Like, self).save(*args, **kwargs)
        self.car.likes += 1
        self.car.save()

    def delete(self, *args, **kwargs):
        self.car.likes -= 1
        self.car.save()
        super(Like, self).delete(*args, **kwargs)


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    comment = models.TextField(max_length=100)





    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.message}"





# 192.168.0.155
