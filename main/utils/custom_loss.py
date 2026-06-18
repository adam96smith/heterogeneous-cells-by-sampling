from typing import Sequence, Tuple, Optional, Dict, Any, Callable, Union, List
import numpy as np
from scipy.ndimage import gaussian_filter

class LinearComboBlur:
    """
    Creates a linear combination of the orginial and blurred image, then applies random scale and shift the final image.

    Args:
        alpha (list): range for linear combination
        blur_z (list): range of z-blurring
        blur_xy (list): range for planar blurring
        scale (list): range to randomly scale intensities
        shift (list): range to randomly shift intensities
    """
    def __init__(
            self,
            alpha: Sequence[float] = [0.0, 1.0],
            blur_z: Sequence[float] = [0.0, 5.0],
            blur_xy: Sequence[float] = [0.0, 2.0],
            scale: Sequence[float] = [0.8, 1.2],
            shift: Sequence[float] = [-0.1, 0.1],
            inplace: bool = False,
            channels: Optional[Sequence[int]] = None,
    ):
        self.alpha = np.array(alpha)
        self.blur_z = np.array(blur_z)
        self.blur_xy = np.array(blur_xy)
        self.scale = np.array(scale)
        self.shift = np.array(shift)
        
        self.inplace = inplace
        self.channels = channels
        
    def __call__(self,
                 inp: np.ndarray,
                 targets: np.ndarray = None  # returned without modifications
                ) -> Tuple[np.ndarray, np.ndarray]:
        
        if self.inplace:
            output = inp  # Refer to the same memory space
        else:
            output = inp.copy()
        
        channels = range(inp.shape[0]) if self.channels is None else self.channels
        
        for c in channels:
            r_alpha = np.random.uniform(self.alpha[0], self.alpha[1])
            r_blur_z = np.random.uniform(self.blur_z[0], self.blur_z[1])
            r_blur_xy = np.random.uniform(self.blur_xy[0], self.blur_xy[1])
            r_scale = np.random.uniform(self.scale[0], self.scale[1])
            r_shift = np.random.uniform(self.shift[0], self.shift[1])

            im_blurred = r_alpha*inp[c] + (1-r_alpha)*gaussian_filter(inp[c], sigma=(r_blur_z, r_blur_xy, r_blur_xy))

            output[c] = (r_scale * im_blurred) + r_shift
        
        return output, targets

    def __repr__(self):
        return f'Normalize(scale={self.scale}, shift={self.shift}, inplace={self.inplace})'


# stand-alone funtion

def linear_combo_blur(image, alpha, sigma=(1,1,1)):

    assert 0<=alpha<=1

    im_blur = gaussian_filter(image, sigma=sigma)

    return alpha*image + (1-alpha)*im_blur