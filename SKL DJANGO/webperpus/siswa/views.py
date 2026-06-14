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

def siswa_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nama, kelas, nis, is_active FROM siswa ORDER BY id ASC")
        data_siswa = dictfetchall(cursor)
    return render(request, 'siswa_list.html', {'siswa_list': data_siswa})

def siswa_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM siswa WHERE id = %s", [id])
        siswa = dictfetchone(cursor)
    return render(request, 'siswa_detail.html', {'siswa': siswa})

def siswa_create(request):
    if request.method == 'POST':
        nama      = request.POST.get('nama', '').strip()
        kelas     = request.POST.get('kelas', '').strip()
        nis       = request.POST.get('nis', '').strip()
        is_active = request.POST.get('is_active') == 'on'

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO siswa (nama, kelas, nis, is_active)
                VALUES (%s, %s, %s, %s)
            """, [nama, kelas, nis, is_active])
        return redirect('siswa_list')
    return render(request, 'siswa_form.html')

def siswa_update(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM siswa WHERE id = %s", [id])
        siswa = dictfetchone(cursor)

    if request.method == 'POST':
        nama      = request.POST.get('nama', '').strip()
        kelas     = request.POST.get('kelas', '').strip()
        nis       = request.POST.get('nis', '').strip()
        is_active = request.POST.get('is_active') == 'on'

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE siswa SET nama=%s, kelas=%s, nis=%s, is_active=%s
                WHERE id = %s
            """, [nama, kelas, nis, is_active, id])
        return redirect('siswa_list')
    return render(request, 'siswa_update.html', {'siswa': siswa})

def siswa_delete(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM siswa WHERE id = %s", [id])
        siswa = dictfetchone(cursor)

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM siswa WHERE id = %s", [id])
        return redirect('siswa_list')
    return render(request, 'siswa_delete.html', {'siswa': siswa})