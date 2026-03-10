@echo off
REM =============================================
REM  GitHub Uploader Script
REM  One-click: add → commit → push
REM =============================================

echo.
echo *** S1 Batch Snapshot: GitHub Upload ***
echo.

REM ======== SET YOUR REPOSITORY URL HERE ========
set REPO_URL=https://github.com/MARISKALINKA/s1_batch_snap.git
REM ===============================================

REM Move into project folder
cd /d E:\Marim\esa_gith\s1_batch_snap

REM Check if .git exists
if not exist .git (
    echo Initializing Git repository...
    git init
)

REM Ensure main branch exists
git branch -M main

REM Set remote if missing
git remote get-url origin >nul 2>nul
if %errorlevel% neq 0 (
    echo Adding remote origin...
    git remote add origin %REPO_URL%
) else (
    echo Remote origin already exists.
)

REM Add all files
echo Adding files...
git add .

REM Commit (ignore empty commit errors)
echo Committing changes...
git commit -m "Update: full project sync" >nul 2>nul

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main

echo.
echo *** Upload complete! ***
echo Open your repo:
echo   %REPO_URL%
echo.
pause
