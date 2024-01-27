from django import forms
class KomentarForm(forms.Form):
    konten = forms.CharField(label="", widget=forms.TextInput(
        attrs={
            'class':'textarea-komen join-item input input-bordered',
            'placeholder':'Tambahkan Komentar'}
        ))
class PostinganForm(forms.Form):
    judul_input = forms.CharField(
        label='Masukan judul diskusi',
        widget=forms.TextInput(attrs={'class': 'input input-bordered w-full max-full'}),
    )
    gambar_input = forms.ImageField(
        label='Pilih gambar',
        widget=forms.FileInput(attrs={'class': 'file-input w-full'}),
        required=False,  # Jika tidak wajib diisi
    )
    konten_input = forms.CharField(
        label='Konten',
        widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered', 'id': 'editor1'}),
    )