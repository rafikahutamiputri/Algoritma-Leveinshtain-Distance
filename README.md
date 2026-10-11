# Pencarian Barang Inventaris dengan Levenshtein Distance

Program ini mencari nama barang yang mengandung kesalahan ketik menggunakan Levenshtein Distance. Algoritma inti ditulis sendiri dengan tabel *dynamic programming* melalui metode Wagner-Fischer. Optimal String Alignment (OSA) digunakan sebagai pembanding dalam eksperimen.

## 1\. Isi proyek

Simpan berkas berikut dalam satu folder. Pertahankan penulisan nama berkas, termasuk huruf besar dan kecil.

|Berkas|Kegunaan|
|-|-|
|`Kode\_Inti.py`|Fungsi normalisasi teks dan perhitungan jarak Levenshtein.|
|`Aplikasi\_pencarian.py`|Pencarian barang melalui terminal menggunakan Levenshtein.|
|`Osa\_pembandingg.py`|Fungsi OSA dan demonstrasi perhitungan dua string. Nama berkas memang memakai dua huruf `g` di akhir.|
|`Eksperimen.py`|Pengujian kedua algoritma, pengukuran waktu, serta pembuatan tabel dan grafik.|
|`data\_inventaris.csv`|Data dasar berisi 10 barang simulasi dengan kode, nama, dan stok.|

`Kode\_Inti.py` dipanggil oleh berkas lain. Menjalankannya langsung tidak menampilkan hasil karena berkas ini hanya mendefinisikan fungsi.



## 2\. Persiapan

Ekstrak ZIP, lalu buka terminal di folder yang berisi berkas Python tersebut. Program membutuhkan Python 3. Eksperimen juga membutuhkan Matplotlib untuk membuat grafik:

```powershell
python -m pip install matplotlib
```

Modul seperti `csv`, `pathlib`, `time`, `random`, dan `statistics` merupakan pustaka standar Python sehingga tidak perlu dipasang terpisah. Pustaka tersebut digunakan untuk mendukung pengolahan data dan eksperimen; perhitungan jarak Levenshtein dan OSA ditulis dalam kode proyek.

Catatan lingkungan pada hasil sesi `20261011\_072055\_051327` mencatat Windows 11, Python 3.14.7, dan Matplotlib 3.11.2. Versi tersebut adalah lingkungan yang tercatat pada hasil pengujian, bukan persyaratan versi minimum.

Jika perintah `python` mengarah ke instalasi yang berbeda, gunakan alamat Python yang sama untuk memasang Matplotlib dan menjalankan program. Contoh sesuai lokasi instalasi pada komputer pengguna:

```powershell
\& "C:\\Users\\Acer\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" -m pip install matplotlib
\& "C:\\Users\\Acer\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" ".\\Eksperimen.py"
```

## 3\. Menjalankan program

### Pencarian inventaris

```powershell
python Aplikasi\_pencarian.py
```

Masukkan nama atau salah ketik, misalnya `proyktor`. Pada data bawaan, program menampilkan Proyektor dengan kode BRG001, stok 4, dan jarak 1. Ketik `:keluar` untuk mengakhiri program.

Program menyeragamkan huruf menggunakan `casefold()` dan merapikan spasi sebelum membandingkan nama lengkap. Kandidat diurutkan berdasarkan jarak terkecil, nama hasil normalisasi, lalu kode barang. Kode dan stok ditampilkan tetapi tidak digunakan untuk menghitung jarak.

Pengaturan pada bagian awal `Aplikasi\_pencarian.py`:

```python
BATAS\_JARAK = 2
MAKSIMUM\_HASIL = 3
```

Artinya, kandidat harus memiliki jarak paling besar 2 dan program menampilkan paling banyak 3 hasil.



**CONTOH KELUARAN** 

Masukkan nama barang: proyktor



Kode       Nama        Stok  Jarak

BRG001     Proyektor      4      1

### Demonstrasi OSA

```powershell
python Osa\_pembandingg.py
```

Masukkan `keybaord` sebagai string asal dan `keyboard` sebagai string tujuan. Hasil OSA adalah 1 karena dua karakter bersebelahan tertukar. Demonstrasi ini menerima teks apa adanya, tanpa normalisasi otomatis.

### Eksperimen lengkap

```powershell
python Eksperimen.py
```

Program menjalankan pengujian kedua algoritma dan menyimpan tabel, grafik, serta ringkasan secara otomatis. Grafik disimpan sebagai PNG tanpa membuka jendela grafik.

## 4\. Data inventaris

Berkas CSV menggunakan pemisah koma dan judul kolom dengan urutan berikut:

```csv
kode,nama,stok
BRG001,Proyektor,4
BRG002,Keyboard,12
BRG003,Mouse,15
```

Kode dan nama harus terisi, stok berupa bilangan bulat tidak negatif, dan kode barang harus unik untuk eksperimen. Eksperimen standar memerlukan tepat 10 barang dasar. Pertahankan data bawaan agar nama target pada pengujian tetap tersedia. Katalog sintetis untuk uji beban dibuat oleh skrip tanpa mengubah CSV dasar.

## 5\. Rancangan eksperimen

### Pemeriksaan tiga kasus kecil

|Kasus|Asal|Tujuan|Levenshtein|OSA|
|-|-|-|-:|-:|
|Penyisipan|proyktor|proyektor|1|1|
|Penggantian|mause|mouse|1|1|
|Transposisi|keybaord|keyboard|2|1|

Skrip memeriksa jarak terhadap nilai yang diharapkan dan mencatat kemunculan barang tujuan pada batas jarak 1. Status `LULUS` merujuk pada kesesuaian nilai jarak; kolom `target\_tampil\_batas\_1` melaporkan kemunculan target secara terpisah.

### Pengukuran dan sensitivitas

|Pengujian|Nilai uji|Panggilan per batch|
|-|-|-:|
|Panjang masing-masing string, `m = n = L`|10, 20, 40, 80, 160 karakter|20 hitungan jarak|
|Jumlah barang, `N`|20, 40, 60, 80, 100 barang|10 pencarian|
|Batas jarak|0, 1, 2, 3; maksimum 3 hasil|5 pencarian|
|Maksimum hasil|1, 3, 5; batas jarak 2|10 pencarian|

Uji jumlah barang memakai kueri `proyktor 01`. Uji batas memakai lima kueri: `proyktor`, `mause`, `keybaord`, `monitro`, dan `webacm`. Batas 0 menjadi kontrol kecocokan persis. Uji maksimum memakai kueri `mouse` pada katalog khusus Mouse dan Mouse A sampai Mouse E.

Pengaturan utama pada `Eksperimen.py`:

```python
PENGULANGAN = 10
BATCH\_INTI = 20
BATCH\_KATALOG = 10
SEED\_DATA = 246024
```

Setiap kondisi diukur 10 kali setelah satu batch pemanasan. Timer menggunakan `time.perf\_counter\_ns()`. Durasi batch dibagi jumlah panggilan untuk memperoleh satu sampel waktu per panggilan. Rata-rata dan simpangan baku sampel dihitung dari 10 sampel tersebut. Urutan kedua algoritma dibalik pada pengulangan berikutnya.

Seed menetapkan pasangan string acak agar input dapat dibuat ulang. Kedua algoritma bersifat deterministik; waktu eksekusi tetap dapat berubah antarpengukuran. Penulisan hasil dan pembuatan grafik dilakukan di luar bagian yang diukur timer.

Pengaturan aplikasi dan eksperimen berada dalam berkas terpisah. Jika mengubah batas atau maksimum hasil untuk perbandingan, periksa keduanya agar kondisi yang digunakan tetap sesuai. Komentar sebelum `ukur\_kondisi()` masih menyebut lima pengulangan; pelaksanaan mengikuti `PENGULANGAN = 10`.

## 6\. Membaca keluaran

Setiap eksekusi terbaru membuat folder baru pada `Hasil Eksperimen/<waktu\_sesi>/`. Lokasi lengkap ditampilkan saat program selesai. Folder `hasil\_bab4` dalam ZIP berisi hasil sesi terdahulu.

|Keluaran|Isi|
|-|-|
|`ringkasan\_hasil.md`|Ringkasan lingkungan dan tabel hasil.|
|`hasil\_tiga\_kasus.csv`|Nilai harapan, jarak hasil, status, dan kemunculan target.|
|`waktu\_mentah.csv`|Sampel waktu setiap pengulangan dan jumlah panggilan per batch.|
|`waktu\_ringkasan.csv`|Rata-rata dan simpangan baku waktu dalam milidetik.|
|`sensitivitas\_batas.csv`|Jumlah target ditemukan dan total saran dari lima kueri.|
|`sensitivitas\_maksimum.csv`|Jumlah kandidat yang lolos dan hasil yang ditampilkan.|
|`grafik\_waktu\_panjang.png`|Waktu terhadap panjang string beserta kurva acuan kuadrat.|
|`grafik\_waktu\_katalog.png`|Waktu terhadap jumlah barang beserta kurva acuan linear.|
|`kurva\_teoretis.csv`|Nilai kurva acuan yang diskalakan pada ukuran terbesar.|
|`lingkungan\_uji.csv`|Lingkungan komputer dan timer yang digunakan.|

Folder hasil juga menyimpan pasangan string, kueri, katalog dasar, katalog skala, dan katalog khusus yang dipakai. Gunakan tabel dan grafik dari satu sesi yang sama saat menyusun laporan.

Kurva acuan membantu membandingkan bentuk pertumbuhan waktu; kurva tersebut bukan bukti kompleksitas. Pada grafik katalog, acuan linear menggambarkan komponen pemindaian, sedangkan waktu terukur juga mencakup pengurutan kandidat. `jumlah\_saran` mencakup semua hasil yang ditampilkan, termasuk target yang ditemukan.

## 7\. Batas penggunaan dan kendala umum

Pencarian menilai kedekatan ejaan nama lengkap. Program tidak mencari sinonim, makna, atau potongan nama, dan tidak memperbarui stok. Kandidat berjarak kecil belum tentu merupakan barang yang dimaksud pengguna. Perbandingan waktu berlaku pada data dan lingkungan pengukuran yang digunakan.

* **`ModuleNotFoundError`:** periksa bahwa semua berkas Python berada dalam satu folder dan nama modul sama persis dengan pernyataan `import`.
* **Matplotlib belum ada:** pasang menggunakan interpreter Python yang sama dengan yang menjalankan `Eksperimen.py`.
* **CSV tidak terbaca:** pastikan `data\_inventaris.csv` berada di folder program dengan judul kolom `kode,nama,stok`.
* **Grafik tidak muncul di layar:** buka berkas PNG di folder hasil; skrip memang menyimpannya tanpa jendela grafik.

