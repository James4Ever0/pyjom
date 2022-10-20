ffmpeg -y -i anime.gif -loop 1 -t 1 -i ad_2_mask.png
  -filter_complex
      "color=black:d=1[c];[c][0]scale2ref[cs][v];[cs]setsar=1[ct];
       [1:v]alphaextract,negate[m];[m][ct]scale2ref[ms][ol];[ms]setsar=1[alf];
       [ol][alf]alphamerge[fin];
       [v][fin]overlay,scale‌​=$WIDTH:$HEIGHT:force_orig‌​inal_aspect_ratio=de‌​crease[fv];
       [fv]pad=6‌$WIDTH:$HEIGHT:(ow-iw)/2:(o‌​h-ih)/2:#000000@1[v]‌​"
-map "[v]" -map 0:a output.mp4