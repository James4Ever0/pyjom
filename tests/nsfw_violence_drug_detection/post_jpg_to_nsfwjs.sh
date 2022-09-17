curl http://localhost:8511/
echo
curl -X POST -F 'image=@/root/Desktop/works/pyjom/samples/image/dog_saturday_night.jpg' http://localhost:8511/nsfw
echo
curl -X POST -F 'image=@/root/Desktop/works/pyjom/samples/image/dog_saturday_night.bmp' http://localhost:8511/nsfw
echo
curl -X POST -F 'image=@/root/Desktop/works/pyjom/samples/video/cute_cat_gif.gif' http://localhost:8511/nsfw
echo
curl -X POST -F 'image=@/root/Desktop/works/pyjom/samples/image/dog_with_text.png' http://localhost:8511/nsfw
echo