# Showcase Guide

## 60-second demo flow

1. Open the repository README and state the problem: noisy images lose useful visual information.
2. Show the BTB update equation: `x_(t+1) = (1-mu)x_t + mu f(x_t)`.
3. Explain that `f(x)` is Non-Local Means (NLM) in this reproduction.
4. Run `btb_denoising.py`, select a JPG/PNG image, and show Original -> Noisy -> BTB Denoised.
5. Show the console metrics: MSE, PSNR, and SSIM.
6. Show the noise-sensitivity graph and iteration-sensitivity graph.
7. State the critical finding: this NLM configuration helps more at stronger noise, while repeated denoising can over-smooth details and reduce PSNR.
8. Close by noting that the original paper used TNRD, so this is a method-level BTB reproduction rather than an exact numerical replication.

## Short opening script

"This project reproduces the Back-to-Basics iterative image denoising framework from Pereg (2024). I create a controlled noisy input using AWGN, use NLM as the base denoiser inside the BTB update, and evaluate the result using MSE, PSNR and SSIM. I also test sensitivity to noise level and iteration count."

## Key viva points

- Higher PSNR generally means the processed image is numerically closer to the reference image.
- Lower MSE is better.
- Higher SSIM means stronger structural similarity to the reference.
- `mu=0.7` gives 70% weight to the current denoised estimate and 30% to the previous estimate.
- `T=3` is a demonstration setting, not a universally optimal value.
- More iterations do not necessarily mean better quality; repeated smoothing can remove fine details.
- The fixed random seed makes the added noise reproducible across runs.
