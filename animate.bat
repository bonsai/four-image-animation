@echo off
REM 4枚の画像から90秒のアニメーションを生成するスクリプト
REM Usage: animate.bat image1.png image2.png image3.png image4.png

if "%~4"=="" (
    echo Usage: %~nx0 ^<image1^> ^<image2^> ^<image3^> ^<image4^>
    exit /b 1
)

set IMG1=%~1
set IMG2=%~2
set IMG3=%~3
set IMG4=%~4
set OUTPUT=output.mp4
set DURATION=90
set FPS=30
set FADE=1
set IMG_DURATION=22

echo Creating 90-second animation from 4 images...
echo Images: %IMG1%, %IMG2%, %IMG3%, %IMG4%

REM 画像をリサイズ
ffmpeg -y -i "%IMG1%" -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" tmp_img1.png 2>nul
ffmpeg -y -i "%IMG2%" -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" tmp_img2.png 2>nul
ffmpeg -y -i "%IMG3%" -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" tmp_img3.png 2>nul
ffmpeg -y -i "%IMG4%" -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" tmp_img4.png 2>nul

REM フェード付きスライドショー生成
ffmpeg -y ^
    -loop 1 -t %IMG_DURATION% -i tmp_img1.png ^
    -loop 1 -t %IMG_DURATION% -i tmp_img2.png ^
    -loop 1 -t %IMG_DURATION% -i tmp_img3.png ^
    -loop 1 -t %IMG_DURATION% -i tmp_img4.png ^
    -filter_complex ^
        "[0:v]fade=t=in:st=0:d=%FADE%,fade=t=out:st=%IMG_DURATION%-1:d=%FADE%[v0]; ^
         [1:v]fade=t=in:st=0:d=%FADE%,fade=t=out:st=%IMG_DURATION%-1:d=%FADE%[v1]; ^
         [2:v]fade=t=in:st=0:d=%FADE%,fade=t=out:st=%IMG_DURATION%-1:d=%FADE%[v2]; ^
         [3:v]fade=t=in:st=0:d=%FADE%,fade=t=out:st=%IMG_DURATION%-1:d=%FADE%[v3]; ^
         [v0][v1][v2][v3]concat=n=4:v=1:a=0[out]" ^
    -map "[out]" ^
    -c:v libx264 ^
    -pix_fmt yuv420p ^
    -r %FPS% ^
    -t %DURATION% ^
    "%OUTPUT%"

REM 一時ファイルを削除
del /q tmp_img*.png 2>nul

echo Done! Output: %OUTPUT%
