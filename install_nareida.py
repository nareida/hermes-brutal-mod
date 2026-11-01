#!/usr/bin/env python3
"""
install_nareida.py — Installer Mod Integrasi Nareida / RedMess untuk Hermes Agent & Multi-Agent.
Bekerja persis seperti installer syadagentic-nareida:
1. Auto-detect active profile Hermes (baca active_profile atau targetkan profil syadagentic / default).
2. Langsung suntikkan SOUL.md ke `config.yaml` -> `agent.system_prompt` (paten & permanen).
3. Salin SOUL.md, PERSONA.md, GODMODE_ULTIMATE.md langsung ke root HERMES_HOME & direktori profil aktif.
4. Salin 1.100+ skills security/pentest ke folder skills profil yang aktif.
"""

import os
import sys
import shutil
import argparse
import datetime
from pathlib import Path

# Safe YAML import
try:
    import yaml
except ImportError:
    try:
        sys.path.insert(0, '/opt/hermes')
        import hermes_yaml as yaml
    except Exception:
        yaml = None

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def log_info(msg):
    print(f"{Colors.CYAN}[*]{Colors.END} {msg}")

def log_success(msg):
    print(f"{Colors.GREEN}[✓]{Colors.END} {msg}")

def log_warn(msg):
    print(f"{Colors.YELLOW}[!]{Colors.END} {msg}")

def log_err(msg):
    print(f"{Colors.RED}[✗]{Colors.END} {msg}")

def banner():
    print(f"{Colors.RED}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║           NAREIDA INTEGRATION INSTALLER MOD               ║")
    print("║       RedMess Core • GODMODE V3.0 • Offensive Arsenal     ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")

def detect_hermes_home(custom_path=None) -> Path:
    if custom_path:
        p = Path(custom_path).expanduser().resolve()
        if p.exists():
            return p
    
    env_home = os.environ.get("HERMES_HOME")
    if env_home:
        p = Path(env_home).expanduser().resolve()
        if p.exists():
            return p
            
    candidates = [
        Path("/opt/data"),                                  # SumoPod VPS / Custom Linux
        Path.home() / ".hermes",                             # Default Linux/macOS
        Path("/data/data/com.termux/files/home/.hermes"),    # Termux
        Path.home() / "AppData/Local/hermes"                 # Windows
    ]
    for c in candidates:
        if c.exists() and ((c / "config.yaml").exists() or (c / "profiles").exists()):
            return c
            
    return Path.home() / ".hermes"

def detect_active_profile(hermes_home: Path, requested_profile: str = None) -> tuple[str, Path]:
    if requested_profile and requested_profile != "auto":
        prof_dir = hermes_home if requested_profile == "default" else hermes_home / "profiles" / requested_profile
        return requested_profile, prof_dir

    active_file = hermes_home / "active_profile"
    active_name = "default"
    if active_file.exists():
        try:
            val = active_file.read_text(encoding="utf-8-sig").strip()
            if val:
                active_name = val
        except Exception:
            pass
            
    # Jika active_name default tapi di folder profiles ada 'syadagentic'
    if active_name == "default":
        if (hermes_home / "profiles" / "syadagentic").exists():
            active_name = "syadagentic"
            
    if active_name == "default":
        prof_dir = hermes_home
    else:
        prof_dir = hermes_home / "profiles" / active_name
        
    return active_name, prof_dir

def copy_tree_safe(src: Path, dst: Path, overwrite=True) -> int:
    count = 0
    if not src.exists():
        return 0
    dst.mkdir(parents=True, exist_ok=True)
    for root, dirs, files in os.walk(src):
        rel_path = Path(root).relative_to(src)
        target_dir = dst / rel_path
        target_dir.mkdir(parents=True, exist_ok=True)
        for f in files:
            source_file = Path(root) / f
            dest_file = target_dir / f
            if not dest_file.exists() or overwrite:
                shutil.copy2(source_file, dest_file)
                count += 1
    return count

def inject_system_prompt_to_config(config_path: Path, soul_content: str) -> bool:
    if not config_path.exists():
        log_warn(f"config.yaml not found at {config_path}")
        return False
        
    log_info(f"Injecting SOUL.md directly into config.yaml -> agent.system_prompt ({config_path})...")
    
    # Backup config.yaml first
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = config_path.with_name(f"config.yaml.bak-{ts}")
    shutil.copy2(config_path, bak)
    log_success(f"Backup config saved: {bak.name}")

    if yaml is not None:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            data.setdefault('agent', {})
            data['agent']['system_prompt'] = soul_content
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            log_success("Updated agent.system_prompt in config.yaml successfully")
            return True
        except Exception as e:
            log_warn(f"YAML parsing error ({e}), falling back to regex patch")

    # Fallback text patch when yaml module is unavailable
    lines = config_path.read_text(encoding='utf-8').splitlines()
    new_lines = []
    in_sp = False
    has_agent = False
    for line in lines:
        if line.strip() == 'agent:':
            has_agent = True
            new_lines.append(line)
            continue
        if line.strip().startswith('system_prompt:'):
            in_sp = True
            continue
        if in_sp and (line.startswith('    ') or line.startswith('\t') or line.strip() == ''):
            continue
        else:
            in_sp = False
        new_lines.append(line)
        
    clean_prompt = soul_content.replace('\n', '\n    ')
    if has_agent:
        # inject right under agent:
        idx = next(i for i, l in enumerate(new_lines) if l.strip() == 'agent:')
        new_lines.insert(idx + 1, f"  system_prompt: |\n    {clean_prompt}")
        new_text = '\n'.join(new_lines) + '\n'
    else:
        new_text = '\n'.join(new_lines) + f"\nagent:\n  system_prompt: |\n    {clean_prompt}\n"
        
    config_path.write_text(new_text, encoding='utf-8')
    log_success("Patched agent.system_prompt into config.yaml successfully")
    return True

def main():
    banner()
    parser = argparse.ArgumentParser(description="Nareida / RedMess Full Integration Installer")
    parser.add_argument("--hermes-home", default=None, help="Custom HERMES_HOME path")
    parser.add_argument("--profile", default="auto", help="Target Hermes profile ('auto', 'syadagentic', 'default')")
    parser.add_argument("--no-config-inject", action="store_true", help="Do not inject into config.yaml")
    parser.add_argument("--skills-only", action="store_true", help="Install skills only")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without writing files")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    hermes_home = detect_hermes_home(args.hermes_home)
    profile_name, profile_dir = detect_active_profile(hermes_home, args.profile)
    
    log_info(f"Repo Root      : {repo_root}")
    log_info(f"Hermes Home    : {hermes_home}")
    log_info(f"Target Profile : {profile_name} ({profile_dir})")
    
    if args.dry_run:
        log_info("DRY-RUN mode enabled. No files modified.")
        return

    # Load SOUL content
    soul_file = repo_root / "SOUL.md"
    soul_content = soul_file.read_text(encoding="utf-8").strip() if soul_file.exists() else ""

    # 1. Deploy RedMess Core Python Package
    redmess_src = repo_root / "redmess"
    if redmess_src.exists():
        copy_tree_safe(redmess_src, hermes_home / "redmess", overwrite=True)
        log_success(f"RedMess Core installed in {hermes_home / 'redmess'}")

    # 2. Deploy Full Skills Arsenal
    skills_src = repo_root / "skills"
    if skills_src.exists():
        skills_dst = profile_dir / "skills" if profile_name != "default" else hermes_home / "skills"
        installed = copy_tree_safe(skills_src, skills_dst, overwrite=True)
        log_success(f"Installed/Updated {installed} skill files in {skills_dst}")

    # 3. Deploy SOUL.md ke root HERMES_HOME & profile_dir
    if soul_content:
        # Copy to root HERMES_HOME/SOUL.md
        shutil.copy2(soul_file, hermes_home / "SOUL.md")
        log_success(f"Copied SOUL.md -> {hermes_home / 'SOUL.md'}")
        
        # Copy to profile_dir/SOUL.md jika beda
        if profile_dir != hermes_home:
            profile_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(soul_file, profile_dir / "SOUL.md")
            log_success(f"Copied SOUL.md -> {profile_dir / 'SOUL.md'}")

    # 4. Inject SOUL.md langsung ke config.yaml -> agent.system_prompt
    if not args.skills_only and not args.no_config_inject and soul_content:
        cfg_candidates = [
            profile_dir / "config.yaml",
            hermes_home / "config.yaml"
        ]
        injected = False
        for cfg in cfg_candidates:
            if cfg.exists():
                injected = inject_system_prompt_to_config(cfg, soul_content)
                break
        if not injected and (hermes_home / "config.yaml").exists():
            inject_system_prompt_to_config(hermes_home / "config.yaml", soul_content)

    # 5. Salin dokumen pendukung ke profile_dir
    for fname in ["GODMODE_ULTIMATE.md", "godmode_prompt.txt", "PERSONA.md"]:
        src_f = repo_root / "security" / fname if (repo_root / "security" / fname).exists() else repo_root / fname
        if src_f.exists():
            shutil.copy2(src_f, profile_dir / fname)
            log_success(f"Copied {fname} -> {profile_dir / fname}")

    print()
    log_success(f"Nareida / RedMess Integration successfully applied to profile '{profile_name}'!")
    print(f"{Colors.CYAN}Summary:{Colors.END}")
    print(f"  • Active Target Profile : {profile_name}")
    print(f"  • System Prompt         : Injected to config.yaml & SOUL.md")
    print(f"  • Skills Deployed       : All RedMess + GODMODE arsenal")
    print(f"\n{Colors.YELLOW}Next Step:{Colors.END} Run 'hermes restart' or 'hermes chat' to start chatting.")

if __name__ == "__main__":
    main()
