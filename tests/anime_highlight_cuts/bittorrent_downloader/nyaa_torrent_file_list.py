url = "https://nyaa.si/view/1627038"


        json_data = utils.parse_single(request_text=r.text, site=self.SITE)

        return torrent.json_to_class(json_data)