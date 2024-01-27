from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='static/profile_pictures/',default='static/assets/profile.jpg', null=True, blank=True)
    follower = models.ManyToManyField(User, related_name="user_follower",blank=True)
    following = models.ManyToManyField(User, related_name="user_following", blank=True)
    # Tambahkan field lain yang mungkin diperlukan untuk profil pengguna

    def __str__(self):
        return self.user.username

    