@echo off
echo === Setting Git username and email ===
git config --global user.name "sarveshdv06-glitch"
git config --global user.email "sarveshdv06@gmail.com"

echo === Navigating to project folder ===
cd /d C:\Users\Dell\Desktop\Freedom

echo === Removing old remote origin (if any) ===
git remote remove origin 2>nul

echo === Adding new GitHub remote URL ===
git remote add origin https://github.com/sarveshdv06-glitch/quiz-app.git

echo === Setting branch to main ===
git branch -M main

echo === Adding all files ===
git add .

echo === Committing changes ===
git commit -m "Update project"

echo === Pushing to GitHub main branch ===
git push -u origin main

echo === Done! ===
pause
