from django.core.validators import *
from django.db import models
from django.conf import settings
class Type(models.Model):
    name = models.CharField(max_length=2500)
    def __str__(self):
       return self.name



class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    genre = models.ForeignKey(Type, related_name='type', on_delete=models.CASCADE)
    description = models.TextField()
    pdf = models.FileField(upload_to='books/', validators=[FileExtensionValidator(['pdf'])], blank=True, null=True)
    cover_image = models.ImageField(upload_to='books/covers/', blank=True, null=True)
    uploaded_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, default=False)
    location = models.TextField(max_length=500, default=False)
    views = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)


    def __str__(self):
        return self.title





class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} in {self.user.name}'s cart"




# class Review(models.Model):
#     book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
#     user = models.ForeignKey('accounts.User', related_name='reviews', on_delete=models.CASCADE)
#     rating = models.PositiveSmallIntegerField()
#     comment = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'Review by {self.user}   for   {self.book}'




