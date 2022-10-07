# seq = [0,1,2,3,4,5,6] # 7
# duration = 4


from vidpy import Composition, Clip
def gen_video(vname, seq, duration):
    mduration = duration / len(seq)

    clips = []
    width,height =1920,1080
    fps=60

    orig_fps = 24

    shift = fps/orig_fps

    for i,s in enumerate(seq):
        codec = str(s)
        codec = "0"*(4-len(codec)) + codec
        path = "/root/Desktop/works/bilibili_tarot/demo_typography/screenshot{}.png".format(codec)
        start = i*mduration
        end = start + mduration
        print(start,end)
        clip = Clip(path,output_fps=fps,start=0,end=mduration*shift,offset = start*shift,profile_override = {"fps":60,"width": width, "height": height})
        clip.vignette()
        clip.dust()
        # clip.charcoal()
        clip.dither(amount=0.10)
        # clip.
        # clip.pixelize()
        clip.pixelize(width = 0.002,height=0.002)
        clips.append(clip)
    # breakpoint()

    # # maybe some other bgm.

    # bgm = Clip(bgm_path,start=0)
    # clips.append(bgm)
    # breakpoint()
    comp = Composition(clips,duration=duration,fps=fps,width=width,height=height)

    comp.save(vname,fps=60,duration = duration,width=width,height=height)