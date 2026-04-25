from pathlib import Path

import cv2
import numpy as np
import mss


def locate_on_screen(
    needle_img_path: str | Path,
    confidence: float = 0.8,
    region: tuple[int, int, int, int] | None = None
) -> tuple[int, int, int, int] | None:
    """
    Efficiently locate an image on the screen.

    :param needle_img_path: Path to the image to search for (needle).
    :param confidence: Minimum confidence (0.0 to 1.0) for a match.
    :param region: A tuple (left, top, width, height) to restrict the search area.
    :return: (x, y, width, height) of the top‑left corner of the found region,
             or None if no match exceeds the confidence.
    """
    # 1. Fast screen capture with mss
    with mss.mss() as sct:
        if region:
            monitor = {
                "left": region[0],
                "top": region[1],
                "width": region[2],
                "height": region[3],
            }
        else:
            monitor = sct.monitors[1]  # primary monitor

        # Grab the screenshot (returns BGRA, shape (H, W, 4))
        screenshot = sct.grab(monitor)
        # Convert to a numpy array (H, W, 4) -> drop alpha -> BGR
        img_bgr = np.array(screenshot)[:, :, :3]  # BGR
        # Convert to grayscale for template matching (still fast)
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # 2. Load the needle image in grayscale
    needle_bgr = cv2.imread(needle_img_path, cv2.IMREAD_COLOR)
    if needle_bgr is None:
        raise FileNotFoundError(f"Needle image not found: {needle_img_path}")
    needle_gray = cv2.cvtColor(needle_bgr, cv2.COLOR_BGR2GRAY)
    h, w = needle_gray.shape

    # 3. Template matching using the normalised correlation coefficient
    result = cv2.matchTemplate(img_gray, needle_gray, cv2.TM_CCOEFF_NORMED)

    # 4. Find the location with the highest confidence
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 5. If the confidence is high enough, return the top-left coordinate and size
    if max_val >= confidence:
        x, y = max_loc
        # Adjust coordinates if a region was given
        if region:
            x += region[0]
            y += region[1]
        return (x, y, w, h)

    return None
