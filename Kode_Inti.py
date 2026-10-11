"""Samakan huruf dan rapikan spasi, ini tidak memperbaiki typo/sinomim"""
def normalisasi(teks):
    if not isinstance(teks, str):
        raise TypeError("Teks harus berupa String")
    return " ".join(teks.casefold().split())

"""Fungsi Inti Leveinshtein (Algoritma Wagner-Fischer) 
    : untuk menghitung jarak perbedaan dua string."""
def levenshtein(asal, tujuan):
    m = len(asal)
    n = len(tujuan)

    # Membuat matriks D berukuran (m + 1) x (n + 1) berisi 0.
    D = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    # Kolom pertama: menghapus karakter asal hingga menjadi string kosong.
    for r in range(m + 1):
        D[r][0] = r

    # Baris pertama: menyisipkan karakter tujuan dari string kosong.
    for c in range(n + 1):
        D[0][c] = c

    # Mengisi matriks dari kiri ke kanan dan dari atas ke bawah.
    for r in range(1, m + 1):
        for c in range(1, n + 1):
            # Jika karakter sama, biaya 0; jika beda, biaya 1 (ganti)
            biaya = 0 if asal[r - 1] == tujuan[c - 1] else 1
            
            dari_atas = D[r - 1][c] + 1       # Operasi Hapus
            dari_kiri = D[r][c - 1] + 1       # Operasi Sisip
            dari_diagonal = D[r - 1][c - 1] + biaya  # Operasi Ganti/Tetap

            # Mencari nilai minimum dari ketiga operasi di atas
            biaya_terkecil = dari_atas
            if dari_kiri < biaya_terkecil:
                biaya_terkecil = dari_kiri
            if dari_diagonal < biaya_terkecil:
                biaya_terkecil = dari_diagonal
            D[r][c] = biaya_terkecil

    return D[m][n]  # Mengembalikan jarak akhir minimum (selisih karakter) 


