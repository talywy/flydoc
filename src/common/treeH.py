#!/usr/bin/env python
#-*- coding: utf-8 -*-

""" IFLYTEK Education Division Architecture Team

@author:     shenghe <shenghe@iflytek.com>
@license:    (C) 2013, iFlyTEK CO.Ltd. All rights reserved.
              IFLYTEK Education Division Architecture Team
@version:    $Id$
"""
import os
import re
from datetime import datetime
from pinyinH import PinyinH


class TreeH:
    @staticmethod
    def getTree(folder, rooturl=".", rootpath="/", filters=None):
        """
            return:
            [
                {
                    "name": "",
                    "path": "",
                    "url": "",
                    "output": "",
                    "date": "",
                    "catalog": true,
                    "children": []
                }
            ]
        """
        if filters is None:
            filters = {"files": [], "folders": []}

        return TreeH.lists(folder, rooturl, rootpath, filters)

    @staticmethod
    def lists(folder, rooturl=".", rootpath="/", filters=None):
        if not os.path.isdir(folder):
            return []

        rooturl = PinyinH.loads(rooturl)
        rootpath = PinyinH.loads(rootpath)

        if filters is None:
            filters = {"files": [], "folders": []}

        infos = []
        filesAndFolders = os.listdir(folder)

        # 按照文件名中的序号排序
        filesAndFoldersSorted = []
        index = -1
        for fd in filesAndFolders:
            path = os.path.join(folder, fd)
            extension = os.path.splitext(fd)[1].lower()
            if os.path.isfile(path) and extension not in [".md"]:
                continue

            try:
                if fd.find(".") != -1:
                    nindex = int(fd[:fd.find(".")])
                else:
                    nindex = -1
            except:
                nindex = -1

            if not filesAndFoldersSorted or nindex >= index:
                filesAndFoldersSorted.append(fd)
            else:
                pre = filesAndFoldersSorted[-1]
                filesAndFoldersSorted.remove(pre)
                filesAndFoldersSorted.append(fd)
                filesAndFoldersSorted.append(pre)
            index = nindex

        for fd in filesAndFoldersSorted:
            path = os.path.join(folder, fd)

            filename = os.path.splitext(fd)[0]
            extension = os.path.splitext(fd)[1]

            key = "files" if os.path.isfile(path) else "folders"
            iscontinue = False
            for pattern in filters[key]:
                if re.search(pattern, path) is not None:
                    iscontinue = True
                    break
            if iscontinue:
                continue

            info = {"name": "", "path": "", "url": "#", "output": "", "children": []}

            # 文件名去掉 1.这类排序用符号
            info["name"] = re.sub("-$", "", re.sub("^\d\.", "", filename))
            pinyin = PinyinH.loads(info["name"])

            info["path"] = path
            info["output"] = os.path.join(rootpath, pinyin)
            info["catalog"] = False if filename and filename[-1] == "-" else True
            if os.path.isfile(path):
                info["url"] = "%s/%s.html" % (rooturl, pinyin)
                info["output"] = os.path.join(rootpath, "%s.html" % pinyin)
                info["date"] = datetime.fromtimestamp(
                    os.path.getmtime(path)
                ).strftime("%Y-%m-%d %H:%M:%S")

            if os.path.isdir(path):
                info["children"] = TreeH.lists(
                    path,
                    rooturl="%s/%s" % (rooturl, fd),
                    rootpath=os.path.join(rootpath, fd),
                    filters=filters
                )

            infos.append(info)
        return infos

if __name__ == '__main__':
    print(TreeH.getTree(u"C:/wamp/www/docs", rootpath="C:\\"))
