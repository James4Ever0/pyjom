curl http://localhost:8511/
echo
echo
curl -X POST -F 'image=@/root/Desktop/works/pyjom/samples/image/dog_saturday_night.jpg' http://localhost:8511/nsfw
echo
echo
curl -X POST -F 'image=@/root/Desktop/works/pyjom/samples/image/dog_saturday_night.bmp' http://localhost:8511/nsfw
echo
echo
curl -X POST -F 'image=@/root/Desktop/works/pyjom/samples/video/cute_cat_gif.gif' http://localhost:8511/nsfw
echo
echo
curl -X POST -F 'image=@/root/Desktop/works/pyjom/samples/image/dog_with_text.png' http://localhost:8511/nsfw
echo
echo
curl -X POST -F 'image=@/root/Desktop/works/pyjom/samples/image/dog_with_text.jpg' http://localhost:8511/nsfw
echo
echo
curl -X POST -F 'image=@/root/Desktop/works/pyjom/samples/image/dog_with_text.bmp' http://localhost:8511/nsfw
echo
echo
# but the bmp looks right. is that the format issue?
# we have consistency with the original model. how about a real porno?
