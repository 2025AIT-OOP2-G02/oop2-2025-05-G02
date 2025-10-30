from typing import Optional

import numpy as np
import cv2
from typing import Optional
from my_module.K21999.lecture05_camera_image_capture import MyVideoCapture


def lecture05_01_k24111():

    # カメラキャプチャ実行
    app = MyVideoCapture()
    app.run()

    # 画像をローカル変数に保存
    google_img: Optional[np.ndarray] = cv2.imread("images/google.png")
    if google_img is None:
        raise FileNotFoundError("images/google.png not found or failed to load")

    # キャプチャ画像は run() の実行後に get_img() で取得する
    capture_img: Optional[np.ndarray] = app.get_img()
    if capture_img is None:
        raise RuntimeError(
            "カメラから画像が取得できませんでした。run() 実行後に q を押してキャプチャしてください。"
        )

    g_hight, g_width, g_channel = google_img.shape
    c_hight, c_width, c_channel = capture_img.shape
    print(google_img.shape)
    print(capture_img.shape)

    # キャプチャ画像を (0,0) からグリッド状に並べる
    tiles_y = (g_hight + c_hight - 1) // c_hight
    tiles_x = (g_width + c_width - 1) // c_width
    tiled = np.tile(capture_img, (tiles_y, tiles_x, 1))
    tiled_crop = tiled[:g_hight, :g_width]

    for x in range(g_width):
        for y in range(g_hight):
            b, g, r = google_img[y, x]
            # もし白色(255,255,255)だったら置き換える
            if (b, g, r) == (255, 255, 255):
                google_img[y, x] = tiled_crop[y, x]

    # 書き込み処理
    output_path = "output_images/lecture_05_01_k24111.png"
    if not cv2.imwrite(output_path, google_img):
        raise IOError(f"failed to write {output_path}")
    print(f"Output saved to {output_path}")


if __name__ == "__main__":
    lecture05_01_k24111()
