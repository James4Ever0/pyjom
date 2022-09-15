from tkinter import *
from pyjom.commons import *
from pyjom.modules.contentCensoring.autoCensor import *

# import tkinter.font
import requests
import traceback
import os
import command_spawner
from progressbar import *

# add progressbar
def mediaDownloader(url, mblogid, basedir=None, index=None):
    try:
        r = requests.get(url)  # what is the media file suffix?
        suffix = url.split("?")[0].split(".")[-1]
        mid = mblogid if index is None else "{}[{}]".format(mblogid, index)
        fname = "{}.{}".format(mid, suffix)
        if not os.path.exists(basedir):
            os.mkdir(basedir)
        fpath = os.path.join(basedir, fname)
        size = int(r.headers["Content-Length"].strip())
        mbytes = 0
        widgets = [
            fpath,
            ": ",
            Bar(marker="|", left="[", right=" "),
            Percentage(),
            " ",
            FileTransferSpeed(),
            "] ",
            " of {0}MB".format(str(round(size / 1024 / 1024, 2))[:4]),
        ]
        pbar = ProgressBar(widgets=widgets, maxval=size).start()
        mfile = []
        for buf in r.iter_content(1024):
            if buf:
                mfile.append(buf)
                mbytes += len(buf)
                pbar.update(mbytes)
        pbar.finish()
        print("saved to {}".format(fpath))
        with open(fpath, "wb") as f:
            for byteContent in mfile:
                f.write(byteContent)
        return fpath
    except:
        traceback.print_exc()
        print("error in mediaDownloader:\n", url)
    return None

x_buffer = None
tag_x_offset =None
tag_y_counter =None

def censorInterface(
    mtitle, mtopic, mcontent,mtags=[], local=False
):  # this could be a standard template.
    global x_buffer,tag_x_offset,tag_y_counter
    assert type(mtopic) == list
    assert type(mtags) == list
    is_on = {key:False for key in mtags}
    def switch(key, buttons, index, is_on):
        button = buttons[index]
        if is_on[key]:
            button.config(text=key ,bg = "grey",fg="black")
            is_on[key] = False
        else:
            button.config(text = key,bg = "green",fg="white")
            is_on[key] = True


    def getSwitchLambda(text, on_buttons, index, is_on):
        return lambda:switch(text, on_buttons, index, is_on)

    on_buttons = []
    mfunctions = []


    mdata = {"labels": [], "comment": None, "discard": False}
    left, top = 1500, 500
    parent = Tk()
    parent.geometry("+{}+{}".format(left, top))
    # parent
    default_window_size =(460,400)
    parent.geometry("{0}x{1}".format(*default_window_size))
    themepath = joinScriptFileBaseDir(__file__, "Forest-ttk-theme/forest-dark.tcl")
    parent.tk.call("source", themepath)
    parent.attributes("-topmost", True)
    if not local:
        title = Label(
            parent,
            text="Title:" + "\n" * 4,
            fg="white",
        )
        title.grid(row=0, column=0, sticky="e")
        text0 = Text(fg="aqua", height=5, width=24)
        text0.grid(row=0, column=1)
        text0.insert(END, mtitle)

        # print(mtopic)
        mlabel = (  # not designed for sina topic format.
            "None" if mtopic == None else " ".join(["[{}]".format(x) for x in mtopic])
        )
        label = Label(
            parent,
            text="Topics:" + "\n" * 4,
            fg="aqua",
        )
        label.grid(row=1, column=0, sticky="e")
        text1 = Text(fg="aqua", height=5, width=24)
        text1.grid(row=1, column=1)
        text1.insert(END, mlabel)

        content = Label(
            parent,
            text="Content:" + "\n" * 4,
            fg="white",
        )
        content.grid(row=2, column=0, sticky="e")
        text2 = Text(fg="aqua", height=5, width=24)
        text2.grid(row=2, column=1)
        text2.insert(END, mcontent)

        conrow = 3
    else:
        conrow = 0
    redbutton = Entry(parent, fg="red")
    redbutton.grid(row=0 + conrow, column=1, sticky="ew")

    # button_height = 32 # default height?
    x_buffer = 10
    tag_x_offset = 0
    tag_y_counter = 0
    # print("TEXT:", text)
    def placeTagButtons(index, text,tag_x_offset, tag_y_counter, x_buffer, on=False):
        # global
        if not on:
            mButton = Button(parent, text=text, bd = 0,bg="grey",fg="black")
        else:
            mButton = Button(parent, text=text, bd = 0,bg="green",fg="white")
        button_width = mButton.winfo_reqwidth()
        # 65
        button_height = mButton.winfo_reqheight()
        # print(button_width, button_height)
        # breakpoint()

        on_buttons.append(mButton)
        mfunctions.append(getSwitchLambda(text, on_buttons, index, is_on))
        on_buttons[index].config(command=mfunctions[index])
        # on_buttons[index].grid_forget()
        estimate_x_size = tag_x_offset+x_buffer+button_width
        estimated_y_size = default_window_size[1]+ button_width*1.3*(tag_y_counter+1)
        if estimate_x_size > default_window_size[0]:
            tag_x_offset = 0
            tag_y_counter+=1
            # change window geometry
            parent.geometry("{0}x{1}".format(default_window_size[0], int(default_window_size[1]+ button_height*0.1+(tag_y_counter+1)*button_height*1.2)))
        elif estimated_y_size > default_window_size[1]:
            parent.geometry("{0}x{1}".format(default_window_size[0], int(default_window_size[1]+ button_height*0.1+(tag_y_counter+1)*button_height*1.2)))
        on_buttons[index].place(x=tag_x_offset+x_buffer, y=default_window_size[1]+ button_height*0.1+tag_y_counter*button_height*1.2)
        tag_x_offset+= button_width
        return tag_x_offset,tag_y_counter
        # print(dir(mButton))
    for index, text in enumerate(is_on.keys()):
        tag_x_offset,tag_y_counter = placeTagButtons(index, text, tag_x_offset,tag_y_counter, x_buffer)
        # 32
        # breakpoint()

    def add_tag():
        global tag_x_offset, tag_y_counter, x_buffer
        mtext = redbutton.get()
        mtext = mtext.strip()
        if mtext != "": # that is the base line
            redbutton.delete(0, END)
            # change this shit.
            # mdata["labels"].append(mtext)
            if mtext not in is_on.keys():
                is_on.update({mtext:True}) # enable this tag anyway.
                # and we do some append task here.
                tag_x_offset, tag_y_counter=placeTagButtons(len(on_buttons), mtext,tag_x_offset, tag_y_counter, x_buffer, on=True)

    bluebutton = Button(parent, text="ADD TAG", fg="aqua", command=add_tag)
    bluebutton.grid(row=0 + conrow, column=0, sticky="e")

    redbutton3 = Label(parent, text="Comment:", fg="red")
    redbutton3.grid(row=1 + conrow, column=0, sticky="e")
    redbutton2 = Entry(parent, fg="red")

    def add_comment():
        comment = redbutton2.get()
        if comment != "":
            mdata["comment"] = comment

    redbutton2.grid(row=1 + conrow, column=1, sticky="ew")

    def mdestroy():
        add_tag()
        add_comment()
        parent.destroy()

    def mdestroy2():
        mdata["discard"] = True
        parent.destroy()

    blackbutton = Button(parent, text="SUBMIT", fg="red", command=mdestroy)
    blackbutton.grid(row=1 + conrow, column=2, sticky="e")
    blackbutton2 = Button(parent, text="KILL", fg="yellow", command=mdestroy2)
    blackbutton2.grid(row=0 + conrow, column=2, sticky="ew")
    parent.bind("<Return>", lambda event=None: bluebutton.invoke())
    parent.bind("<Control-Return>", lambda event=None: mdestroy())
    parent.bind("<KeyRelease>", lambda event=None:  print("KEY RELEASED!"))
    parent.mainloop()
    mdata["labels"] = [x for x in is_on.keys() if is_on[x]]
    mdata["total_labels"] = [x for x in is_on.keys()]
    return mdata


def playMedia(mediaPath):
    cmdline = "ffplay -alwaysontop -loop 0 -top 0 -left 0 {}".format(mediaPath)
    cs = command_spawner.CommandSpawner(command=cmdline, daemon=True)
    cs.run()
    return cs


def coreMediaCensor(
    mediaPath,
    meta,
    play=True,
    auto=False,
    semiauto=True,
    local=False,
    dummy_auto=True,
    args={},
    template_names=[],
):
    assert type(local) == bool
    mtitle, mtopic, mcontent = meta
    censor_method = (
        keywordDecorator(autoCensor, args=args, template_names=template_names)
        if not dummy_auto
        else dummyAutoCensor
    )
    if ((not auto) or semiauto) and play:
        cs = playMedia(mediaPath)  # siderun.
        if not auto:
            mdata = censorInterface(mtitle, mtopic, mcontent, local=local)
        else:
            nextData = censor_method(
                mediaPath, meta, semiauto=semiauto
            )  # this will not approve the thing. only generate tags and metadata.
            mdata = censorInterface(mtitle, mtopic, mcontent, local=True)
            mdata.update(nextData)
    else:
        mdata = censor_method(mediaPath, meta, semiauto=semiauto)
    if ((not auto) or semiauto) and play:
        cs.kill()
        os.system("killall ffplay")
    return mdata


@decorator
def weiboCensor(
    content,
    basedir=None,
    auto=False,
    semiauto=True,
    dummy_auto=True,
    args={},
    template_names=[],
):
    groupArgs = {
        "template_names": template_names,
        "auto": auto,
        "semiauto": semiauto,
        "dummy_auto": dummy_auto,
        "args": args,
    }
    if (not auto) or semiauto:
        os.system("killall ffplay")
    # we only need video.
    data = {"type": "text", "review": None}
    mtitle = content["title"]
    mtopic = (
        None if content["topic"] is None else [x[0] for x in content["topic"]]
    )  # excerpt the topic name only
    mcontent = content["text"]["raw"]
    meta = (mtitle, mtopic, mcontent)
    if content["video"] is not None:
        data["type"] = "video"
        videoUrl = content["video"]["download_link"]
        mblogid = content["meta"]["mblogid"]
        videoPath = mediaDownloader(videoUrl, mblogid, basedir=basedir)
        mdata = coreMediaCensor(videoPath, meta, **groupArgs)
        data["review"] = (videoPath, mdata)
        # return mdata
    elif content["picture"] is not None and content["picture"] is not []:
        data["type"] = "picture"
        data["review"] = []
        for index, pictureUrl in enumerate(content["picture"]):
            picturePath = mediaDownloader(
                pictureUrl, mblogid, basedir=basedir, index=index
            )
            mdata = coreMediaCensor(picturePath, meta, **groupArgs)
            data["review"].append((picturePath, mdata))
    else:
        # just display the raw content.
        mdata = coreMediaCensor(
            None, meta, play=False, **groupArgs
        )  # how to automate this shit?
        data["review"] = mdata
    return data


@decorator
def localCensor(
    content, auto=False, semiauto=True, dummy_auto=True, args={}, template_names=[]
):
    # examine local files.
    # first determine the content type.
    groupArgs = {
        "auto": auto,
        "semiauto": semiauto,
        "dummy_auto": dummy_auto,
        "template_names": template_names,
        "args": args,
    }
    if (not auto) or semiauto:
        os.system("killall ffplay")
    # you may play the media as well.
    data = {"type": None, "review": None}
    mediaTypes = ["picture", "video"]
    if content["type"] in mediaTypes:
        data["type"] = content["type"]
        mediaPath = content["path"]
        mdata = coreMediaCensor(mediaPath, (None, None, None), local=True, **groupArgs)
        # review as video.
        data["review"] = (mediaPath, mdata)
    else:
        raise Exception("Unknown Content Type: {}\n{}".format(content["type"], content))
    return data
