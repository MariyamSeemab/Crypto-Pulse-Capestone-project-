# Git & File Management Guide for CryptoPulse

## 📚 Complete Guide to Managing Your Project Files

---

## 🌟 Getting Started with Git

### What is Git?
Git is a version control system that helps you:
- Track changes to your code
- Collaborate with others
- Keep a history of your project
- Backup your work to the cloud (GitHub)

### What is GitHub?
GitHub is a website that stores your Git projects online, like a cloud storage for code.

---

## 📥 Cloning a Project from GitHub

### Command: `git clone`

**What it does:**
Downloads a complete copy of a project from GitHub to your computer.

**Syntax:**
```bash
git clone GITHUB_REPO_URL
```

**Example:**
```bash
git clone https://github.com/yourusername/CryptoPulse.git
```

**What happens:**
1. Git connects to GitHub
2. Downloads all project files
3. Creates a new folder named `CryptoPulse`
4. Copies all files into that folder
5. Sets up Git tracking automatically

**Real-world analogy:**
Like downloading a ZIP file from the internet, but with superpowers - it includes the entire history of changes!

---

## 📂 Navigating Folders (Directories)

### Command: `cd` (Change Directory)

**What it does:**
Moves you into a different folder, like clicking on a folder in File Explorer.

**Syntax:**
```bash
cd folder_name
```

**Examples:**

#### 1. Enter the project folder
```bash
cd CryptoPulse
```
**Result:** You're now inside the CryptoPulse folder

#### 2. Enter a subfolder
```bash
cd templates
```
**Result:** You're now inside the templates folder

#### 3. Enter nested folders
```bash
cd static/css
```
**Result:** You're now inside the css folder within static

#### 4. Go to your home directory
```bash
cd ~
```
**Result:** Takes you to your user home folder

#### 5. Go to a specific path
```bash
cd C:\Users\YourName\Desktop\CryptoPulse
```
**Result:** Goes directly to that location

**Real-world analogy:**
Like double-clicking folders on your desktop to open them.

---

## 📋 Listing Files

### Command: `ls` (List)

**What it does:**
Shows all files and folders in your current location.

**Syntax:**
```bash
ls
```

**Example output:**
```
app.py
requirements.txt
templates/
static/
README.md
```

**Useful variations:**

#### Show detailed information
```bash
ls -l
```
**Output:**
```
-rw-r--r-- 1 user user 15234 Feb 10 14:30 app.py
-rw-r--r-- 1 user user   234 Feb 10 14:30 requirements.txt
drwxr-xr-x 2 user user  4096 Feb 10 14:30 templates/
```

#### Show hidden files
```bash
ls -a
```
**Output:**
```
.
..
.git
.gitignore
app.py
```

#### Show files with sizes
```bash
ls -lh
```
**Output:**
```
-rw-r--r-- 1 user user  15K Feb 10 14:30 app.py
-rw-r--r-- 1 user user 234B Feb 10 14:30 requirements.txt
```

**Real-world analogy:**
Like viewing files in File Explorer or Finder.

---

## ⬆️ Going Back to Parent Folder

### Command: `cd ..`

**What it does:**
Moves you up one level to the parent folder.

**Syntax:**
```bash
cd ..
```

**Example:**
```bash
# You are here: C:\Users\YourName\Desktop\CryptoPulse\templates
cd ..
# Now you are here: C:\Users\YourName\Desktop\CryptoPulse
```

**Multiple levels:**
```bash
cd ../..
# Goes up two levels
```

**Real-world analogy:**
Like clicking the "Up" or "Back" button in File Explorer.

---

## 🗺️ Finding Your Current Location

### Command: `pwd` (Print Working Directory)

**What it does:**
Shows your current folder path.

**Syntax:**
```bash
pwd
```

**Example output:**
```
C:\Users\YourName\Desktop\CryptoPulse
```

**Real-world analogy:**
Like looking at the address bar in File Explorer.

---

## 📁 Complete CryptoPulse Project Structure

```
CryptoPulse/
├── app.py                          # Main Flask application
├── app_aws.py                      # AWS version of the app
├── requirements.txt                # Python dependencies
├── requirements_aws.txt            # AWS-specific dependencies
├── README.md                       # Project documentation
├── .gitignore                      # Files to ignore in Git
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── login.html                 # Login page
│   ├── signup.html                # Signup page
│   ├── home.html                  # User dashboard
│   ├── portfolio.html             # Portfolio page
│   ├── charts.html                # Charts page
│   ├── news.html                  # News page
│   ├── settings.html              # Settings page
│   ├── admin_dashboard.html       # Admin dashboard
│   ├── analyst_dashboard.html     # Analyst dashboard
│   └── moderator_dashboard.html   # Moderator dashboard
│
├── static/                         # Static files (CSS, JS, images)
│   ├── style.css                  # Main stylesheet
│   ├── script.js                  # JavaScript functions
│   └── uploads/                   # User uploaded files
│
├── aws-infrastructure.yaml         # AWS CloudFormation template
├── deploy-aws.sh                  # AWS deployment script
├── init_admin.py                  # Admin initialization script
│
└── Documentation/                  # Project documentation
    ├── LOGIN_CREDENTIALS.md
    ├── AWS_SNS_SETUP.md
    ├── DYNAMODB_TABLE_SCHEMA.md
    ├── DASHBOARD_FEATURES.md
    └── GIT_FILE_MANAGEMENT_GUIDE.md
```

---

## 🚀 Common Navigation Scenarios

### Scenario 1: Just Cloned the Project

```bash
# 1. Clone the project
git clone https://github.com/yourusername/CryptoPulse.git

# 2. Enter the project folder
cd CryptoPulse

# 3. See what's inside
ls

# 4. Check your location
pwd
```

### Scenario 2: Working on Templates

```bash
# 1. Go to templates folder
cd templates

# 2. List all HTML files
ls

# 3. Go back to main project
cd ..
```

### Scenario 3: Exploring the Project

```bash
# 1. Start in project root
pwd
# Output: /Users/YourName/CryptoPulse

# 2. Go to templates
cd templates
pwd
# Output: /Users/YourName/CryptoPulse/templates

# 3. Go back
cd ..
pwd
# Output: /Users/YourName/CryptoPulse

# 4. Go to static
cd static
pwd
# Output: /Users/YourName/CryptoPulse/static

# 5. Go back to root
cd ..
```

---

## 🔧 Essential Git Commands

### 1. Check Status
```bash
git status
```
**Shows:** What files have changed

### 2. Add Files to Staging
```bash
git add .                    # Add all files
git add app.py              # Add specific file
git add templates/          # Add entire folder
```

### 3. Commit Changes
```bash
git commit -m "Added email notifications feature"
```
**What it does:** Saves your changes with a description

### 4. Push to GitHub
```bash
git push origin main
```
**What it does:** Uploads your changes to GitHub

### 5. Pull Latest Changes
```bash
git pull origin main
```
**What it does:** Downloads latest changes from GitHub

### 6. View History
```bash
git log
```
**Shows:** All previous commits

### 7. Create a Branch
```bash
git branch feature-name
git checkout feature-name
```
**What it does:** Creates a separate workspace for new features

---

## 📝 Complete Workflow Example

### Starting a New Feature

```bash
# 1. Make sure you're in the project folder
cd CryptoPulse
pwd

# 2. Check current status
git status

# 3. Pull latest changes
git pull origin main

# 4. Create a new branch
git checkout -b add-email-notifications

# 5. Make your changes (edit files)
# ... edit app.py, add new features ...

# 6. Check what changed
git status

# 7. Add your changes
git add .

# 8. Commit with a message
git commit -m "Added AWS SNS email notifications for trades"

# 9. Push to GitHub
git push origin add-email-notifications

# 10. Create Pull Request on GitHub website
```

---

## 🎯 Quick Reference Card

### Navigation Commands
| Command | What It Does | Example |
|---------|-------------|---------|
| `cd folder` | Enter folder | `cd templates` |
| `cd ..` | Go up one level | `cd ..` |
| `cd ~` | Go to home | `cd ~` |
| `pwd` | Show current path | `pwd` |
| `ls` | List files | `ls` |
| `ls -la` | List all files (detailed) | `ls -la` |

### Git Commands
| Command | What It Does | Example |
|---------|-------------|---------|
| `git clone URL` | Download project | `git clone https://...` |
| `git status` | Check changes | `git status` |
| `git add .` | Stage all changes | `git add .` |
| `git commit -m "msg"` | Save changes | `git commit -m "Fix bug"` |
| `git push` | Upload to GitHub | `git push origin main` |
| `git pull` | Download from GitHub | `git pull origin main` |
| `git log` | View history | `git log` |

---

## 💡 Pro Tips

### 1. Use Tab Completion
Type the first few letters and press `Tab`:
```bash
cd Cry[Tab]  # Autocompletes to: cd CryptoPulse/
```

### 2. View Previous Commands
Press `↑` (up arrow) to see previous commands

### 3. Clear the Screen
```bash
clear          # Linux/Mac
cls            # Windows CMD
Clear-Host     # Windows PowerShell
```

### 4. Create Aliases (Shortcuts)
```bash
# Add to ~/.bashrc or ~/.zshrc
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push origin main'
```

### 5. Use .gitignore
Create a `.gitignore` file to exclude files:
```
__pycache__/
*.pyc
.env
.DS_Store
node_modules/
```

---

## 🆘 Common Issues & Solutions

### Issue 1: "Not a git repository"
**Problem:** You're not in a Git project folder
**Solution:**
```bash
cd CryptoPulse  # Go to project folder
git status      # Now it works
```

### Issue 2: "Permission denied"
**Problem:** Don't have access to GitHub repo
**Solution:**
```bash
# Set up SSH key or use HTTPS with credentials
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### Issue 3: "Merge conflict"
**Problem:** Your changes conflict with others
**Solution:**
```bash
git status              # See conflicted files
# Edit files to resolve conflicts
git add .
git commit -m "Resolved merge conflict"
```

### Issue 4: "Can't find folder"
**Problem:** Wrong path or typo
**Solution:**
```bash
pwd                     # Check where you are
ls                      # See what's available
cd correct-folder-name  # Use exact name
```

---

## 📚 Learning Resources

### Interactive Tutorials
- [GitHub Learning Lab](https://lab.github.com/)
- [Git Immersion](http://gitimmersion.com/)
- [Learn Git Branching](https://learngitbranching.js.org/)

### Documentation
- [Git Official Docs](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Atlassian Git Tutorial](https://www.atlassian.com/git/tutorials)

### Cheat Sheets
- [GitHub Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [GitLab Git Cheat Sheet](https://about.gitlab.com/images/press/git-cheat-sheet.pdf)

---

## 🎓 Practice Exercises

### Exercise 1: Basic Navigation
```bash
# 1. Clone a project
git clone https://github.com/yourusername/CryptoPulse.git

# 2. Enter the project
cd CryptoPulse

# 3. List files
ls

# 4. Go to templates
cd templates

# 5. List HTML files
ls *.html

# 6. Go back
cd ..

# 7. Check location
pwd
```

### Exercise 2: Making Changes
```bash
# 1. Check status
git status

# 2. Create a new file
echo "# Test" > test.md

# 3. Check status again
git status

# 4. Add the file
git add test.md

# 5. Commit
git commit -m "Added test file"

# 6. Push to GitHub
git push origin main
```

---

## 🌟 Summary

### Key Concepts
1. **`git clone`** - Download project from GitHub
2. **`cd`** - Move between folders
3. **`ls`** - See what's in a folder
4. **`cd ..`** - Go back to parent folder
5. **`pwd`** - See where you are

### Remember
- Git tracks your code changes
- GitHub stores your code online
- Navigation commands help you move around
- Always check where you are with `pwd`
- Use `git status` frequently

### Next Steps
1. Practice these commands
2. Clone your CryptoPulse project
3. Explore the folder structure
4. Make small changes
5. Commit and push to GitHub

---

*Happy Coding! 🚀*

*Last Updated: February 2026*
*Version: 1.0 - Git & File Management Guide*