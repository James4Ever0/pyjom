

def OnlinePoster(content, iterate=False, contentType='video',postMetadataGenerator=postMetadataGenerator, platform='bilibili'):
    poster = {'bilibili':BilibiliPoster}