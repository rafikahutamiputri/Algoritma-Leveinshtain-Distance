"""Implementasi & Eksperimen"""

import csv
from datetime import datetime
from importlib import import_module
from pathlib import Path
import platform
import random
import statistics
import string
import subprocess
import time

from Osa_pembandingg import osa
from Kode_Inti import levenshtein, normalisasi

ALGORITMA = {"Levenshtein": levenshtein, "OSA": osa}
FOLDER_PROGRAM = Path(__file__).resolve().parent
FILE_DATA = FOLDER_PROGRAM / "data_inventaris.csv"

# 2 pengaturan ini sama dgn Aplikasi_Pencarian.py
BATAS_JARAK = 2
MAKSIMUM_HASIL = 3
UKURAN_L = (10, 20, 40, 80, 160)  # m = n = L.
UKURAN_N = (20, 40, 60, 80, 100)  # Banyak barang dalam katalog.
PENGULANGAN = 10
BATCH_INTI = 20
BATCH_KATALOG = 10
SEED_DATA = 246024

"""Baca CSV dengan kolom kode,nama,stok seperti aplikasi pencarian."""
def baca_inventaris(lokasi):
    katalog = []
    kode_terpakai = set()
    with lokasi.open("r", encoding="utf-8-sig", newline="") as file:
        pembaca = csv.DictReader(file)
        if pembaca.fieldnames != ["kode", "nama", "stok"]:
            raise ValueError("Kolom CSV harus berurutan: kode,nama,stok")

        for nomor, baris in enumerate(pembaca, start=2):
            if None in baris or any(isi is None for isi in baris.values()):
                raise ValueError(f"Jumlah kolom salah pada baris {nomor}.")
            try:
                kode = baris["kode"].strip()
                nama = baris["nama"].strip()
                stok = int(baris["stok"].strip())
            except (AttributeError, TypeError, ValueError):
                raise ValueError(f"Isi data salah pada baris {nomor}.") from None

            if not kode or not normalisasi(nama) or stok < 0:
                raise ValueError(f"Kode/nama kosong atau stok negatif: baris {nomor}.")
            if kode in kode_terpakai:
                raise ValueError(f"Kode {kode} berulang pada baris {nomor}.")
            katalog.append({"kode": kode, "nama": nama, "stok": stok})
            kode_terpakai.add(kode)
    return katalog


"""Menggunakan aplikasi yang sama untuk kedua algoritma.
    Semua nama lengkap dibandingkan; batas diterapkan setelah jarak dihitung.
    Setelah diurutkan, baru ambil paling banyak 'maksimum' hasil.
    """
def cari_barang(kata_kunci, katalog, fungsi_jarak, batas, maksimum):
    asal = normalisasi(kata_kunci)
    if not asal:
        return []

    hasil = []
    for barang in katalog:
        tujuan = normalisasi(barang["nama"])
        jarak = fungsi_jarak(asal, tujuan)
        if jarak <= batas:
            hasil.append({**barang, "jarak": jarak})

    hasil.sort(key=lambda barang: (
        barang["jarak"], normalisasi(barang["nama"]), barang["kode"]
    ))
    return hasil[:maksimum]

"""Menyimpan tabel agar dapat dibuka di Excel tanpa mengubah hasil hitung."""
def tulis_csv(lokasi, baris):
    if not baris:
        raise ValueError(f"Tabel kosong: {lokasi.name}")
    with lokasi.open("w", encoding="utf-8-sig", newline="") as file:
        penulis = csv.DictWriter(file, fieldnames=list(baris[0]))
        penulis.writeheader()
        penulis.writerows(baris)

"""Bentuk tabel teks untuk terminal dan ringkasan laporan."""
def tabel_markdown(baris, kolom):
    isi = ["| " + " | ".join(kolom) + " |",
        "| " + " | ".join("---" for _ in kolom) + " |"]
    for data in baris:
        nilai = []
        for nama in kolom:
            angka = data[nama]
            nilai.append(f"{angka:.6f}" if isinstance(angka, float) else str(angka))
        isi.append("| " + " | ".join(nilai) + " |")
    return "\n".join(isi)

"""Temukan kode barang dari nama, yang sesuai dengan dataset inventaris."""
def kode_target(katalog, nama):
    for barang in katalog:
        if normalisasi(barang["nama"]) == normalisasi(nama):
            return barang["kode"]
    raise ValueError(f"Barang '{nama}' tidak ada di data_inventaris.csv.")


"""Menguji Tiga kasus kecil dengan hasil yang dapat dihitung manual."""
def uji_tiga_kasus(katalog):
    kasus = [
        ("Penyisipan", "proyktor", "proyektor", 1, 1),
        ("Penggantian", "mause", "mouse", 1, 1),
        ("Transposisi", "keybaord", "keyboard", 2, 1),
    ]
    baris = []
    for jenis, asal, tujuan, harapan_l, harapan_o in kasus:
        target = kode_target(katalog, tujuan)
        for nama, fungsi in ALGORITMA.items():
            harapan = harapan_l if nama == "Levenshtein" else harapan_o
            jarak = fungsi(normalisasi(asal), normalisasi(tujuan))
            if jarak != harapan:
                raise RuntimeError(
                    f"Kasus {jenis} gagal: {nama} menghasilkan {jarak}, "
                    f"seharusnya {harapan}."
                )
            hasil_batas_1 = cari_barang(asal, katalog, fungsi, 1, MAKSIMUM_HASIL)
            baris.append({
                "kasus": jenis, "asal": asal, "tujuan": tujuan,
                "algoritma": nama, "jarak_harapan": harapan,
                "jarak_hasil": jarak, "kode_target": target,
                "target_tampil_batas_1": any(
                    barang["kode"] == target for barang in hasil_batas_1
                ),
                "status": "LULUS",
            })
    return baris

"""Buat dua string a-z tetap; tiap L memakai awalan string yang sama."""
def buat_pasangan_string():
    pembangkit = random.Random(SEED_DATA)
    asal = "".join(pembangkit.choice(string.ascii_lowercase)
                for _ in range(max(UKURAN_L)))
    tujuan = "".join(pembangkit.choice(string.ascii_lowercase)
                for _ in range(max(UKURAN_L)))
    return [{"L": L, "asal": asal[:L], "tujuan": tujuan[:L]}
            for L in UKURAN_L]

"""Perluas sepuluh nama asli dengan nomor sintetis dua digit."""
def buat_katalog_skala(katalog, N):
    if len(katalog) != 10 or N % 10 != 0:
        raise ValueError("Uji skala memerlukan 10 nama dasar dan N kelipatan 10.")
    hasil = []
    for nomor in range(1, N // 10 + 1):
        for barang in katalog:
            hasil.append({
                "kode": f"UJI{len(hasil) + 1:03d}",
                "nama": f"{barang['nama']} {nomor:02d}",
                "stok": barang["stok"],
            })
    return hasil


"""Ukur satu kondisi lima kali untuk tiap algoritma.
    Satu pengulangan menghasilkan satu sampel: durasi satu batch dibagi
    jumlah pencarian/perhitungan di dalam batch. Statistik memakai lima
    sampel pengulangan, bukan setiap panggilan dalam batch."""
def ukur_kondisi(jenis, ukuran, operasi, batch, panggilan_per_operasi=1):
    if PENGULANGAN < 5 or batch < 1 or panggilan_per_operasi < 1:
        raise ValueError("Perlu >=5 pengulangan dan ukuran batch positif.")

    sampel = {nama: [] for nama in operasi}
    mentah = []

    # Satu batch pemanasan per algoritma, tanpa memasukkannya ke hasil.
    for fungsi in operasi.values():
        for _ in range(batch):
            fungsi()

    nama_algoritma = list(operasi)
    for ulang in range(1, PENGULANGAN + 1):
        # Balik urutan agar algoritma yang sama tidak selalu diuji pertama.
        urutan = nama_algoritma if ulang % 2 else nama_algoritma[::-1]
        for posisi, nama in enumerate(urutan, start=1):
            mulai = time.perf_counter_ns()
            for _ in range(batch):
                operasi[nama]()
            durasi_ns = time.perf_counter_ns() - mulai
            banyak_panggilan = batch * panggilan_per_operasi
            waktu_ms = durasi_ns / banyak_panggilan / 1_000_000
            sampel[nama].append(waktu_ms)
            mentah.append({
                "pengujian": jenis, "ukuran": ukuran, "algoritma": nama,
                "pengulangan": ulang, "urutan": posisi,
                "panggilan_per_batch": banyak_panggilan,
                "waktu_batch_ns": durasi_ns,
                "waktu_per_panggilan_ms": waktu_ms,
            })

    ringkasan = []
    for nama, nilai in sampel.items():
        ringkasan.append({
            "pengujian": jenis, "ukuran": ukuran, "algoritma": nama,
            "pengulangan": PENGULANGAN,
            "panggilan_per_batch": batch * panggilan_per_operasi,
            "rata_rata_ms": statistics.mean(nilai),
            "simpangan_baku_ms": statistics.stdev(nilai),
        })
    return mentah, ringkasan

"""Lima kueri simulasi dengan barang tujuan yang sudah diketahui."""
def kueri_berlabel(katalog):
    contoh = [
        ("proyktor", "proyektor"), ("mause", "mouse"),
        ("keybaord", "keyboard"), ("monitro", "monitor"),
        ("webacm", "webcam"),
    ]
    return [{"kueri": kueri, "nama_target": nama,
            "kode_target": kode_target(katalog, nama)}
            for kueri, nama in contoh]


"""Catat lingkungan komputer yang benar-benar menjalankan eksperimen."""
def informasi_lingkungan():
    cpu = platform.processor().strip()
    if platform.system() == "Windows":
        # PowerShell bawaan Windows membaca nama model CPU; tanpa pustaka lain.
        try:
            proses = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command",
            "(Get-CimInstance Win32_Processor | "
            "Select-Object -First 1 -ExpandProperty Name)"],
                capture_output=True, text=True, timeout=10, check=True,
            )
            cpu = proses.stdout.strip() or cpu
        except (OSError, subprocess.SubprocessError):
            pass

    jam = time.get_clock_info("perf_counter")
    return [
        {"komponen": "Waktu lokal", "nilai": datetime.now().astimezone().isoformat()},
        {"komponen": "Sistem operasi", "nilai": platform.platform()},
        {"komponen": "CPU", "nilai": cpu or "Tidak terdeteksi; periksa Task Manager"},
        {"komponen": "Python yang digunakan", "nilai": platform.python_version()},
        {"komponen": "Timer", "nilai": "time.perf_counter_ns()"},
        {"komponen": "Resolusi timer (detik)", "nilai": f"{jam.resolution:.3e}"},
        {"komponen": "Eksekusi", "nilai": "Satu proses, berurutan"},
    ]

"""Gambar waktu terukur dan bentuk teori yang diskalakan di titik terbesar."""
def buat_grafik(plt, ringkasan, pengujian, parameter, pangkat, judul, lokasi):
    fig, ax = plt.subplots(figsize=(8, 5))
    kurva = []
    warna = {"Levenshtein": "tab:blue", "OSA": "tab:orange"}
    for nama in ALGORITMA:
        data = sorted(
            (x for x in ringkasan
            if x["pengujian"] == pengujian and x["algoritma"] == nama),
            key=lambda x: x["ukuran"],
        )
        ukuran = [x["ukuran"] for x in data]
        rata = [x["rata_rata_ms"] for x in data]
        sd = [x["simpangan_baku_ms"] for x in data]
        skala = rata[-1] / (ukuran[-1] ** pangkat)

        ax.errorbar(ukuran, rata, yerr=sd, marker="o", capsize=3,
                    color=warna[nama], label=f"{nama} (rata-rata ± SD)")
        rentang = range(ukuran[0], ukuran[-1] + 1)
        ax.plot(list(rentang), [skala * x ** pangkat for x in rentang],
                "--", color=warna[nama], alpha=0.7,
                label=f"{nama}: acuan {parameter}^{pangkat}")

        for x in ukuran:
            kurva.append({
                "pengujian": pengujian, "algoritma": nama,
                "ukuran": x, "pangkat": pangkat,
                "konstanta_skala": skala,
                "waktu_teoretis_ms": skala * x ** pangkat,
            })

    ax.set(title=judul, xlabel=f"Ukuran input ({parameter})",
        ylabel="Waktu per panggilan (ms)")
    ax.set_xticks(list(UKURAN_L if pengujian == "panjang_string" else UKURAN_N))
    ax.set_ylim(bottom=0)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(lokasi, dpi=180)
    plt.close(fig)
    return kurva


"""Jalankan seluruh eksperimen dan simpan hasil sesi ini."""
def main():  
    try:
        import matplotlib
        matplotlib.use("Agg")  # Simpan PNG meskipun tanpa jendela grafik.
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib belum ada. Jalankan: python -m pip install matplotlib")
        return 1

    try:
        katalog = baca_inventaris(FILE_DATA)
        if len(katalog) != 10:
            raise ValueError("Eksperimen standar memerlukan 10 barang dasar.")
        kasus = uji_tiga_kasus(katalog)
        kueri = kueri_berlabel(katalog)
    except (OSError, ValueError, RuntimeError, csv.Error) as kesalahan:
        print(f"Persiapan eksperimen gagal: {kesalahan}")
        return 1

    # Folder baru per sesi: hasil lama tidak tertimpa saat eksperimen diulang.
    waktu_sesi = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    folder = FOLDER_PROGRAM / "Hasil Eksperimen" / waktu_sesi
    folder.mkdir(parents=True, exist_ok=False)
    lingkungan = informasi_lingkungan()
    lingkungan.append({"komponen": "Matplotlib", "nilai": matplotlib.__version__})

    tulis_csv(folder / "lingkungan_uji.csv", lingkungan)
    tulis_csv(folder / "katalog_dasar.csv", katalog)
    tulis_csv(folder / "hasil_tiga_kasus.csv", kasus)
    tulis_csv(folder / "kueri_sensitivitas.csv", kueri)

    semua_mentah = []
    semua_ringkasan = []
    pasangan = buat_pasangan_string()
    tulis_csv(folder / "pasangan_input.csv", pasangan)

    # Uji 1: pertumbuhan waktu fungsi inti ketika m = n = L.
    for data in pasangan:
        L, asal, tujuan = data["L"], data["asal"], data["tujuan"]
        print(f"Uji panjang string: L={L}", flush=True)
        operasi = {
            nama: (lambda f=fungsi, a=asal, t=tujuan: f(a, t))
            for nama, fungsi in ALGORITMA.items()
        }
        mentah, ringkasan = ukur_kondisi(
            "panjang_string", L, operasi, BATCH_INTI
        )
        semua_mentah.extend(mentah)
        semua_ringkasan.extend(ringkasan)

    # Uji 2: pertumbuhan waktu pencarian terhadap jumlah barang N.
    for N in UKURAN_N:
        katalog_N = buat_katalog_skala(katalog, N)
        tulis_csv(folder / f"katalog_skala_{N}.csv", katalog_N)
        print(f"Uji banyak barang: N={N}", flush=True)
        operasi = {
            nama: (lambda f=fungsi, data=katalog_N:
                cari_barang("proyktor 01", data, f,
                            BATAS_JARAK, MAKSIMUM_HASIL))
            for nama, fungsi in ALGORITMA.items()
        }
        mentah, ringkasan = ukur_kondisi(
            "jumlah_barang", N, operasi, BATCH_KATALOG
        )
        semua_mentah.extend(mentah)
        semua_ringkasan.extend(ringkasan)

    # Sensitivitas 1: ubah batas jarak, gunakan kueri dan katalog yang sama.
    sensitivitas_batas = []
    for batas in (0, 1, 2, 3):
        print(f"Uji sensitivitas batas: {batas}", flush=True)
        operasi = {
            nama: (lambda f=fungsi, b=batas:
                [cari_barang(x["kueri"], katalog, f, b, MAKSIMUM_HASIL)
                    for x in kueri])
            for nama, fungsi in ALGORITMA.items()
        }
        mentah, ringkasan = ukur_kondisi(
            "sensitivitas_batas", batas, operasi, 1, len(kueri)
        )
        semua_mentah.extend(mentah)
        semua_ringkasan.extend(ringkasan)
        for nama, fungsi in ALGORITMA.items():
            hasil_semua = operasi[nama]()
            ditemukan = sum(
                any(barang["kode"] == x["kode_target"] for barang in hasil)
                for x, hasil in zip(kueri, hasil_semua)
            )
            sensitivitas_batas.append({
                "algoritma": nama, "batas": batas,
                "maksimum": MAKSIMUM_HASIL, "jumlah_kueri": len(kueri),
                "target_ditemukan": ditemukan,
                "jumlah_saran": sum(len(hasil) for hasil in hasil_semua),
            })

    # Sensitivitas 2: katalog khusus membuat efek maksimum hasil terlihat.
    # Semua nama di bawah ini adalah data simulasi, bukan barang inventaris.
    nama_khusus = ["Mouse", "Mouse A", "Mouse B",
                "Mouse C", "Mouse D", "Mouse E"]
    katalog_khusus = [
        {"kode": f"SYN{k:03d}", "nama": nama, "stok": 1}
        for k, nama in enumerate(nama_khusus, start=1)
    ]
    tulis_csv(folder / "katalog_khusus_maksimum.csv", katalog_khusus)
    sensitivitas_maksimum = []
    for maksimum in (1, 3, 5):
        print(f"Uji sensitivitas maksimum: {maksimum}", flush=True)
        operasi = {
            nama: (lambda f=fungsi, batas=BATAS_JARAK, banyak=maksimum:
                cari_barang("mouse", katalog_khusus, f, batas, banyak))
            for nama, fungsi in ALGORITMA.items()
        }
        mentah, ringkasan = ukur_kondisi(
            "sensitivitas_maksimum", maksimum, operasi, BATCH_KATALOG
        )
        semua_mentah.extend(mentah)
        semua_ringkasan.extend(ringkasan)
        for nama, fungsi in ALGORITMA.items():
            hasil = operasi[nama]()
            semua_lolos = cari_barang(
                "mouse", katalog_khusus, fungsi, BATAS_JARAK,
                len(katalog_khusus)
            )
            sensitivitas_maksimum.append({
                "algoritma": nama, "batas": BATAS_JARAK,
                "maksimum": maksimum, "kandidat_lolos": len(semua_lolos),
                "hasil_tampil": len(hasil),
                "kode_tampil": ", ".join(x["kode"] for x in hasil),
            })

    # Menulis CSV dan membuat grafik dilakukan setelah seluruh timer berhenti.
    tulis_csv(folder / "waktu_mentah.csv", semua_mentah)
    tulis_csv(folder / "waktu_ringkasan.csv", semua_ringkasan)
    tulis_csv(folder / "sensitivitas_batas.csv", sensitivitas_batas)
    tulis_csv(folder / "sensitivitas_maksimum.csv", sensitivitas_maksimum)

    kurva = buat_grafik(
        plt, semua_ringkasan, "panjang_string", "L", 2,
        "Waktu fungsi inti dan acuan L²",
        folder / "grafik_waktu_panjang.png",
    )
    kurva += buat_grafik(
        plt, semua_ringkasan, "jumlah_barang", "N", 1,
        "Waktu pencarian dan acuan komponen pemindaian N",
        folder / "grafik_waktu_katalog.png",
    )
    tulis_csv(folder / "kurva_teoretis.csv", kurva)

    kolom_kasus = ["kasus", "asal", "tujuan", "algoritma",
                "jarak_hasil", "target_tampil_batas_1", "status"]
    kolom_waktu = ["pengujian", "ukuran", "algoritma",
                "rata_rata_ms", "simpangan_baku_ms"]
    bagian = [
        "# Hasil eksperimen BAB 4",
        "Hasil ini berasal dari komputer yang menjalankan skrip",
        "## Lingkungan uji",
        tabel_markdown(lingkungan, ["komponen", "nilai"]),
        "## Tiga studi kasus",
        tabel_markdown(kasus, kolom_kasus),
        "## Waktu: rata-rata dan simpangan baku (ms)",
        tabel_markdown(semua_ringkasan, kolom_waktu),
        "## Sensitivitas batas jarak",
        tabel_markdown(sensitivitas_batas,
                    ["algoritma", "batas", "jumlah_kueri",
                        "target_ditemukan", "jumlah_saran"]),
        "## Sensitivitas maksimum hasil (katalog sintetis khusus)",
        tabel_markdown(sensitivitas_maksimum,
                    ["algoritma", "maksimum", "kandidat_lolos",
                        "hasil_tampil", "kode_tampil"]),
        f"Setiap kondisi waktu diulang {PENGULANGAN} kali. Satu sampel adalah durasi "
        f"satu batch dibagi jumlah panggilan dalam batch; simpangan baku "
        f"menggunakan {PENGULANGAN} sampel (penyebut n-1).",
        "Pasangan string acak dibuat dengan seed 246024. Kedua algoritma "
        "deterministik; seed hanya menetapkan data input. Hasil antarrun "
        "yang dapat bervariasi adalah waktu eksekusi.",
        "Kurva L² dan N diskalakan agar melewati rata-rata pada ukuran "
        "terbesar. Kurva itu acuan visual, bukan pembuktian kompleksitas. "
        "Untuk pencarian, N menggambarkan komponen pemindaian; pengurutan "
        "kandidat juga ikut terukur.",
        "Uji batas dan maksimum adalah sensitivitas parameter aplikasi, "
        "bukan parameter metaheuristik atau machine learning.",
    ]
    (folder / "ringkasan_hasil.md").write_text(
        "\n\n".join(bagian) + "\n", encoding="utf-8"
    )

    print("\nTIGA STUDI KASUS")
    print(tabel_markdown(kasus, kolom_kasus))
    print("\nRATA-RATA DAN SIMPANGAN BAKU WAKTU (ms)")
    print(tabel_markdown(semua_ringkasan, kolom_waktu))
    print("\nSENSITIVITAS BATAS")
    print(tabel_markdown(
        sensitivitas_batas,
        ["algoritma", "batas", "target_ditemukan", "jumlah_saran"],
    ))
    print("\nSENSITIVITAS MAKSIMUM")
    print(tabel_markdown(
        sensitivitas_maksimum,
        ["algoritma", "maksimum", "kandidat_lolos", "hasil_tampil"],
    ))
    print(f"\nTabel, grafik PNG, dan ringkasan tersimpan di: {folder}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())