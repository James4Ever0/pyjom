url = "https://media3.giphy.com/media/wTrXRamYhQzsY/giphy.gif?cid=dda24d502m79hkss38jzsxteewhs4e3ocd3iqext2285a3cq&rid=giphy.gif&ct=g"

# url = "https://media3.giphy.com/media/J9asIpW5apX7cjT2oh/giphy.gif"
option = 3

if option == 1:
    import yt_dlp
    # import pyidm
    path = "./randomName.mp4"
    x = yt_dlp.YoutubeDL({"outtmpl":path,'format':'[ext=mp4]'})
    y = x.download([url])
    breakpoint()
elif option == 2:
    from pySmartDL import SmartDL

    dest = "./test.gif"
    obj = SmartDL(url, dest, threads=20)
    obj.start()
    # [*] 0.23 Mb / 0.37 Mb @ 88.00Kb/s [##########--------] [60%, 2s left]
    print('DOWNLOAD FINISHED')
    path = obj.get_dest()
    print("DOWNLOADED AT:", path)
elif option == 3:
    from firedm import FireDM
    args = ["-o","./test.gif", url]
    settings = FireDM.pars_args(args)
    urls = settings.pop('url')
    controller = FireDM.Controller(view_class=FireDM.CmdView, custom_settings=settings)
    controller.run()
    controller.cmdline_download(urls, **settings)
    print('FireDM download complete')
