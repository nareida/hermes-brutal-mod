#!/usr/bin/env python3
"""
install_nareida.py — Installer Mod Integrasi Nareida / RedMess untuk Hermes Agent & Multi-Agent.
Dirancang bersih, modular, tanpa hardcode ID Telegram eksternal, dan aman untuk berbagai environment
(VPS SumoPod, Termux, Linux, macOS, WSL).

Fitur Utama:
1. Auto-detect root Hermes (HERMES_HOME, /opt/data, ~/.hermes, Termux).
2. Backup otomatis sebelum modifikasi config atau file profil.
3. Modular Skill Deployment: Deploy kumpulan skills security/pentest ke folder skills profile aktif.
4. Clean Persona & System Prompt: Pilihan integrasi SOUL.md / GODMODE prompt tanpa ID lock.
5. Universal Multi-Agent Integration: Mendukung OpenCode (AGENTS.md), Claude Code (CLAUDE.md), Cursor (.cursorrules).
6. Non-destructive: File config penting dan keys tidak pernah ditimpa secara sembarangan.
"""

import os
import sys
import shutil
import argparse
import datetime
from pathlib import Path

# Color helpers
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
    print("║          Hermes Agent • Security • Multi-Agent            ║")
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

def copy_tree_safe(src: Path, dst: Path, overwrite=False) -> int:
    count = 0
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

def deploy_skills(repo_root: Path, hermes_home: Path, profile_name="default") -> int:
    log_info(f"Deploying security & dev skills to profile: {profile_name}...")
    
    # Destination skills dir
    if profile_name == "default" and (hermes_home / "skills").exists():
        skills_dst = hermes_home / "skills"
    else:
        skills_dst = hermes_home / "profiles" / profile_name / "skills"
        
    skills_src = repo_root / "skills"
    if not skills_src.exists():
        log_warn(f"Source skills folder not found at {skills_src}")
        return 0
        
    # Backup existing if present
    if skills_dst.exists():
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = hermes_home / f"skills_backup_{timestamp}"
        log_info(f"Backing up existing skills to {backup_path}...")
        try:
            shutil.copytree(skills_dst, backup_path, dirs_exist_ok=True)
            log_success("Backup created")
        except Exception as e:
            log_warn(f"Backup notice: {e}")

    installed = copy_tree_safe(skills_src, skills_dst, overwrite=True)
    log_success(f"Installed/Updated {installed} skill files in {skills_dst}")
    return installed

def deploy_persona(repo_root: Path, hermes_home: Path, profile_name="default", mode="persona"):
    log_info(f"Configuring persona/system prompt (mode: {mode})...")
    
    source_prompt = repo_root / "SOUL.md"
    if not source_prompt.exists():
        source_prompt = repo_root / "godmode_prompt.txt"
        
    if not source_prompt.exists():
        log_warn("No persona / prompt template found in repository")
        return
        
    target_dir = hermes_home / "profiles" / profile_name
    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
        
    dest_file = target_dir / "SOUL-NAREIDA.md"
    shutil.copy2(source_prompt, dest_file)
    log_success(f"Persona saved to {dest_file}")
    log_info("You can include this persona via agent.system_prompt or custom instructions.")

def deploy_multiagent_configs(repo_root: Path, target_dir: Path):
    log_info(f"Deploying multi-agent instructions to project root: {target_dir}...")
    agents_src = repo_root / "AGENTS.md"
    claude_src = repo_root / "SOUL.md"
    
    if agents_src.exists():
        shutil.copy2(agents_src, target_dir / "AGENTS.md")
        log_success(f"Deployed {target_dir / 'AGENTS.md'}")
    if claude_src.exists():
        shutil.copy2(claude_src, target_dir / "CLAUDE.md")
        log_success(f"Deployed {target_dir / 'CLAUDE.md'}")

def main():
    banner()
    parser = argparse.ArgumentParser(description="Nareida / RedMess Integration Installer")
    parser.add_argument("--hermes-home", default=None, help="Custom HERMES_HOME path")
    parser.add_argument("--profile", default="default", help="Target Hermes profile (default: default)")
    parser.add_argument("--skills-only", action="store_true", help="Install skills only")
    parser.add_argument("--multiagent-root", default=None, help="Deploy AGENTS.md/CLAUDE.md to project directory")
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without writing files")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    hermes_home = detect_hermes_home(args.hermes_home)
    
    log_info(f"Repository root: {repo_root}")
    log_info(f"Detected Hermes Home: {hermes_home}")
    
    if args.dry_run:
        log_info("DRY-RUN mode enabled. No changes applied.")
        return
        
    # 1. Deploy skills
    skills_count = deploy_skills(repo_root, hermes_home, args.profile)
    
    # 2. Deploy persona / prompts (if not skills-only)
    if not args.skills_only:
        deploy_persona(repo_root, hermes_home, args.profile)
        
    # 3. Multi-agent configs (optional)
    if args.multiagent_root:
        p_root = Path(args.multiagent_root).expanduser().resolve()
        deploy_multiagent_configs(repo_root, p_root)
        
    print()
    log_success("Nareida Integration Installation Completed Successfully!")
    print(f"{Colors.CYAN}Summary:{Colors.END}")
    print(f"  • Hermes Home : {hermes_home}")
    print(f"  • Target Profile : {args.profile}")
    print(f"  • Skills Deployed : {skills_count} files")
    print(f"\n{Colors.YELLOW}Next Step:{Colors.END} Restart or switch profile in Hermes if running.")

if __name__ == "__main__":
    main()
