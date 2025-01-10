from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    nick = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    passwd = models.CharField(max_length=128)

class Keys(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    private_key_file = models.BinaryField()
    public_key_file = models.BinaryField()
    iv = models.BinaryField()
    caducidad = models.DateTimeField()
