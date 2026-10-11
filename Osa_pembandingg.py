"""Implementasi mandiri algoritma Optimal String Alignment (OSA).

OSA digunakan sebagai algoritma pembanding terhadap Levenshtein.
Fungsi ini menghitung sisip, hapus, ganti, dan pertukaran dua karakter
bersebelahan dengan biaya satu.
"""


def osa(asal, tujuan):
    """Menghitung jarak OSA antara string asal dan string tujuan.

    Fungsi ini menerima teks apa adanya. Jika normalisasi diperlukan,
    pemanggil melakukannya sebelum memanggil fungsi ini.

    Waktu dan ruang: Theta((m + 1) * (n + 1)).
    """
    m = len(asal)
    n = len(tujuan)

    # D menyimpan jarak untuk setiap pasangan prefix asal dan tujuan.
    # Baris 0 dan kolom 0 mewakili perbandingan dengan string kosong.
    D = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    # Menghapus seluruh karakter dari prefix asal untuk mencapai string kosong.
    for r in range(m + 1):
        D[r][0] = r

    # Menyisipkan seluruh karakter prefix tujuan dari string kosong.
    for c in range(n + 1):
        D[0][c] = c

    # Isi tabel dari kiri ke kanan, lalu lanjut ke baris berikutnya.
    for r in range(1, m + 1):
        for c in range(1, n + 1):
            # Karakter sama tidak menambah biaya; karakter berbeda perlu diganti.
            biaya = 0 if asal[r - 1] == tujuan[c - 1] else 1

            # Tiga operasi dasar yang juga digunakan Levenshtein.
            dari_atas = D[r - 1][c] + 1       # Hapus satu karakter.
            dari_kiri = D[r][c - 1] + 1       # Sisip satu karakter.
            dari_diagonal = D[r - 1][c - 1] + biaya  # Sama atau ganti.

            # Pilih biaya terkecil dari operasi dasar.
            biaya_terkecil = dari_atas
            if dari_kiri < biaya_terkecil:
                biaya_terkecil = dari_kiri
            if dari_diagonal < biaya_terkecil:
                biaya_terkecil = dari_diagonal

            D[r][c] = biaya_terkecil

            # OSA menambahkan satu operasi: menukar dua karakter bersebelahan.
            # Syarat ini memastikan dua karakter tersebut benar-benar tertukar.
            if (
                r > 1
                and c > 1
                and asal[r - 1] == tujuan[c - 2]
                and asal[r - 2] == tujuan[c - 1]
            ):
                biaya_transposisi = D[r - 2][c - 2] + 1

                # Gunakan transposisi hanya jika biayanya lebih kecil.
                if biaya_transposisi < D[r][c]:
                    D[r][c] = biaya_transposisi

    # Sel terakhir berisi jarak untuk kedua string secara utuh.
    return D[m][n]


if __name__ == "__main__":
    print("PERHITUNGAN OPTIMAL STRING ALIGNMENT (OSA)")

    asal = input("Masukkan string asal   : ")
    tujuan = input("Masukkan string tujuan : ")

    jarak = osa(asal, tujuan)

    print(f"\nJarak OSA antara '{asal}' dan '{tujuan}' = {jarak}")
