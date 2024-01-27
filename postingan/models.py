from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField
# Create your models here.
class Postingan(models.Model):
        judul = models.CharField(max_length=100)
        konten = RichTextField()
        penulis = models.ForeignKey(User, on_delete=models.CASCADE)
        tanggal_dibuat = models.DateTimeField(auto_now_add=True)
        gambar = models.ImageField(upload_to='static/images/', null=True, blank=True)
        slug = models.SlugField(default="", null=False, unique = True)
        like = models.ManyToManyField(User, related_name='post_like')
        class Meta:
            verbose_name_plural = "Postingan"
        def __str__(self):
            return self.slug
        def save(self, *args, **kwargs):
            if not self.id:
                # Newly created object, so set slug combining judul and penulis
                judul_slug = slugify(self.judul)
                penulis_slug = slugify(self.penulis.username)
                self.slug = f"{judul_slug}-{penulis_slug}"
            super(Postingan, self).save(*args, **kwargs)

class Komentar(models.Model):
    posting = models.ForeignKey('Postingan', on_delete=models.CASCADE, related_name='komentar')
    penulis = models.ForeignKey(User, on_delete=models.CASCADE)
    konten = models.TextField()
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    class Meta:
             verbose_name_plural = "Komentar"
    def __str__(self):
        return f"Komentar oleh {self.penulis} pada {self.posting}"
class Quotes(models.Model):
    quotes = models.TextField()
    author = models.CharField(max_length=100)
    show = models.BooleanField( default=False, null=True, )
    def save(self, *args, **kwargs):
        # Jika nilai show pada objek ini adalah True,
        # set semua objek Quotes dengan show=True menjadi False
        if self.show:
            Quotes.objects.exclude(id=self.id).update(show=False)
        super().save(*args, **kwargs)
    class Meta:
         verbose_name_plural = "Quote"
         
    def __str__(self):
        return f"Quotes {self.quotes}, oleh{self.author}"
    