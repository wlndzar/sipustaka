from django.db import models

from django.db import models

class Buku(models.Model):
    judul        = models.CharField(max_length=200)
    pengarang    = models.CharField(max_length=100)
    kategori     = models.CharField(max_length=100, blank=True, null=True)
    penerbit     = models.CharField(max_length=100, blank=True, null=True)
    tahun_terbit = models.DateField(blank=True, null=True)
    rak          = models.CharField(max_length=50, blank=True, null=True)
    stok         = models.IntegerField(default=0)
    deskripsi    = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.judul

class Buku_siswa(models.Model):
    nama      = models.CharField(max_length=100)
    kelas     = models.CharField(max_length=20)
    nis       = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nama

class Peminjaman(models.Model):
    STATUS_CHOICES = [
        ('dipinjam', 'Dipinjam'),
        ('dikembalikan', 'Dikembalikan'),
        ('terlambat', 'Terlambat'),
    ]
    buku_siswa          = models.ForeignKey(Buku_siswa, on_delete=models.CASCADE)
    buku           = models.ForeignKey(Buku, on_delete=models.CASCADE)
    tanggal_pinjam = models.DateField()
    jatuh_tempo    = models.DateField()
    keperluan      = models.TextField(blank=True, null=True)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='dipinjam')

    def __str__(self):
        return f"{self.buku_siswa.nama} - {self.buku.judul}"
