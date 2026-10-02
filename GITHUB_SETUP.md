# GitHub Setup - A to Z

## Option A - Easiest: GitHub website upload

1. Sign in to GitHub.
2. Click **New repository**.
3. Repository name: `BTB-Image-Denoising-OEL`.
4. Set visibility to **Public**.
5. Do **not** initialize with a README, .gitignore, or license because they are already included here.
6. Create the repository.
7. Open the repository and choose **Add file -> Upload files**.
8. Upload the contents of this folder (not the outer ZIP itself).
9. Commit the upload.
10. Open `CITATION.cff` and replace `USERNAME` with your actual GitHub username.

## Enable GitHub Pages

1. Open the repository **Settings**.
2. Go to **Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Branch: `main`.
5. Folder: `/docs`.
6. Click **Save**.
7. After deployment, GitHub will show your public project website URL.

## Option B - Git commands

```bash
git init
git add .
git commit -m "Initial BTB image denoising OEL showcase"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/BTB-Image-Denoising-OEL.git
git push -u origin main
```

Then enable GitHub Pages using the steps above.

## Local run

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
python btb_denoising.py
```
