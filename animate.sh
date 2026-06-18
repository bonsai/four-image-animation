#!/bin/bash

# 4枚の画像から90秒のアニメーションを生成するスクリプト
# Usage: ./animate.sh image1.png image2.png image3.png image4.png

set -e

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <image1> <image2> <image3> <image4>"
    exit 1
fi

IMG1="$1"
IMG2="$2"
IMG3="$3"
IMG4="$4"
OUTPUT="output.mp4"
DURATION=90
FPS=30
TRANSITION=2
FADE=1

# 各画像の表示時間（秒）
# 90秒 ÷ 4枚 = 22.5秒、トランジション分を考慮
IMG_DURATION=22.5

echo "Creating 90-second animation from 4 images..."
echo "Images: $IMG1, $IMG2, $IMG3, $IMG4"

# 画像をリサイズして一時ファイルに保存
for i in 1 2 3 4; do
    eval "img=\$IMG$i"
    ffmpeg -y -i "$img" -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" "tmp_img$i.png" 2>/dev/null
done

# フェードイン/アウト付きのスライドショーを生成
ffmpeg -y \
    -loop 1 -t $IMG_DURATION -i tmp_img1.png \
    -loop 1 -t $IMG_DURATION -i tmp_img2.png \
    -loop 1 -t $IMG_DURATION -i tmp_img3.png \
    -loop 1 -t $IMG_DURATION -i tmp_img4.png \
    -filter_complex "
        [0:v]fade=t=in:st=0:d=$FADE,fade=t=out:st=$((IMG_DURATION-FADE)):d=$FADE[v0];
        [1:v]fade=t=in:st=0:d=$FADE,fade=t=out:st=$((IMG_DURATION-FADE)):d=$FADE[v1];
        [2:v]fade=t=in:st=0:d=$FADE,fade=t=out:st=$((IMG_DURATION-FADE)):d=$FADE[v2];
        [3:v]fade=t=in:st=0:d=$FADE,fade=t=out:st=$((IMG_DURATION-FADE)):d=$FADE[v3];
        [v0][v1][v2][v3]concat=n=4:v=1:a=0[out]
    " \
    -map "[out]" \
    -c:v libx264 \
    -pix_fmt yuv420p \
    -r $FPS \
    -t $DURATION \
    "$OUTPUT"

# 一時ファイルを削除
rm -f tmp_img*.png

echo "Done! Output: $OUTPUT"
