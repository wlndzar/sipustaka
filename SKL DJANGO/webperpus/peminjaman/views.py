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

def peminjaman_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, s.nama AS nama_siswa, b.judul AS judul_buku,
                   p.tanggal_pinjam, p.jatuh_tempo, p.keperluan, p.status
            FROM peminjaman p
            JOIN siswa s ON s.id = p.siswa_id
            JOIN buku b ON b.id = p.buku_id
            ORDER BY p.id DESC
        """)
        data = dictfetchall(cursor)
    return render(request, 'peminjaman_list.html', {'peminjaman_list': data})

def peminjaman_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, s.nama AS nama_siswa, b.judul AS judul_buku,
                   p.tanggal_pinjam, p.jatuh_tempo, p.keperluan, p.status
            FROM peminjaman p
            JOIN siswa s ON s.id = p.siswa_id
            JOIN buku b ON b.id = p.buku_id
            WHERE p.id = %s
        """, [id])
        peminjaman = dictfetchone(cursor)
    return render(request, 'peminjaman_detail.html', {'peminjaman': peminjaman})

def peminjaman_create(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama FROM siswa WHERE is_active = TRUE ORDER BY nama")
        siswa_list = dictfetchall(cursor)
        cursor.execute("SELECT id, judul FROM buku ORDER BY judul")
        buku_list = dictfetchall(cursor)

    if request.method == 'POST':
        siswa_id       = request.POST.get('siswa_id')
        buku_id        = request.POST.get('buku_id')
        tanggal_pinjam = request.POST.get('tanggal_pinjam')
        jatuh_tempo    = request.POST.get('jatuh_tempo')
        keperluan      = request.POST.get('keperluan', '').strip()
        status         = 'dipinjam'

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO peminjaman (siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status])
        return redirect('peminjaman_list')

    return render(request, 'peminjaman_form.html', {
        'siswa_list': siswa_list,
        'buku_list': buku_list,
    })

def peminjaman_update(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM peminjaman WHERE id = %s", [id])
        peminjaman = dictfetchone(cursor)
        cursor.execute("SELECT id, nama FROM siswa WHERE is_active = TRUE ORDER BY nama")
        siswa_list = dictfetchall(cursor)
        cursor.execute("SELECT id, judul FROM buku ORDER BY judul")
        buku_list = dictfetchall(cursor)

    if request.method == 'POST':
        siswa_id       = request.POST.get('siswa_id')
        buku_id        = request.POST.get('buku_id')
        tanggal_pinjam = request.POST.get('tanggal_pinjam')
        jatuh_tempo    = request.POST.get('jatuh_tempo')
        keperluan      = request.POST.get('keperluan', '').strip()
        status         = request.POST.get('status')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE peminjaman
                SET siswa_id=%s, buku_id=%s, tanggal_pinjam=%s,
                    jatuh_tempo=%s, keperluan=%s, status=%s
                WHERE id = %s
            """, [siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, status, id])
        return redirect('peminjaman_list')

    return render(request, 'peminjaman_update.html', {
        'peminjaman': peminjaman,
        'siswa_list': siswa_list,
        'buku_list': buku_list,
    })

def peminjaman_delete(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, s.nama AS nama_siswa, b.judul AS judul_buku
            FROM peminjaman p
            JOIN siswa s ON s.id = p.siswa_id
            JOIN buku b ON b.id = p.buku_id
            WHERE p.id = %s
        """, [id])
        peminjaman = dictfetchone(cursor)

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM peminjaman WHERE id = %s", [id])
        return redirect('peminjaman_list')

    return render(request, 'peminjaman_delete.html', {'peminjaman': peminjaman})

def peminjaman_kembalikan(request, id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE peminjaman SET status = 'dikembalikan' WHERE id = %s
            """, [id])
    return redirect('peminjaman_list')