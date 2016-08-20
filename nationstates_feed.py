#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from pyquery import PyQuery as pq


def dl_parse(url):
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        events = []
        dom = pq(r.text, parser="html")
        elements = dom.find("li")
        for element in elements.items():
            time = element.find("time").attr("data-epoch")
            path = "https://www.nationstates.net/{}".format(
                element.find("a").attr("href"))
            flag = "https://www.nationstates.net{}".format(
                element.find("img.miniflag").attr("src"))
            nation = element.find("span").text()
            element.remove("time, img")
            text = element.text()[2:].replace(" , ", ", ")
            events.append({
                'time': int(time),
                'uri': path,
                'flag_uri': flag,
                'name': nation,
                'text': text
            })

        return json.dumps(events, indent=4)
    else:
        return None

if __name__ == "__main__":
    print(dl_parse(
        "https://www.nationstates.net/page=ajax2/a=reports/view=region.martial_arts_dojo"))
