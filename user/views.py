from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
import re
from django.core.files.storage import default_storage
from PIL import Image
import imghdr
from .models import *
from postingan.models import Postingan
from django.http import HttpResponse
from django.views.generic import ListView
# Create your views here.
class LoginView(View):
    template_name = 'login.html'
    def get(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request,'Anda Sudah Login')
            return redirect('postingan')
        return render(request, self.template_name)
    def post (self,request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,f'Login berhasil selamat datang {user.first_name}')
            return redirect('postingan') 
        else:
            messages.error(request,'Invalid username or password')
            return render(request, self.template_name)

class RegisterView(View):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request,'Anda Sudah Login')
            return redirect('postingan')
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name').strip()
        username = request.POST.get('username').lower().strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        confirm_password = request.POST.get('confirm_password').strip()
        if not re.match(r'^\S+@\S+\.\S+$', email):
            messages.warning(request, "Invalid email format")
            return render(request, self.template_name)
        if not username or not name:
            messages.warning(request, "Username or email is empty")
            return render(request, self.template_name)
        if not password:
            messages.warning(request, "password is empty")
            return render(request, self.template_name)
        if password == confirm_password :
            # Check if the username or email is already taken
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                messages.warning(request, "Username or email already exists")
                return render(request, self.template_name)
            # Create a new user
            user = User.objects.create_user( username, email, password, first_name = name)
            UserProfile.objects.create(user= user, profile_picture = 'static/assets/profile.jpg' )
            login(request, user)
            return redirect('postingan')  # Redirect to the desired URL after registration
        else:
            # Passwords do not match
            messages.warning(request, "Passwords do not match")
            return render(request, self.template_name)

        # Registration failed
        return render(request, self.template_name, {'error_message': 'User registration failed'})
class userProfileView(View):
    template_name = 'profile.html'
    def get(self,request,username):
        user = get_object_or_404(User,username=username)
        postingan = Postingan.objects.filter(penulis=user).order_by('-tanggal_dibuat')
        following = user.user_following.filter(user=request.user).exists()
        
        context = {'detail_user':user,'postingan':postingan, 'following':following}
        return render(request, self.template_name, context)
    def post(self,request,*args, **kwargs):
        name = request.POST.get('name').strip()
        username = request.POST.get('username').lower().strip()
        email = request.POST.get('email').strip()
        if not re.match(r'^\S+@\S+\.\S+$', email):
            messages.warning(request, "Invalid email format")
            return render(request, self.template_name)
        if not username or not name:
            messages.warning(request, "Username or email is empty")
            return render(request, self.template_name)
        user = User.objects.get(username = request.user.username)
        if user == request.user:
            user.username = username
            user.first_name = name
            user.email = email
            user.save()
            messages.success(request, "User berhasil di perbarui")
            return redirect('profile', username=username)
        else:
            messages.error(request, "User gagal di perbarui")
            return redirect('profile', username=kwargs['username'])
class ChangePassword(View):
    def post(self,request, username,*args, **kwargs):
        user = User.objects.get(username = username)
        curent_pasword = request.POST.get('curent_password').strip()
        new_password = request.POST.get('password').strip()
        confirm_password = request.POST.get('confirm_password').strip()
        
            
        if new_password != confirm_password:
            messages.error(request," Password Sebelum nya tidak sama")
            return redirect('profile', username = username)
        if not new_password or not confirm_password:
            messages.error(request," Field kosong")
            return redirect('profile', username = username)
        if not authenticate(username = username, password = curent_pasword):
            messages.error(request," Password Sebelum nya tidak sama")
            return redirect('profile', username = username)
        else:
            user.set_password(new_password)
            user.save()
            login(request, user)
            messages.success(request," Berhasil di ubah")
            return redirect('profile', username = username)

def toggleFollow(request, user_id,*args, **kwargs):
    if request.POST :
        following = get_object_or_404(UserProfile, user=request.user)
        follower = get_object_or_404(UserProfile, user=user_id)

        # Penanganan kasus ketika pengguna mencoba mengikuti dirinya sendiri
        if request.user.id == user_id:
            messages.error(request, "Tidak dapat mengikuti diri sendiri.")
            return redirect('postingan')

        if following.following.filter(id=user_id).exists():
            following.following.remove(follower.user)
            follower.follower.remove(request.user)
            print(f"user {request.user.id} ingin unfollow {user_id}")
        else:
            following.following.add(follower.user)
            follower.follower.add(request.user)
            print(f"user {request.user.id} ingin mengikuti {user_id}")
        return redirect('profile', username = kwargs['username'])
    else:
        return HttpResponse("Miyaww")
class UserFollowerView(View):
    template_name = "list_user.html"
    def get(self, request, username):
        # Dapatkan objek User berdasarkan nama pengguna
        user = get_object_or_404(User, username=username)
        # Dapatkan objek UserProfile terkait dengan pengguna
        user_profile = get_object_or_404(UserProfile, user=user)
        # Dapatkan daftar pengguna yang mengikuti oleh pengguna ini
        follower_users = user_profile.follower.all()
        return render(request, self.template_name, {'list_user': follower_users})
class UserFollowingView(View):
    template_name = "list_user.html"
    def get(self, request, username):
        # Dapatkan objek User berdasarkan nama pengguna
        user = get_object_or_404(User, username=username)
        # Dapatkan objek UserProfile terkait dengan pengguna
        user_profile = get_object_or_404(UserProfile, user=user)
        # Dapatkan daftar pengguna yang mengikuti oleh pengguna ini
        following_users = user_profile.following.all()
        return render(request, self.template_name, {'list_user': following_users})
class changeProfilePicture(View):
    def post (self,request,username, *args, **kwargs):
        user = UserProfile.objects.get(user = request.user.id)
        profile_image = request.FILES.get('profile_image')
        print(profile_image)
        if profile_image:
            valid_image_formats = ["jpeg", "jpg", "png", "gif"]
            file_format = imghdr.what(profile_image)
            print(f"Format Gambar = {file_format}")
            if file_format not in valid_image_formats:
                print("Image tidak valid")
                messages.error(request, "Gambar tidak valid harap unggah gambar yang valid")
                return redirect('profile',username=username)
            try:
                image = Image.open(profile_image)
                image.tell()
            except Exception as e:
                messages.error(request, f"Error opening the image: {e}")
                return redirect('profile',username=username)
            #  hapus file pada direktori
            if user.profile_picture:
                old_picture_path = user.profile_picture.path
                default_storage.delete(old_picture_path)
            user.profile_picture.save(slugify(request.user.username) + "_profile.jpg", profile_image)
            user.save()
        else:
            if user.profile_picture:
                old_picture_path = user.profile_picture.path
                default_storage.delete(old_picture_path)
            default_picture ='static/assets/profile.jpg'
            user.profile_picture.save(slugify(request.user.username) + "_default.jpg", default_storage.open(default_picture))
            user.save()
        # if request.user == user.user:
        return redirect('profile',username=username)
class ListUserView(LoginRequiredMixin,ListView):
    model = User
    login_url ='login'
    template_name = 'list_user.html'
    context_object_name='list_user'