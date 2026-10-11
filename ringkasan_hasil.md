# Hasil eksperimen BAB 4

Hasil ini berasal dari komputer yang menjalankan skrip

## Lingkungan uji

| komponen | nilai |
| --- | --- |
| Waktu lokal | 2026-10-11T07:20:57.613152+08:00 |
| Sistem operasi | Windows-11-10.0.26200-SP0 |
| CPU | 11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz |
| Python yang digunakan | 3.14.7 |
| Timer | time.perf_counter_ns() |
| Resolusi timer (detik) | 1.000e-07 |
| Eksekusi | Satu proses, berurutan |
| Matplotlib | 3.11.2 |

## Tiga studi kasus

| kasus | asal | tujuan | algoritma | jarak_hasil | target_tampil_batas_1 | status |
| --- | --- | --- | --- | --- | --- | --- |
| Penyisipan | proyktor | proyektor | Levenshtein | 1 | True | LULUS |
| Penyisipan | proyktor | proyektor | OSA | 1 | True | LULUS |
| Penggantian | mause | mouse | Levenshtein | 1 | True | LULUS |
| Penggantian | mause | mouse | OSA | 1 | True | LULUS |
| Transposisi | keybaord | keyboard | Levenshtein | 2 | False | LULUS |
| Transposisi | keybaord | keyboard | OSA | 1 | True | LULUS |

## Waktu: rata-rata dan simpangan baku (ms)

| pengujian | ukuran | algoritma | rata_rata_ms | simpangan_baku_ms |
| --- | --- | --- | --- | --- |
| panjang_string | 10 | Levenshtein | 0.048564 | 0.006683 |
| panjang_string | 10 | OSA | 0.056426 | 0.000441 |
| panjang_string | 20 | Levenshtein | 0.183726 | 0.026669 |
| panjang_string | 20 | OSA | 0.220436 | 0.014622 |
| panjang_string | 40 | Levenshtein | 0.643876 | 0.066359 |
| panjang_string | 40 | OSA | 0.830512 | 0.017235 |
| panjang_string | 80 | Levenshtein | 2.499716 | 0.050224 |
| panjang_string | 80 | OSA | 3.356930 | 0.164550 |
| panjang_string | 160 | Levenshtein | 10.049190 | 0.303762 |
| panjang_string | 160 | OSA | 13.617544 | 1.410844 |
| jumlah_barang | 20 | Levenshtein | 1.051008 | 0.055721 |
| jumlah_barang | 20 | OSA | 1.288400 | 0.014924 |
| jumlah_barang | 40 | Levenshtein | 2.135226 | 0.107473 |
| jumlah_barang | 40 | OSA | 2.619628 | 0.087662 |
| jumlah_barang | 60 | Levenshtein | 3.090189 | 0.029061 |
| jumlah_barang | 60 | OSA | 3.897390 | 0.090964 |
| jumlah_barang | 80 | Levenshtein | 4.321647 | 0.262848 |
| jumlah_barang | 80 | OSA | 5.446493 | 0.305234 |
| jumlah_barang | 100 | Levenshtein | 5.248869 | 0.249672 |
| jumlah_barang | 100 | OSA | 6.618015 | 0.179402 |
| sensitivitas_batas | 0 | Levenshtein | 0.254352 | 0.025432 |
| sensitivitas_batas | 0 | OSA | 0.321990 | 0.063849 |
| sensitivitas_batas | 1 | Levenshtein | 0.259578 | 0.022042 |
| sensitivitas_batas | 1 | OSA | 0.321004 | 0.041576 |
| sensitivitas_batas | 2 | Levenshtein | 0.251064 | 0.014134 |
| sensitivitas_batas | 2 | OSA | 0.330434 | 0.087168 |
| sensitivitas_batas | 3 | Levenshtein | 0.248084 | 0.007034 |
| sensitivitas_batas | 3 | OSA | 0.310440 | 0.030353 |
| sensitivitas_maksimum | 1 | Levenshtein | 0.119596 | 0.010831 |
| sensitivitas_maksimum | 1 | OSA | 0.137715 | 0.002550 |
| sensitivitas_maksimum | 3 | Levenshtein | 0.127368 | 0.021368 |
| sensitivitas_maksimum | 3 | OSA | 0.170451 | 0.050472 |
| sensitivitas_maksimum | 5 | Levenshtein | 0.114281 | 0.003008 |
| sensitivitas_maksimum | 5 | OSA | 0.143454 | 0.015243 |

## Sensitivitas batas jarak

| algoritma | batas | jumlah_kueri | target_ditemukan | jumlah_saran |
| --- | --- | --- | --- | --- |
| Levenshtein | 0 | 5 | 0 | 0 |
| OSA | 0 | 5 | 0 | 0 |
| Levenshtein | 1 | 5 | 2 | 2 |
| OSA | 1 | 5 | 5 | 5 |
| Levenshtein | 2 | 5 | 5 | 5 |
| OSA | 2 | 5 | 5 | 5 |
| Levenshtein | 3 | 5 | 5 | 5 |
| OSA | 3 | 5 | 5 | 5 |

## Sensitivitas maksimum hasil (katalog sintetis khusus)

| algoritma | maksimum | kandidat_lolos | hasil_tampil | kode_tampil |
| --- | --- | --- | --- | --- |
| Levenshtein | 1 | 6 | 1 | SYN001 |
| OSA | 1 | 6 | 1 | SYN001 |
| Levenshtein | 3 | 6 | 3 | SYN001, SYN002, SYN003 |
| OSA | 3 | 6 | 3 | SYN001, SYN002, SYN003 |
| Levenshtein | 5 | 6 | 5 | SYN001, SYN002, SYN003, SYN004, SYN005 |
| OSA | 5 | 6 | 5 | SYN001, SYN002, SYN003, SYN004, SYN005 |

Setiap kondisi waktu diulang {PENGULANGAN} kali. Satu sampel adalah durasi satu batch dibagi jumlah panggilan dalam batch; simpangan baku menggunakan{PENGULANGAN} sampel (penyebut n-1).

Pasangan string acak dibuat dengan seed 246024. Kedua algoritma deterministik; seed hanya menetapkan data input. Hasil antarrun yang dapat bervariasi adalah waktu eksekusi.

Kurva L² dan N diskalakan agar melewati rata-rata pada ukuran terbesar. Kurva itu acuan visual, bukan pembuktian kompleksitas. Untuk pencarian, N menggambarkan komponen pemindaian; pengurutan kandidat juga ikut terukur.

Uji batas dan maksimum adalah sensitivitas parameter aplikasi, bukan parameter metaheuristik atau machine learning.
