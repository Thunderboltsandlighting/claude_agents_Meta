# ADA Content Creator - Installation Guide

## Quick Installation (One Command)

Install the `acc` command globally so you can run it from anywhere:

```bash
cd "/Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project"
./install_command.sh
```

That's it! Now you can type `acc` from any directory.

---

## What Gets Installed?

The installer creates a symbolic link in `/usr/local/bin/acc` that points to your project.

**This means:**
- ✅ Type `acc` from anywhere
- ✅ No need to remember the project path
- ✅ Works just like `claude`, `git`, or any other command
- ✅ Updates automatically when you pull from git

---

## Usage After Installation

### From Anywhere:
```bash
cd ~
acc  # Works!

cd /tmp
acc  # Works!

cd /Users/Documents
acc  # Works!
```

### What Happens:
1. You type `acc`
2. Terminal finds `/usr/local/bin/acc`
3. Symlink points to your project
4. Ada Content Creator launches! 🚀

---

## Verification

Check if installation worked:

```bash
which acc
# Should output: /usr/local/bin/acc

acc --help  # (if we add help flag later)
# Or just:
acc  # Launches the menu
```

---

## Uninstallation

If you ever want to remove the global command:

```bash
cd "/Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project"
./uninstall_command.sh
```

Or manually:
```bash
sudo rm /usr/local/bin/acc
```

---

## Troubleshooting

### "Permission denied" when running installer

The installer needs sudo access to create the symlink:
```bash
./install_command.sh
# Will prompt for your password
```

### Command not found after installation

1. Check if symlink exists:
   ```bash
   ls -la /usr/local/bin/acc
   ```

2. Check if /usr/local/bin is in PATH:
   ```bash
   echo $PATH | grep "/usr/local/bin"
   ```

3. If not in PATH, add to your shell config:
   ```bash
   # For zsh (macOS default):
   echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc

   # For bash:
   echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bash_profile
   source ~/.bash_profile
   ```

### Updates Not Working

The symlink should automatically reflect code updates when you pull from git. If not:

1. Reinstall:
   ```bash
   ./uninstall_command.sh
   ./install_command.sh
   ```

---

## Technical Details

### What the Installer Does:

1. Creates a symlink: `/usr/local/bin/acc` → `[project]/acc`
2. The `acc` script:
   - Finds its own location
   - Changes to project directory
   - Launches `content_cli.py`

### Why This Approach?

**Symlink vs Copy:**
- ✅ Symlink: Updates automatically with git pulls
- ❌ Copy: Would need reinstall after every update

**Why /usr/local/bin:**
- Standard location for user-installed commands
- Already in PATH on macOS
- No system files modified
- Easy to uninstall

---

## Alternative: Shell Alias (If You Don't Want Global Install)

If you prefer not to use the installer, add an alias to your shell config:

```bash
# For zsh (~/.zshrc):
echo 'alias acc="cd \"/Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project\" && ./start.sh"' >> ~/.zshrc
source ~/.zshrc

# For bash (~/.bash_profile):
echo 'alias acc="cd \"/Users/Coding Projects/Claude_Agents_Meta/therapy-practice-project\" && ./start.sh"' >> ~/.bash_profile
source ~/.bash_profile
```

**Note:** Alias approach changes your directory, symlink approach doesn't.

---

## Comparison to Other Commands

| Command | How It Works |
|---------|-------------|
| `claude` | Installed by Claude CLI installer |
| `git` | System package manager |
| `python3` | System package manager |
| `acc` | Your custom symlink (same pattern!) |

Your `acc` command follows the same pattern as professional CLI tools!

---

## Support

**Installation Issues:**
- Check [TROUBLESHOOTING] section above
- Ensure Python 3 is installed: `python3 --version`
- Ensure you have sudo access

**Command Not Working:**
- Verify installation: `which acc`
- Check permissions: `ls -la /usr/local/bin/acc`
- Reinstall: `./install_command.sh`

---

**Installed?** Type `acc` and start creating content! 🎉
