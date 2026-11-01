# 🚀 Panduan Installer Mod Integrasi Nareida (`install_nareida.py`)

Installer universal, aman, dan non-destruktif untuk mengintegrasikan kumpulan **Skills**, **Persona/SOUL**, serta instruksi multi-agent (OpenCode, Claude Code, Cursor) dari repo ini ke lingkungan **Hermes Agent**.

---

## 🛡️ Mengapa Menggunakan `install_nareida.py`?
Berbeda dari `deploy.sh` atau script bawaan RedMess lama:
1. **Tidak Ada ID Telegram Terkunci / Paywall Gate:** Bawaan RedMess lama mengunci aktivasi hanya untuk ID Telegram `7570665912`. Mod ini 100% terbuka untuk siapa saja.
2. **Auto-Detect Root & Multi-Environment:** Otomatis mendeteksi lokasi Hermes di VPS (`/opt/data`), PC standar (`~/.hermes`), Termux Android (`/data/data/com.termux/files/home/.hermes`), atau Windows WSL.
3. **Aman & Non-Destruktif:**
   - Melakukan backup folder `skills` otomatis sebelum penambahan file baru.
   - Tidak menimpa `config.yaml` atau token API yang sedang aktif.
   - Menyediakan mode simulasi (`--dry-run`).

---

## ⚡ Cara Menjalankan

### 1. Test Simulasi (Dry-Run)
Cek apa saja yang akan dipasang tanpa mengubah file apa pun:
```bash
python3 install_nareida.py --dry-run
```

### 2. Pasang ke Profile Hermes Default
Menyalin semua katalog skills + persona `SOUL-NAREIDA.md`:
```bash
python3 install_nareida.py
```

### 3. Pasang Khusus Skills Saja
Jika kamu tidak ingin menyentuh persona dan hanya butuh seluruh skills tambahan:
```bash
python3 install_nareida.py --skills-only
```

### 4. Pasang ke Profile Tertentu (Isolated Profile)
```bash
python3 install_nareida.py --profile custom-profile
```

### 5. Pasang ke Root Project Multi-Agent
Untuk meletakkan `AGENTS.md` (OpenCode) dan `CLAUDE.md` (Claude Code) di root project tertentu:
```bash
python3 install_nareida.py --multiagent-root /path/ke/project
```

---

## 📋 Parameter Lengkap

| Argumen | Deskripsi | Default |
|---|---|---|
| `--hermes-home <PATH>` | Menentukan direktori root Hermes secara manual | Auto-detect |
| `--profile <NAME>` | Target profil Hermes yang akan dipasang | `default` |
| `--skills-only` | Hanya memasang katalog skills | `False` |
| `--multiagent-root <PATH>` | Menyalin `AGENTS.md` & `CLAUDE.md` ke folder project | `None` |
| `--dry-run` | Menampilkan simulasi tanpa menulis file | `False` |
