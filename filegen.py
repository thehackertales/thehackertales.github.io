import base64
from pyDes import *
import glob
from pathlib import Path
import json
import os
from urllib.parse import quote_plus

def setDecipher():
    return des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)

def downloadURL(songurl):
    des_cipher = setDecipher()
    try:
        enc_url = base64.b64decode(songurl.strip())
        dec_url = des_cipher.decrypt(
            enc_url, padmode=PAD_PKCS5).decode('utf-8')
        dec_url = dec_url.replace('_96.mp4', '_320.mp4')
        return dec_url
    except Exception as e:
        print('Song URL Error' + str(e))

if __name__ == '__main__':
    for file in glob.glob("../meta/0-9/*.json"):
        html = """---
layout: default
title: "Download var1 - var2 var3 album"
description: "Free download var4"
metaimg: "var5"
permalink: /albums/var6
---
<div class="sidebar-img">
  <img src="var5" alt="var4">
</div>
<div class="mainbar-contant">
  <h1>Download free songs - var4</h1>
  <div class="album-songs">
    var7
  </div>
</div>"""
        with open(file) as f:
            d = json.load(f)
            var1 = d['title']
            var2 = d['year']
            var3 = d['language']
            var4 = d['header_desc']
            var5 = d['image']
            var6 = quote_plus(var1).replace("+","-").replace(".","-")
            var7 = ''
            for i in d['list']:
                var7 += """
                <div class="song">
                  <h2 class="song-title">svar1</h2>
                  <p class="song-subtitle">svar2</p>
                  <p class="song-music">Music: svar3</p>
                  <a rel="noopener noreferrer nofollow" target="_blank" href="svar4" download>{% include icon-download.html %}Download Now</a>
                </div>
                """
                var7 = var7.replace("svar1", i['title'])
                var7 = var7.replace("svar2", i['subtitle'])
                var7 = var7.replace("svar3", i['more_info']['music'])
                var7 = var7.replace("svar4", downloadURL(i['more_info']['encrypted_media_url']) or "#")
            html = html.replace("var1", var1).replace("var2", var2).replace("var3", var3).replace("var4", var4).replace("var5", var5).replace("var6", var6).replace("var7", var7)
            file1 = open('./albums/'+ d['id'] +'.html', 'w')
            file1.write(html)
            file1.close()
