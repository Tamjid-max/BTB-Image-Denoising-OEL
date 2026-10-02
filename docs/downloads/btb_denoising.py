import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tkinter import Tk, filedialog

from skimage.restoration import denoise_nl_means
from skimage.metrics import peak_signal_noise_ratio as PSNR
from skimage.metrics import structural_similarity as SSIM


# ---------- Select image ----------
root = Tk()
root.withdraw()

path = filedialog.askopenfilename(
    title="Select Image",
    filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")]
)

if not path:
    raise SystemExit("No image selected")

clean = np.array(
    Image.open(path).convert("L").resize((256, 256)),
    dtype=float
) / 255.0


# ---------- Add Gaussian noise ----------
def add_noise(img, sigma=15):
    rng = np.random.default_rng(1)
    return np.clip(
        img + rng.normal(0, sigma/255, img.shape),
        0, 1
    )


# ---------- Base denoiser ----------
def denoise(img, sigma=15):
    s = sigma / 255.0

    return denoise_nl_means(
        img,
        h=0.8*s,
        sigma=s,
        patch_size=5,
        patch_distance=6,
        fast_mode=True,
        channel_axis=None
    )


# ---------- BTB ----------
def btb(img, T=3, mu=.7, sigma=15):
    x = img.copy()

    for _ in range(T):
        z = denoise(x, sigma)
        x = (1-mu)*x + mu*z

    return np.clip(x, 0, 1)


# ---------- Metrics ----------
def metrics(a, b):
    mse = np.mean((a-b)**2)
    psnr = PSNR(a, b, data_range=1)
    ssim = SSIM(a, b, data_range=1)
    return mse, psnr, ssim


# ---------- Process ----------
sigma = 15

noisy = add_noise(clean, sigma)
output = btb(noisy, T=3, mu=0.7, sigma=sigma)

n = metrics(clean, noisy)
d = metrics(clean, output)


# ---------- Print ----------
print("\nNOISY IMAGE")
print(f"MSE  = {n[0]:.6f}")
print(f"PSNR = {n[1]:.2f} dB")
print(f"SSIM = {n[2]:.4f}")

print("\nBTB DENOISED")
print(f"MSE  = {d[0]:.6f}")
print(f"PSNR = {d[1]:.2f} dB")
print(f"SSIM = {d[2]:.4f}")


# ---------- Show ----------
plt.figure(figsize=(12,4))

for i, (img, title) in enumerate([
    (clean, "Original"),
    (noisy, f"Noisy\nPSNR={n[1]:.2f} dB"),
    (output, f"BTB Denoised\nPSNR={d[1]:.2f} dB")
]):
    plt.subplot(1,3,i+1)
    plt.imshow(img, cmap="gray", vmin=0, vmax=1)
    plt.title(title)
    plt.axis("off")

plt.tight_layout()
plt.show()

# ================= NOISE SENSITIVITY GRAPH =================
sigmas = [10, 15, 25]
noisy_psnr = []
btb_psnr = []

for s in sigmas:
    n_img = add_noise(clean, s)
    d_img = btb(n_img, T=3, mu=0.7, sigma=s)

    noisy_psnr.append(metrics(clean, n_img)[1])
    btb_psnr.append(metrics(clean, d_img)[1])

plt.figure(figsize=(7, 4))
plt.plot(sigmas, noisy_psnr, "o-", label="Noisy Image")
plt.plot(sigmas, btb_psnr, "s-", label="BTB Denoised")
plt.xlabel("Noise Level (Sigma)")
plt.ylabel("PSNR (dB)")
plt.title("Effect of Noise Level on Image Quality")
plt.xticks(sigmas)
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()


# ================= ITERATION SENSITIVITY GRAPH =================
iterations = range(1, 11)
iteration_psnr = []

test_noisy = add_noise(clean, 15)

for t in iterations:
    result = btb(test_noisy, T=t, mu=0.7, sigma=15)
    iteration_psnr.append(metrics(clean, result)[1])

plt.figure(figsize=(7, 4))
plt.plot(iterations, iteration_psnr, "o-")
plt.xlabel("Number of BTB Iterations")
plt.ylabel("PSNR (dB)")
plt.title("Effect of BTB Iterations on PSNR")
plt.xticks(iterations)
plt.grid()
plt.tight_layout()
plt.show()
