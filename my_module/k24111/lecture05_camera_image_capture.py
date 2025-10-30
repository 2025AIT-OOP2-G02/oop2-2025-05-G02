import numpy as np
import cv2


class MyVideoCapture:
    """Webカメラから1枚キャプチャして取得する簡易クラス。

    run() を実行してウィンドウでプレビューし、'q' で終了すると最後に取得したフレームを
    get_img() で取り出せます。ファイルへの保存機能はこのモジュールには実装しません。
    """

    DELAY: int = 100

    def __init__(self) -> None:
        # デフォルトカメラを開く。必要なら 1 に変更してください。
        self.cap: cv2.VideoCapture = cv2.VideoCapture(0)
        # 要求されているキャプチャサイズに合わせる
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.captured_img: np.ndarray | None = None

    def run(self) -> None:
        """カメラを起動してフレームを表示。'q' 押下で終了して最後のフレームを保持する。"""
        if not self.cap.isOpened():
            # try opening with index 1 as fallback
            self.cap = cv2.VideoCapture(1)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            # 表示用に左右反転（好みで変更可）
            disp = cv2.flip(frame, 1)
            cv2.imshow("camera - press q to capture", disp)

            if cv2.waitKey(self.DELAY) & 0xFF == ord("q"):
                # 保存は行わずにインスタンス内に保持する
                self.captured_img = frame
                break

    def get_img(self) -> np.ndarray | None:
        """最後にキャプチャしたフレームを返す（BGR）"""
        return self.captured_img

    def __del__(self) -> None:
        try:
            if hasattr(self, "cap") and self.cap.isOpened():
                self.cap.release()
        finally:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    app = MyVideoCapture()
    app.run()
    img = app.get_img()
    if img is None:
        print("No image captured")
    else:
        print("Image captured (in-memory).")
