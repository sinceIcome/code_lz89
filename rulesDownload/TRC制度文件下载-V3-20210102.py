# coding=gbk
'''
��Ҫ����
ʹ��Firefox�������������������Ŀ������߽��з�������ݼ�F12���뿪��ģʽ��
���뿪�����ߺ������磨network��һ���У����Կ���������ͷ�����֮��Ļ���������XHR�����������������
����������Ŀ�����Ի����Ӧ��������Ϣ����������ͷ��������cookies����Ӧ�ȵ�
'''
'''
��Ҫ˼·
���������0.����������͵�����
��ҳ�ϵ�"+"��Ӧ����һ��gettree.action000000000000000000000000000000000000000
����������Ŀ����Ӧ����һ��getnodeinfo.action
ͨ��gettree.action���Ի��ÿ���ڵ��id��parentID������һ����id���Լ�text������ʾ�����ƣ�
ͨ��id��parentID�Ϳ��Ի��filename�����ļ��ڷ������ϵ����ƣ������Խ�һ��ȡ���ļ���url
'''
'''
�����ʵ��
1.������������requests��
2.�Է��������ص�json���ݽ��д�������json��
3.ͨ��id��parentId��text�Ϳ��Ի������url��Ȼ�����أ�����Щд��һ�������def DownloadRuls(dict2)
4.��Ҫ�������еĽڵ�node��ֱ��Ƕ��ѭ���Ƚ����ѣ���˲���һ��һ�㴦��ķ�ʽ��������ÿһ���list��ŵ�ǰ��Ľڵ���Ϣ������һ�����ʱ���ã�����϶࣬��˼·��
5.ע����������������ͣ���Ϣ��Ҫ�洢��list��dict��'''
import requests
import json

# �������
StrGettree = "http://172.31.120.5:8080/TangcheRule/gettree.action?"
# ���ڷ���get�����url���������Ϊsystemid��id�����Ի����һ��ڵ��id��parentId��text
StrGetnodeinfo = "http://172.31.120.5:8080/TangcheRule/getnodeinfo.action"
# ���ڷ���post�����url�����������id��parentId��posnr����Ϊ"1"�������Ի�ýڵ����Ϣ��Ŀǰ��Ҫ���ڻ�ȡ�ļ��Ĵ洢λ��"filename"���������������Ļ��������Դ�"detaildata"��ȡ����ر���������Ϣ

# ����ͷheaders
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

'''' # ��ȡ��������Լ���Ӧ��systemid
SortList_raw = requests.get("http://172.31.120.5:8080/TangcheRule/getclass.action").json()["root"]

# ʹ��requests����get��������õ�response��json����
# ͨ��.json()�����������ص�json����ת��Ϊdict����
# ͨ��dict��key ��root������ȡnode�ڵ���Ϣ����Ч��Ϣ����"id"��"systemid"��"text��,Ҳ����������Ϣ�������һ��Ҫ�����õ���Ϣ��ȡ����
sort_list = []  # ����һ���б��б�Ԫ�ص���������Ϊdict�����ڴ洢sort�����id��systemid��text��Ϣ
sortInput_list = []  # ����һ���б��б�Ԫ����������Ϊstr�����ڴ洢�������������Ҫ��systemid&id������Ϣ,Ŀǰδʹ��
for i in SortList_raw:
    sort_list.append({"id": i["id"], "systemid": i["systemid"], "text": i["text"]})
    sortInput_list.append("systemid=" + str(i["systemid"]) + "&id=" + str(i["id"]))
#print(sort_list)
#print(sortInput_list)'''

# sort_list���������ﶨ��⡢��ɫ����ָ�ϵ�������п��������⣬�������¶�����һ���б����systemid_list��ֻ�洢������Ϣ
systemid_list = [{'id': 5343, 'systemid': 'ZC', 'text': '��˾�³�'},
                 {'id': 2969, 'systemid': 'NZ', 'text': '��˾�������ƶ��ļ�'},
                 {'id': 5539, 'systemid': 'DJ', 'text': '��˾�������ƶ��ļ�'},
                 {'id': 3712, 'systemid': 'DW', 'text': '��λ���ƶ��ļ�'},
                 {'id': 974, 'systemid': 'WW', 'text': '��˾�ⲿ�ļ�'}
                 ]

# �½��б����ڴ洢����ÿһ�㼶��node�ڵ���Ϣ
node_level1_list = []
node_level2_list = []
node_level3_list = []
node_level4_list = []


# ���庯��������get����ȡ��node����Ϣ
def getNodeID(dict1, dict2):
    '''�ȷ���get������response��Ȼ���ֵ仯����ȡ��Ϣ
    dict1��Ҫ��Ϊ�˱�֤����ѭ�����ڵ�systemid���䣬
    ѭ����ͨ��dict2����
    dict1���������б�systemid_list��ã�dict1��key������id������systemid���͡�text��
    dict2��dict�������ݣ��ǽڵ�node��Ϣ���ڴ˺�������Ҫ���õ�key�ǡ�id��'''
    list1 = requests.get(StrGettree + "systemid=" + str(dict1["systemid"]) + "&id=" + str(dict2["id"])).json()[
        "root"]  # ����get����ͨ��������systemid���͡�id��һ������ȡ����һ��ڵ��id��parentId��text
    return list1  # ����һ���б��б��Ԫ����dict�������ݣ�keyΪ"id"��"parentId"��"text"

# ���庯����ͨ����֪��"id"��"parentId"��"text"�ڵ���Ϣ����ȡ�ļ�url�������ر����ļ�����������
def DownloadRuls(dict2):  # ����Ĳ�����������Ϊdict����Ҫ��key������id������parentId���͡�text��

    # ����һ�������������ļ��������ļ�������
    def downloadAndRename(dict3):  # ����Ĳ�����������dict����Ҫ��key�������ļ������͡����ص�ַ��
        r = requests.get("http://172.31.120.5:8080/TangcheRule/" + dict3["���ص�ַ"], headers=headers)
        with open(dict3["�ļ���"] + "." + dict3["���ص�ַ"].split(".")[-1], "wb") as f:
            f.write(r.content)

    data = {"id": dict2["id"], "parentId": dict2["parentId"], "ponsr": "1"}  # post����Ĳ������ɴ���Ĳ������

    r = requests.post(StrGetnodeinfo, data=data)  # ����post���󣬻��json����
    if r.status_code == 200:
        s = r.json()  # ��������json���ݡ��ֵ仯����s����������Ϊdict
        # if "text" in s.keys():
        if "/" in dict2["text"]:  # �����ļ�֮ǰ������ȷ���ļ����в�����"/"�ַ�����/���ַ��޷���Ϊ�ļ���ʹ��
            dict2["text"] = dict2["text"].replace("/","_")
            # ��ͨ��post��������õķ���ֵ�С�text���ַ����еġ�/"�滻���ļ���������ַ���_",�����滻������ַ���������dict2�С�text����ֵ
        if s["filename"] != 'null':  # ȷ�����ص�ַ��Ϊ�գ����ص�ַΪ��˵��û���ļ���Ҫ����
            # filename = {"�ļ���": i["text"], "���ص�ַ": s["filename"]}
            DownloadAddress_dict = {"�ļ���": dict2["text"], "���ص�ַ": s["filename"]}  # ����һ��dict���ͱ�����keyֵ�ֱ��ǡ��ļ������͡����ص�ַ��
            # filename_list.append(filename)
            downloadAndRename(DownloadAddress_dict)  # ����downloadAndRename�������ر��沢�������ļ�
    # return DownloadAddress_dict


# ����5��ڵ�,���ÿһ���ڵ��id��parentId��text��ÿ���ڵ���Ϣ��dict��type�洢���б�node_total��ȥ
for i in systemid_list:  # �ڹ�˾�³̡���˾�����ļ�����λ���ƶ��ļ���һ��ѭ����ͨ������i����i["systemid"]ȷ��ѭ�����ڵ�systemid���ֲ���
    for k0 in getNodeID(i, i):  # ����systemid֮��һ���node�ڵ�
        if k0 is not None: # is�������==Ч�ʸߣ��ڱ�����None���бȽ�ʱ��Ӧ��ʹ��is��is�Ƚ����õĵ�ַ��==�Ƚ����õ�ֵ
            DownloadRuls(k0)
            node_level1_list.append({"id": k0["id"], "parentId": k0["parentId"],
                                     "text": k0["text"]})  # �����˲�Ľڵ��б����ڷ��������ȡ��һ��ڵ��id��parentId��text
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
