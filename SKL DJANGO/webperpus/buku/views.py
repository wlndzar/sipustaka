from django.shortcuts import render, redirect
from django.db import connection

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]



def dictfetchone(cursor):
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row is None:
        return None
    return dict(zip(columns, row))



def buku_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi
            FROM buku_buku
            ORDER BY id DESC
        """)
        data_buku = dictfetchall(cursor)
    return render(request, 'index.html', {'buku_list': data_buku})



def buku_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buku_buku WHERE id = %s", [id])
        buku = dictfetchone(cursor)
    return render(request, 'detail.html', {'buku': buku})



def buku_create(request):
    if request.method == 'POST':
        judul        = request.POST.get('judul', '').strip()
        pengarang    = request.POST.get('pengarang', '').strip()
        kategori     = request.POST.get('kategori', '').strip()
        penerbit     = request.POST.get('penerbit', '').strip()
        tahun_terbit = request.POST.get('tahun_terbit', '').strip()
        rak          = request.POST.get('rak', '').strip()
        stok         = request.POST.get('stok', '').strip()
        deskripsi    = request.POST.get('deskripsi', '').strip()

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO  buku_buku (judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi])

            
        return redirect('buku_list')
    return render(request, 'form.html')



def buku_update(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buku_buku WHERE id = %s", [id])
        buku = dictfetchone(cursor)

    if request.method == 'POST':
        judul        = request.POST.get('judul', '').strip()
        pengarang    = request.POST.get('pengarang', '').strip()
        kategori     = request.POST.get('kategori', '').strip()
        penerbit     = request.POST.get('penerbit', '').strip()
        tahun_terbit = request.POST.get('tahun_terbit', '').strip()
        rak          = request.POST.get('rak', '').strip()
        stok         = request.POST.get('stok', '').strip()
        deskripsi    = request.POST.get('deskripsi', '').strip()

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE buku_buku
                SET judul=%s, pengarang=%s, kategori=%s, penerbit=%s,
                    tahun_terbit=%s, rak=%s, stok=%s, deskripsi=%s
                WHERE id = %s
            """, [judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi, id])
        return redirect('buku_list')

    return render(request, 'update.html', {'buku': buku})



def buku_delete(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buku_buku WHERE id = %s", [id])
        buku = dictfetchone(cursor)

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM buku_buku WHERE id = %s", [id])
        return redirect('buku_list')

    return render(request, 'delete.html', {'buku': buku})



def dashboard(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT SUM(stok) FROM buku_buku")
        total_buku = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM buku_buku")
        total_judul = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM buku_peminjaman WHERE status = 'dipinjam'")
        total_dipinjam = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM buku_peminjaman WHERE status = 'dikembalikan'")
        total_kembali = cursor.fetchone()[0]

        cursor.execute("SELECT judul, stok FROM buku_buku ORDER BY stok DESC")
        stok_buku = cursor.fetchall()
        max_stok = max([s[1] for s in stok_buku], default=1)

    return render(request, 'dashboard.html', {
        'total_buku': total_buku,
        'total_judul': total_judul,
        'total_dipinjam': total_dipinjam,
        'total_kembali': total_kembali,
        'stok_buku': stok_buku,
        'max_stok': max_stok,
    })