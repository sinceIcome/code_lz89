# coding=gbk
'''
主要方法
使用Firefox浏览器，并利用浏览器的开发工具进行分析（快捷键F12进入开发模式）
进入开发工具后，在网络（network）一栏中，可以看到浏览器和服务器之间的互动，其中XHR是浏览器发出的请求
点击具体的条目，可以获得相应的请求信息，包括请求头，参数，cookies，响应等等
'''
'''
主要思路
分析浏览器0.向服务器发送的请求
网页上的"+"对应的是一个gettree.action000000000000000000000000000000000000000
点击具体的条目，对应的是一个getnodeinfo.action
通过gettree.action可以获得每个节点的id，parentID（即上一级的id）以及text（即显示的名称）
通过id和parentID就可以获得filename（即文件在服务器上的名称），可以进一步取得文件的url
'''
'''
代码的实现
1.发送请求，利用requests库
2.对服务器返回的json数据进行处理，利用json库
3.通过id、parentId和text就可以获得下载url，然后下载，将这些写到一个函数里，def DownloadRuls(dict2)
4.需要遍历所有的节点node，直接嵌套循环比较困难，因此采用一层一层处理的方式，并创建每一层的list存放当前层的节点信息，供下一层遍历时调用，代码较多，但思路简单
5.注意各变量的数据类型，信息主要存储在list和dict中'''
import requests
import json

# 定义变量
StrGettree = "http://172.31.120.5:8080/TangcheRule/gettree.action?"
# 用于发送get请求的url，所需参数为systemid和id，可以获得下一层节点的id，parentId和text
StrGetnodeinfo = "http://172.31.120.5:8080/TangcheRule/getnodeinfo.action"
# 用于发送post请求的url，所需参数是id、parentId和posnr（总为"1"），可以获得节点的信息，目前主要用于获取文件的存储位置"filename"，后续持续开发的话，还可以从"detaildata"中取得相关表单和其他信息

# 请求头headers
headers = {
    'Host': '172.31.120.5:8080',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://172.31.120.5:8080/TangcheRule/',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Content-Length': '29'
}

'''' # 获取大类分类以及相应的systemid
SortList_raw = requests.get("http://172.31.120.5:8080/TangcheRule/getclass.action").json()["root"]

# 使用requests发送get请求，所获得的response是json数据
# 通过.json()方法，将返回的json数据转化为dict数据
# 通过dict的key ”root“，提取node节点信息，有效信息包括"id"，"systemid"和"text”,也包括无用信息，因此下一步要将有用的信息提取出来
sort_list = []  # 创建一个列表，列表元素的数据类型为dict，用于存储sort级别的id、systemid和text信息
sortInput_list = []  # 创建一个列表，列表元素数据类型为str，用于存储发送请求可能需要的systemid&id参数信息,目前未使用
for i in SortList_raw:
    sort_list.append({"id": i["id"], "systemid": i["systemid"], "text": i["text"]})
    sortInput_list.append("systemid=" + str(i["systemid"]) + "&id=" + str(i["id"]))
#print(sort_list)
#print(sortInput_list)'''

# sort_list包括了术语定义库、角色工作指南等类别，运行可能有问题，所以重新定义了一个列表变量systemid_list，只存储五类信息
systemid_list = [{'id': 5343, 'systemid': 'ZC', 'text': '公司章程'},
                 {'id': 2969, 'systemid': 'NZ', 'text': '公司级行政制度文件'},
                 {'id': 5539, 'systemid': 'DJ', 'text': '公司级党建制度文件'},
                 {'id': 3712, 'systemid': 'DW', 'text': '单位级制度文件'},
                 {'id': 974, 'systemid': 'WW', 'text': '公司外部文件'}
                 ]

# 新建列表、用于存储后续每一层级的node节点信息
node_level1_list = []
node_level2_list = []
node_level3_list = []
node_level4_list = []


# 定义函数，发送get请求，取得node的信息
def getNodeID(dict1, dict2):
    '''先发送get请求获得response，然后字典化，截取信息
    dict1主要是为了保证后续循环体内的systemid不变，
    循环体通过dict2传入
    dict1的数据由列表systemid_list获得，dict1的key包括“id”，“systemid”和”text“
    dict2是dict类型数据，是节点node信息，在此函数中需要利用的key是”id“'''
    list1 = requests.get(StrGettree + "systemid=" + str(dict1["systemid"]) + "&id=" + str(dict2["id"])).json()[
        "root"]  # 发送get请求，通过参数”systemid“和”id“一定可以取得下一层节点的id、parentId和text
    return list1  # 返回一个列表，列表的元素是dict类型数据，key为"id"、"parentId"、"text"

# 定义函数，通过已知的"id"、"parentId"、"text"节点信息，获取文件url，并下载保存文件，并重命名
def DownloadRuls(dict2):  # 传入的参数数据类型为dict，需要的key包括“id”、“parentId”和“text”

    # 定义一个函数，保存文件，并对文件重命名
    def downloadAndRename(dict3):  # 传入的参数数据类型dict，需要的key包括”文件名”和“下载地址”
        r = requests.get("http://172.31.120.5:8080/TangcheRule/" + dict3["下载地址"], headers=headers)
        with open(dict3["文件名"] + "." + dict3["下载地址"].split(".")[-1], "wb") as f:
            f.write(r.content)

    data = {"id": dict2["id"], "parentId": dict2["parentId"], "ponsr": "1"}  # post请求的参数，由传入的参数获得

    r = requests.post(StrGetnodeinfo, data=data)  # 发送post请求，获得json数据
    if r.status_code == 200:
        s = r.json()  # 将反馈的json数据“字典化”，s的数据类型为dict
        # if "text" in s.keys():
        if "/" in dict2["text"]:  # 保存文件之前，需先确认文件名中不包含"/"字符，“/”字符无法作为文件名使用
            dict2["text"] = dict2["text"].replace("/","_")
            # 将通过post请求所获得的返回值中“text”字符串中的“/"替换成文件名允许的字符”_",并用替换后的新字符串，更改dict2中“text”的值
        if s["filename"] != 'null':  # 确认下载地址不为空，下载地址为空说明没有文件需要下载
            # filename = {"文件名": i["text"], "下载地址": s["filename"]}
            DownloadAddress_dict = {"文件名": dict2["text"], "下载地址": s["filename"]}  # 定义一个dict类型变量，key值分别是“文件名”和“下载地址”
            # filename_list.append(filename)
            downloadAndRename(DownloadAddress_dict)  # 调用downloadAndRename函数下载保存并重命名文件
    # return DownloadAddress_dict


# 遍历5层节点,获得每一个节点的id，parentId和text，每个节点信息以dict的type存储到列表node_total中去
for i in systemid_list:  # 在公司章程、公司行政文件、单位及制度文件这一层循环，通过变量i饮用i["systemid"]确保循环体内的systemid保持不变
    for k0 in getNodeID(i, i):  # 遍历systemid之下一层的node节点
        if k0 is not None: # is运算符比==效率高，在变量和None进行比较时，应该使用is；is比较引用的地址，==比较引用的值
            DownloadRuls(k0)
            node_level1_list.append({"id": k0["id"], "parentId": k0["parentId"],
                                     "text": k0["text"]})  # 构建此层的节点列表，用于发送请求获取下一层节点的id，parentId和text
    for k1 in node_level1_list:
        for j1 in getNodeID(i, k1):
            if j1 is not None:
                DownloadRuls(j1)
                node_level2_list.append({"id": j1["id"], "parentId": j1["parentId"], "text": j1["text"]})
    for k2 in node_level2_list:
        for j2 in getNodeID(i, k2):
            if j2 is not None:
                DownloadRuls(j2)
                node_level3_list.append({"id": j2["id"], "parentId": j2["parentId"], "text": j2["text"]})
    for k3 in node_level3_list:
        for j3 in getNodeID(i, k3):
            if j3 is not None:
                DownloadRuls(j3)
                node_level4_list.append({"id": j3["id"], "parentId": j3["parentId"], "text": j3["text"]})
    for k4 in node_level4_list:
        for j4 in getNodeID(i, k4):
            if j4 is not None:
                DownloadRuls(j4)
