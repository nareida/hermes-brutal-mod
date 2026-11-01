# 🚀 Panduan Installer Mod Integrasi Nareida (`install_nareida.py`)

Installer universal, aman, dan non-destruktif untuk mengintegrasikan **RedMess Core**, **GODMODE ULTIMATE V3.0**, **Katalog Skills Security/Pentest**, serta jembatan multi-agent (OpenCode, Claude Code, Cursor) ke dalam lingkungan **Hermes Agent**.

---

## 📦 Apa Saja yang Di-include?

Installer ini sudah **100% full-bundle** mencakup semua komponen:

1. **RedMess Core Engine:**
   - Package Python `redmess/` (`core.py`, `skills.py`, `utils.py`, `cli.py`).
   - Dedicated profile `profiles/redmess/` (lengkap dengan `SOUL.md`, `JAILBREAK.md`, `GODMODE.md`, `IDENTITY.md`).

2. **GODMODE ULTIMATE V3.0:**
   - `GODMODE_ULTIMATE.md` & `godmode_prompt.txt`.
   - `godmode_config.yaml` versi unlocked (**tidak ada lock ID Telegram**, bebas dipakai siapa saja).
   - Persona `SOUL-NAREIDA.md`.

3. **RedMess Offensive Arsenal & Skills:**
   - `skills/security/redmess-arsenal` & `skills/redmess-security`.
   - `skills/security/godmode` (script auto-jailbreak, parseltongue, godmode race).
   - `skills/security/super-mod-brutal-prefills` (35+ template prefill model: Claude, GPT, DeepSeek, GLM, Kimi, dll.).
   - Seluruh skill pelengkap (APK modding, OSINT, web-pentest, reverse engineering).

4. **Multi-Agent Setup:**
   - `AGENTS.md` (OpenCode) & `CLAUDE.md` (Claude Code) untuk root project.

---

## ⚡ Cara Menjalankan

### 1. Test Simulasi (Dry-Run)
Cek apa saja yang akan dipasang tanpa mengubah file apa pun:
```bash
python3 install_nareida.py --dry-run
```

### 2. Pasang Lengkap (Default Profile)
Memasang RedMess Core, GODMODE V3.0, Persona, dan semua Skills:
```bash
python3 install_nareida.py
```

### 3. Pasang + Buat Dedicated Profile `redmess`
Membuat profil terpisah khusus RedMess agar profil default kamu tidak tercampur:
```bash
python3 install_nareida.py --create-redmess-profile
```
*(Bisa beralih kapan saja lewat: `hermes profile switch redmess`)*

### 4. Pasang Khusus Skills Saja
Jika kamu hanya butuh seluruh tool/skill tanpa mengubah persona:
```bash
python3 install_nareida.py --skills-only
```

### 5. Pasang ke Root Project Multi-Agent
Untuk meletakkan `AGENTS.md` & `CLAUDE.md` di folder project tertentu:
```bash
python3 install_nareida.py --multiagent-root /path/ke/project
```

---

## 📋 Parameter Lengkap

| Argumen | Deskripsi | Default |
|---|---|---|
| `--hermes-home <PATH>` | Menentukan direktori root Hermes secara manual | Auto-detect |
| `--profile <NAME>` | Target profil Hermes yang dipasang | `default` |
| `--create-redmess-profile` | Buat direktori profile khusus `profiles/redmess` | `False` |
| `--skills-only` | Hanya memasang katalog skills | `False` |
| `--multiagent-root <PATH>` | Salin `AGENTS.md` & `CLAUDE.md` ke folder project | `None` |
| `--dry-run` | Menampilkan simulasi tanpa menulis file | `False` |
