from typing import Any
from django.db.models import Count,Q
from django.db.models.query import QuerySet
from .models import *
import imghdr
from django.utils.html import escape
from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView,DetailView, TemplateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import *
# Create your views here.
class PostinganView(ListView):
    model = Postingan
    paginate_by= 9
    template_name="postingan.html"
    context_object_name = 'list_postingan'
    
    def get_queryset(self):
        return Postingan.objects.all().order_by('-tanggal_dibuat')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quote'] = Quotes.objects.filter(show=True)
        context['postingan_form']=PostinganForm()
        context['most_comment'] = Postingan.objects.annotate(num_comments=Count('komentar')).filter(num_comments__gt=1).order_by('-num_comments')
        context['most_like'] = Postingan.objects.annotate(num_like=Count('like')).filter(num_like__gt=1).order_by('-num_like')

        if self.request.user.is_authenticated:  
            postingan_ids_liked_by_user = self.request.user.post_like.values_list('id', flat=True)
            context['post_ids_liked_by_user'] = postingan_ids_liked_by_user
        return context
    

class DetailPostinganView(LoginRequiredMixin,DetailView):
    login_url = 'login'
    redirect_field_name = 'login'
    model = Postingan
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "post"
    template_name="postingan_detail.html"
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        postingan = self.get_object()
        context['form'] = KomentarForm
        context['list_komentar'] = Komentar.objects.filter(posting=postingan).order_by('-tanggal_dibuat')
        return context
class TambahKomentar(LoginRequiredMixin,View):
    login_url = 'login'
    redirect_field_name ='login'
    def post(self,request, *args, **kwargs):
        # Dapatkan objek postingan yang akan diberi komentar
        
        postingan = get_object_or_404(Postingan, slug=kwargs['slug'])
        # Dapatkan data komentar dari formulir
        form = KomentarForm(request.POST) # Ganti 'komentar_input' dengan nama field dari formulir komentar
        if form.is_valid():
            konten = form.cleaned_data['konten']
            Komentar.objects.create(posting = postingan, penulis = request.user, konten = konten)
            return redirect('detail-postingan', slug =kwargs['slug'])
        else:
            messages.error(request,"Tidak valid")
            return redirect('detail-postingan', slug =kwargs['slug'])
class HapusKomentar(LoginRequiredMixin,DeleteView):
    login_url = 'login'
    redirect_field_name ='login'
    model = Komentar
    
    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('detail-postingan', kwargs={'slug': self.kwargs['slug']})

    
    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('detail-postingan', kwargs={'slug': self.kwargs['slug']})
class TambahPostinganView(LoginRequiredMixin, View):
    template_name = "postingan_tambah.html"
    login_url = 'login'
    def get (self,request):
        form = PostinganForm()
        return render(request, self.template_name,{'form':form})
    
    def post(self, request,*args, **kwargs):
        form = PostinganForm(request.POST, request.FILES)
        if form.is_valid():
            # Lakukan sesuatu dengan data formulir yang valid
            judul = form.cleaned_data['judul_input']
            gambar = form.cleaned_data['gambar_input']
            konten = form.cleaned_data['konten_input']
            if gambar:
                valid_image_formats = ["jpeg", "jpg", "png", "gif"]
                file_format = imghdr.what(gambar)
                print(f"Format Gambar = {file_format}")
                if file_format not in valid_image_formats:
                    print("Image tidak valid")
                    messages.error(request, "Gambar tidak valid harap unggah gambar yang valid")
                    return redirect('postingan')
                try:
                    image = Image.open(gambar)
                    image.tell()
                except Exception as e:
                    messages.error(request, f"Error opening the image: {e}")
                    return redirect('postingan') 
            Postingan.objects.create(judul = judul, konten = konten, penulis = request.user, gambar = gambar)
            messages.success(request, "Diskusi berhasil dibuat")
            return redirect('postingan')
        else:
            messages.error(request, "Diskusi gagal dibuat.")
            return redirect('postingan')
class DeletePostinganView(LoginRequiredMixin,DeleteView):
    login_url='login'
    def post(self, request,id):
        postingan = get_object_or_404(Postingan, id=id)
        if request.user == postingan.penulis:
            postingan.delete()
            messages.success(request, 'Postingan berhasil dihapus.')
            return redirect('postingan')  
        else:
            messages.error(request, 'Anda tidak memiliki izin untuk menghapus postingan ini.')
            return redirect('postingan') 
class EditPostinganView(LoginRequiredMixin,View):
    def post(self, request,id,**kwargs):
        postingan = get_object_or_404(Postingan, id=id, penulis=request.user)
        judul = request.POST['judul_input'].strip()
        konten = escape(request.POST['konten_input'].strip())
        if judul and konten:
            postingan.judul = judul
            postingan.konten = konten
            postingan.save()
            messages.success(request, "Postingan berhasil di edit")
        else:
            messages.error(request, "Judul dan konten tidak boleh kosong")
        
        return redirect('detail-postingan', slug=kwargs['slug'])
    
class ShowQuotes(ListView):
    model = Quotes
    template_name = 'postingan.html'
    context_object_name ='quote'
    
    
    print(Quotes.objects.filter(show=True))
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["quotes"] = Quotes.objects.filter(show = True)
        return context
    
def toggleLike(request, post_id):
    post = get_object_or_404(Postingan, id= post_id)
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
        liked = False
    else:
        post.like.add(request.user)
        liked = True
    return redirect('postingan')
class SearchPostingan(ListView):
    template_name = 'search_postingan.html'
    model= Postingan
    context_object_name = 'list_postingan'
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Postingan.objects.filter(Q(judul__contains=query) | Q(konten__contains = query))
        return object_list