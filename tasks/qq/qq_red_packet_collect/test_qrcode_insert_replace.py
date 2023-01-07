from ad_template_2_functional import removeAndInsertQRCode
import cv2


def test_main():
    images = [
        "/root/Desktop/works/pyjom/samples/image/qrcode_test/no_qrcode.jpg",
        "/root/Desktop/works/pyjom/samples/image/qrcode_test/with_qrcode.jpg",
    ]  # convert to compatible formats first.

    qrcode_path = "/root/Desktop/works/pyjom/tests/bilibili_video_recommendation_server/ebegging_template.png"

    for img in images:
        output = removeAndInsertQRCode(img, qrcode_path, None)
        cv2.imshow("IMG", output)
        cv2.waitKey(0)


if __name__ == "__main__":
    test_main()
