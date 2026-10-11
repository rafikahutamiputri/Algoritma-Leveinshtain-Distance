"""Aplikasi pencarian barang menggunakan jarak Levenshtein."""

import csv
from pathlib import Path

# Mengambil dua fungsi dari file inti.
# Algoritma Levenshtein tidak ditulis ulang di file aplikasi ini.
from Kode_Inti import levenshtein, normalisasi


# Pencarian menampilkan barang dengan jarak maksimal 2,
# dan paling banyak 3 hasil.
BATAS_JARAK = 2
MAKSIMUM_HASIL = 3

# Lokasi CSV mengikuti folder tempat file aplikasi ini disimpan.
FILE_DATA = Path(__file__).resolve().parent / "data_inventaris.csv"


def baca_inventaris(lokasi_file=FILE_DATA):
    """Membaca data barang dari CSV dan menyimpannya sebagai list."""
    katalog = []

    # newline="" membantu csv membaca baris dengan benar.
    # utf-8-sig juga dapat membaca CSV yang memiliki penanda BOM.
    with Path(lokasi_file).open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        pembaca = csv.DictReader(file)

        # Nama dan urutan kolom CSV harus sesuai dengan data yang digunakan.
        if pembaca.fieldnames != ["kode", "nama", "stok"]:
            raise ValueError(
                "Judul kolom CSV harus: kode,nama,stok"
            )

        # Baris data pertama bernomor 2 karena baris 1 adalah judul kolom.
        for nomor_baris, baris in enumerate(pembaca, start=2):

            # Memeriksa apakah jumlah kolom pada baris tersebut sesuai.
            if None in baris or any(
                nilai is None for nilai in baris.values()
            ):
                raise ValueError(
                    f"Jumlah kolom tidak sesuai pada baris {nomor_baris}."
                )

            try:
                kode = baris["kode"].strip()
                nama = baris["nama"].strip()
                stok = int(baris["stok"].strip())
            except (AttributeError, TypeError, ValueError):
                raise ValueError(
                    f"Isi data tidak sesuai pada baris {nomor_baris}."
                ) from None

            if not kode or not nama:
                raise ValueError(
                    f"Kode dan nama barang tidak boleh kosong "
                    f"(baris {nomor_baris})."
                )

            if stok < 0:
                raise ValueError(
                    f"Stok tidak boleh negatif (baris {nomor_baris})."
                )

            # Setiap barang disimpan sebagai dictionary.
            katalog.append({
                "kode": kode,
                "nama": nama,
                "stok": stok
            })

    return katalog


def cari_barang(kata_kunci, katalog):
    """Mencari nama barang yang jaraknya tidak melebihi batas."""

    # Samakan format kueri lebih dulu, misalnya huruf besar-kecil
    # dan spasi berlebih.
    kueri = normalisasi(kata_kunci)

    # Kueri kosong tidak digunakan untuk mencari.
    if not kueri:
        return []

    hasil = []

    # Periksa nama setiap barang di dalam katalog.
    for barang in katalog:
        nama_normal = normalisasi(barang["nama"])

        # Memanggil algoritma dari file inti untuk mengukur jarak.
        jarak = levenshtein(kueri, nama_normal)

        # Hanya simpan barang yang jaraknya masih dalam batas.
        if jarak <= BATAS_JARAK:
            hasil.append({
                "kode": barang["kode"],
                "nama": barang["nama"],
                "stok": barang["stok"],
                "jarak": jarak
            })

    # Urutan hasil:
    # 1. Jarak terkecil.
    # 2. Nama barang secara alfabetis jika jaraknya sama.
    # 3. Kode barang jika nama dan jaraknya sama.
    hasil.sort(key=lambda barang: (
        barang["jarak"],
        normalisasi(barang["nama"]),
        barang["kode"]
    ))

    # Ambil paling banyak sejumlah MAKSIMUM_HASIL.
    return hasil[:MAKSIMUM_HASIL]


def tampilkan_hasil(hasil):
    """Menampilkan hasil pencarian dalam bentuk tabel di terminal."""

    if not hasil:
        print("Tidak ada barang yang sesuai dengan batas jarak.")
        return

    # Mengatur lebar kolom nama agar tabel mudah dibaca.
    lebar_nama = max(
        len("Nama"),
        max(len(barang["nama"]) for barang in hasil)
    )

    print()
    print(
        f"{'Kode':<10} "
        f"{'Nama':<{lebar_nama}} "
        f"{'Stok':>6} "
        f"{'Jarak':>6}"
    )

    for barang in hasil:
        print(
            f"{barang['kode']:<10} "
            f"{barang['nama']:<{lebar_nama}} "
            f"{barang['stok']:>6} "
            f"{barang['jarak']:>6}"
        )


def main():
    """Menjalankan aplikasi pencarian barang."""

    try:
        katalog = baca_inventaris()
    except (OSError, csv.Error, ValueError) as kesalahan:
        print(f"Data inventaris tidak dapat dibaca: {kesalahan}")
        return

    if not katalog:
        print("Data inventaris masih kosong.")
        return

    print("PENCARIAN BARANG — LEVENSHTEIN")
    print(f"Batas jarak: {BATAS_JARAK}")
    print(f"Maksimum hasil: {MAKSIMUM_HASIL}")
    print("Ketik :keluar untuk mengakhiri program.")

    while True:
        kata_kunci = input("\nMasukkan nama barang: ")

        if kata_kunci.strip().casefold() == ":keluar":
            print("Program selesai.")
            break

        if not normalisasi(kata_kunci):
            print("Kata kunci tidak boleh kosong.")
            continue

        hasil = cari_barang(kata_kunci, katalog)
        tampilkan_hasil(hasil)


# Bagian ini membuat main() berjalan saat file dijalankan langsung,
# tetapi tidak berjalan otomatis saat file diimpor oleh file lain.
if __name__ == "__main__":
    main()