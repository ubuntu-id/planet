# Planet feed at Ubuntu-ID

## Who?

If you are using Ubuntu and want to share your blog, please let us know

## How to add my blog to planet?

You need to:
1. Create [Launchpad](https://launchpad.net) account
2. Sign [Ubuntu CoC](https://launchpad.net/codeofconduct)
3. Open a pull request that adds your feed to `config.ini`, using the pull request template
4. (optional) Hackergotchi if you want you face appear in planet (put the image in `heads/`)

## etc
Planet Ubuntu ID is using planet venus and Ubuntu Theme, all copyrights
goes to origin creator

## How to build

Planet Venus (Python 2) sudah tidak dipakai. Situs sekarang dibangun oleh `build.py` (Python 3, feedparser + Jinja2)
yang membaca `config.ini`, mengambil semua feed, lalu menulis situs statis ke `public/`.

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python build.py
```

Feed yang gagal diambil dilewati dan dicatat di stderr. Hasilnya bisa disajikan oleh web server statis apa pun.

### Cloudflare (Workers Builds / Pages)

Situs ini statis. `wrangler.jsonc` mengunggah folder `public/` sebagai static assets.

- Project name: `planet-ubuntu-id` (huruf kecil, angka, dan tanda hubung saja)
- Build command: `pip install -r requirements.txt && python build.py`
- Deploy command: `npx wrangler deploy`
- Preview command: `npx wrangler versions upload`
- Python versi 3.13 dipilih lewat `.python-version`
- Rebuild berkala: `.github/workflows/rebuild.yml` memanggil Deploy Hook tiap 6 jam. Simpan URL hook sebagai secret `CLOUDFLARE_DEPLOY_HOOK` (Settings > Secrets and variables > Actions).
