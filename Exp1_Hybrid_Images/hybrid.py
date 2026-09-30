import sys
sys.path.append('/Users/kb/bin/opencv-3.1.0/build/lib/')

import cv2
import numpy as np

def cross_correlation_2d(img, kernel):
    '''Given a kernel of arbitrary m x n dimensions, with both m and n being
    odd, compute the cross correlation of the given image with the given
    kernel, such that the output is of the same dimensions as the image and that
    you assume the pixels out of the bounds of the image to be zero. Note that
    you need to apply the kernel to each channel separately, if the given image
    is an RGB image.

    Inputs:
        img:    Either an RGB image (height x width x 3) or a grayscale image
                (height x width) as a numpy array.
        kernel: A 2D numpy array (m x n), with m and n both odd (but may not be
                equal).

    Output:
        Return an image of the same dimensions as the input image (same width,
        height and the number of color channels)
    '''
    img = np.asarray(img)
    kernel = np.asarray(kernel, dtype=np.float32)

    if img.ndim not in (2, 3):
        raise ValueError("img must be a grayscale or RGB image")
    if kernel.ndim != 2 or kernel.shape[0] % 2 == 0 or kernel.shape[1] % 2 == 0:
        raise ValueError("kernel must be a 2D array with odd dimensions")

    kernel_height, kernel_width = kernel.shape
    pad_height = kernel_height // 2
    pad_width = kernel_width // 2
    padded = np.pad(
        img.astype(np.float32),
        ((pad_height, pad_height), (pad_width, pad_width))
        if img.ndim == 2
        else ((pad_height, pad_height), (pad_width, pad_width), (0, 0)),
        mode='constant',
        constant_values=0,
    )

    output = np.zeros(img.shape, dtype=np.float32)
    if img.ndim == 2:
        for row in range(img.shape[0]):
            for column in range(img.shape[1]):
                region = padded[row:row + kernel_height, column:column + kernel_width]
                output[row, column] = np.sum(region * kernel)
    else:
        for row in range(img.shape[0]):
            for column in range(img.shape[1]):
                region = padded[row:row + kernel_height, column:column + kernel_width, :]
                output[row, column, :] = np.sum(region * kernel[:, :, None], axis=(0, 1))

    return output

def convolve_2d(img, kernel):
    '''Use cross_correlation_2d() to carry out a 2D convolution.

    Inputs:
        img:    Either an RGB image (height x width x 3) or a grayscale image
                (height x width) as a numpy array.
        kernel: A 2D numpy array (m x n), with m and n both odd (but may not be
                equal).

    Output:
        Return an image of the same dimensions as the input image (same width,
        height and the number of color channels)
    '''
    kernel = np.asarray(kernel)
    return cross_correlation_2d(img, np.flip(kernel, axis=(0, 1)))

def gaussian_blur_kernel_2d(sigma, height, width):
    '''Return a Gaussian blur kernel of the given dimensions and with the given
    sigma. Note that width and height are different.

    Input:
        sigma:  The parameter that controls the radius of the Gaussian blur.
                Note that, in our case, it is a circular Gaussian (symmetric
                across height and width).
        width:  The width of the kernel.
        height: The height of the kernel.

    Output:
        Return a kernel of dimensions height x width such that convolving it
        with an image results in a Gaussian-blurred image.
    '''
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    if height <= 0 or width <= 0 or height % 2 == 0 or width % 2 == 0:
        raise ValueError("height and width must be positive odd numbers")

    rows = np.arange(height, dtype=np.float32) - height // 2
    columns = np.arange(width, dtype=np.float32) - width // 2
    x, y = np.meshgrid(columns, rows)
    kernel = np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))
    return (kernel / np.sum(kernel)).astype(np.float32)

def low_pass(img, sigma, size):
    '''Filter the image as if its filtered with a low pass filter of the given
    sigma and a square kernel of the given size. A low pass filter supresses
    the higher frequency components (finer details) of the image.

    Output:
        Return an image of the same dimensions as the input image (same width,
        height and the number of color channels)
    '''
    kernel = gaussian_blur_kernel_2d(sigma, size, size)
    return convolve_2d(img, kernel)

def high_pass(img, sigma, size):
    '''Filter the image as if its filtered with a high pass filter of the given
    sigma and a square kernel of the given size. A high pass filter suppresses
    the lower frequency components (coarse details) of the image.

    Output:
        Return an image of the same dimensions as the input image (same width,
        height and the number of color channels)
    '''
    return np.asarray(img, dtype=np.float32) - low_pass(img, sigma, size)

def create_hybrid_image(img1, img2, sigma1, size1, high_low1, sigma2, size2,
        high_low2, mixin_ratio):
    '''This function adds two images to create a hybrid image, based on
    parameters specified by the user.'''
    high_low1 = high_low1.lower()
    high_low2 = high_low2.lower()

    if img1.dtype == np.uint8:
        img1 = img1.astype(np.float32) / 255.0
        img2 = img2.astype(np.float32) / 255.0

    if high_low1 == 'low':
        img1 = low_pass(img1, sigma1, size1)
    else:
        img1 = high_pass(img1, sigma1, size1)

    if high_low2 == 'low':
        img2 = low_pass(img2, sigma2, size2)
    else:
        img2 = high_pass(img2, sigma2, size2)

    img1 *= 2 * (1 - mixin_ratio)
    img2 *= 2 * mixin_ratio
    hybrid_img = (img1 + img2)
    return (hybrid_img * 255).clip(0, 255).astype(np.uint8)


