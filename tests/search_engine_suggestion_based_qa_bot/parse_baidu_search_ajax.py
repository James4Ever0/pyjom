import pyjq

def getBaiduImageSearchAjaxInfoParsed(obj, debug=False):
    commonFilter = "select(.extData) | .extData.showInfo | select(. != null) | {titles, snippets, imgs_src, simi} | select (.titles !=null)"
    def standardJsonParser(obj):
        command = ".data.cardData[] | {}".format(commonFilter)
        processed_obj = pyjq.first(command, obj)
        return processed_obj
    def hiddenJsParser(obj):
        processed_obj = obj
        for index in range(3):
            data = pyjq.first(".data.commonData.js[{}]".format(index), obj2)
            if not ('titles' in data and 'titles_url' in data):
                continue
            lines = data.split("\n")
            for line in lines:
                line = line.strip()
                hint = "var cardData = "
                # print(line)
                if line.startswith(hint):
                    import javascript
                    cardData = javascript.eval_js(line.replace(hint,"")).valueOf()
                    real_data = pyjq.first(commonFilter,cardData)
                    # import pprint
                    return real_data
                    # pprint.pprint(real_data)
    import pandas as pd
    processed_obj = None
    methods = [standardJsonParser,hiddenJsParser]
    for method in methods:
        try:
            processed_obj = method(obj)
            if processed_obj is not None:
                break
        except:
            ...
    if processed_obj is None:
        if debug:
            print('cannot parse info from obj')
    # print(processed_obj)
    # breakpoint()
    # from pprint import pprint
    # pprint(processed_obj)
    title_snippets = pyjq.first("{titles, snippets}", processed_obj)
    img_sim = pyjq.first("(.simi[]|=tonumber )|{imgs_src, simi}", processed_obj) # TODO: error! what is going on?
    # img_sim["simi"] = img_sim["simi"] # what is this?
    # [('titles', 15), ('snippets', 15), ('imgs_src', 43), ('simi', 43)]
    # 15, 15, 43, 43
    df_title_snippets = pd.DataFrame(title_snippets)
    df_img_sim = pd.DataFrame(img_sim)
    elem = df_img_sim["simi"][0]

    if debug:
        print(df_title_snippets.head())
        print(df_img_sim.head())
        print(type(elem), elem)  # str?
    # breakpoint()
    from urllib.parse import parse_qs


    def getWidthHeight(url):
        qs = url.split("?")[-1]
        mdict = parse_qs(qs)
        # print(mdict)
        # breakpoint()
        width = int(mdict["w"][0])
        height = int(mdict["h"][0])
        area = width * height
        return width, height, area


    # pre_qs = df_img_sim['imgs_src'].split("?")
    width_height = df_img_sim["imgs_src"].apply(
        lambda v: pd.Series(getWidthHeight(v), index=["width", "height", "area"])
    )
    df_img_sim_width_height = pd.concat([df_img_sim, width_height], axis=1, join="inner")
    # qs = parse_qs(pre_qs)
    # print(qs)
    if debug:
        print(df_img_sim_width_height.head())
    return df_title_snippets, df_img_sim_width_height

# the "js" response may contain video info which may help with our reverse video search.
# but the keyword also helps!
if __name__ == "__main__":
    from lazero.filesystem.io import readJsonObjectFromFile
    # obj = readJsonObjectFromFile("ajax_baidu.json")
    obj2 = readJsonObjectFromFile("jq_image_2.json")
    getBaiduImageSearchAjaxInfoParsed(obj2, debug=True)