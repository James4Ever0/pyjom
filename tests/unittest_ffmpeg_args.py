['ffmpeg','-y','-ss', '0', '-to', '59.3942553191489', '-i', '/root/Desktop/works/pyjom/samples/video/LiGlReJ4i.mp4', '-ss', '59.3942553191489', '-to', '62.0340000000000', '-i', '/root/Desktop/works/pyjom/samples/video/LiGlReJ4i.mp4', '-ss', '0', '-to', '62.034', '-i', '/root/Desktop/works/pyjom/samples/video/LiGlReJ4i.mp4', '-filter_complex', '[0:v]crop=h=1099:w=717:x=1:y=72[s0];[s0]pad=color=black:height=max(ih\\, ceil(iw*max(1080/1920\\, ih/iw))):width=max(iw\\, ceil(ih*max(1920/1080\\, iw/ih))):x=floor((max(iw\\, ceil(ih*max(1920/1080\\, iw/ih)))-iw)/2):y=floor((max(ih\\, ceil(iw*max(1080/1920\\, ih/iw)))-ih)/2)[s1];[s1]scale=1920:1080[s2];[s2]scale=ceil((iw*0.15555555555555556)/4)*4:ceil((ih*0.15555555555555556)/4)*4[s3];[1:v]pad=color=black:height=max(ih\\, ceil(iw*max(1080/1920\\, ih/iw))):width=max(iw\\, ceil(ih*max(1920/1080\\, iw/ih))):x=floor((max(iw\\, ceil(ih*max(1920/1080\\, iw/ih)))-iw)/2):y=floor((max(ih\\, ceil(iw*max(1080/1920\\, ih/iw)))-ih)/2)[s4];[s4]scale=1920:1080[s5];[s5]scale=ceil((iw*0.15555555555555556)/4)*4:ceil((ih*0.15555555555555556)/4)*4[s6];[s3][s6]concat=n=2[s7]', '-map', '[s7]', '-map', '2:a', '/dev/shm/2c6b1466-6186-41dd-9ce3-2f757c082c5a.mp4']

print()