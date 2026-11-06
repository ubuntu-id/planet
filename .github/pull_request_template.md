## Permintaan tambah blog ke Planet Ubuntu-ID

Template ini untuk menambahkan feed blog pribadi Anda ke `config.ini`. Untuk perubahan kode, hapus isi template ini dan jelaskan perubahannya.

### Data blog

- Nama lengkap:
- Username Launchpad (tautan profil, mis. `https://launchpad.net/~username`):
- Alamat feed (RSS/Atom, bukan alamat halaman blog):
- Hackergotchi (opsional): tambahkan gambar ke `heads/` dan isi `face = nama-file` di config

### Tambahan di `config.ini`

```ini
[https://contoh.web.id/feed.xml]
name = Nama Lengkap
face = nama-file.png
```

### Ubuntu Code of Conduct

- [ ] Saya punya akun [Launchpad](https://launchpad.net) dan sudah menandatangani [Ubuntu Code of Conduct](https://launchpad.net/codeofconduct) (tanda tangan terlihat di profil Launchpad saya).
- [ ] Saya sudah membaca dan akan mematuhi [Ubuntu Code of Conduct](https://ubuntu.com/community/docs/ethos/code-of-conduct) dalam konten yang tampil di planet ini.

### Feed

- [ ] Alamat feed sudah saya buka di browser dan isinya XML RSS/Atom yang valid.
- [ ] Blog dan feed ini milik saya.
- [ ] Isi feed relevan dengan Ubuntu, Linux, atau open source. Kalau blog saya campur topik, saya memakai feed kategori atau tag khusus.
- [ ] Blog tidak berisi iklan terselubung, judi, konten dewasa, atau spam.
- [ ] Saya setuju tulisan saya (judul dan isi) ditampilkan ulang di planet ini dan bisa dihapus dengan meminta lewat issue.
- [ ] Saya hanya mengubah `config.ini` (dan gambar di `heads/` jika ada) dalam PR ini.

<!-- Untuk maintainer: periksa profil Launchpad pemohon, pastikan "Signed Ubuntu Code of Conduct" tercentang, dan buka feed-nya sebelum merge. -->
