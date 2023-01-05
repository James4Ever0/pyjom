from ad_template_2_functional import generateBilibiliVideoAd, getAdLock

videoData = [
    [
        "BV1Qd4y177Tc",
        "bbb",
        "https://i0.hdslb.com/bfs/archive/8a5f0a2bdffc99d33776c9d1f101521c0fc85e31.jpg",
    ],
    [
        "BV1FG411K7Cd",
        "aaa",
        "https://i2.hdslb.com/bfs/archive/6423c88a8d3011a6a911627d9100b4cc4f08758d.jpg",
    ],
]

import cv2

for (bvid, title_text, image_link) in videoData:
    with getAdLock():
        output_path, output_standalone, output_masked_path = generateBilibiliVideoAd(
            bvid, title_text, image_link
        )
        img = cv2.imread(output_path)
        cv2.imshow("IMAGE", img)
        cv2.waitKey(0)
