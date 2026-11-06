# planet

Planet (agregator blog) komunitas Ubuntu Indonesia. Situs statis yang dibangun dari daftar feed di `config.ini`, live di https://planet.ubuntu-id.org (Cloudflare Workers static assets). Branch default `master`.

## Stack

- `build.py`: Python 3 (versi di `.python-version`), `feedparser` + `Jinja2`. Mengganti Planet Venus (Python 2) yang sudah mati.
- Template: `index.html.j2`, `rss20.xml.j2`, `opml.xml.j2`. Tema lama di `css/`, `images/`, `heads/` (hackergotchi), `style.css`. Aset CSS memakai path absolut `/ubuntu/...`, jadi output aset ditulis ke `public/ubuntu/`.
- `config.ini`: bagian `[Planet]` untuk pengaturan, satu section per feed (`[URL]`, `name`, `face`). Beberapa kunci Venus (`template_files`, `bill_of_materials`, dst) tidak dipakai lagi.
- `wrangler.jsonc`: mengunggah `public/` sebagai static assets.

## Build dan tes

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python build.py     # tulis ke public/ (di-gitignore)
```

Butuh jaringan dan memakan 1 sampai 2 menit karena ada feed yang lambat. Feed yang gagal dilewati dan dicatat di stderr, jadi build tetap sukses. CI (`.github/workflows/ci.yml`) mengecek syntax, config, build, XML valid, dan minimal satu entri.

## Konvensi

- Feed yang mati atau error ditandai komentar `# ERROR (cek <tanggal>): <alasan>` di atas section-nya, dan seluruh section dikomentari (`# `). Jangan dihapus kecuali diminta, ini data komunitas.
- Permintaan tambah blog lewat PR yang mengubah `config.ini` (template di `.github/pull_request_template.md`). Pemohon wajib sudah menandatangani Ubuntu Code of Conduct di Launchpad: cek profil Launchpad-nya sebelum merge, dan buka feed-nya. Tolak feed spam atau konten tidak relevan.
- Alamat feed harus feed asli (RSS/Atom), bukan halaman HTML. Uji dengan `curl -sL <url>` sebelum menambah.
- Tulisan feed ditampilkan ulang apa adanya (sudah disanitasi `feedparser`). Jangan menambah pemrosesan HTML tanpa alasan.

## Deploy

- Push ke `master` memicu build Cloudflare (build: `pip install -r requirements.txt && python build.py`, deploy: `npx wrangler deploy`).
- Build branch non-production memakai `npx wrangler preview`, yang mewajibkan blok `"previews": {}` di `wrangler.jsonc`. Jangan dihapus.
- `.github/workflows/rebuild.yml` memanggil Deploy Hook tiap 6 jam lewat secret `CLOUDFLARE_DEPLOY_HOOK`. Jangan menaruh URL hook di repo atau chat.
- Cron GitHub hanya jalan dari `master`.
