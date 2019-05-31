import requests
from bs4 import BeautifulSoup as bs
import json
import re
from tqdm import tqdm,trange


abs=[]
with open('../../abbreviationExpansion.txt',encoding='utf8') as f:
    for line in f:
        if line.split('\t')[0].strip():
            abs.append(line.split('\t')[0].strip())
print(abs)


headers = {
   'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
   'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3',
   'Cache-Control': 'max-age=0',
   'Cookie': 'ipv6=hit=1559103046767&t=4; _SS=SID=2F80B1B05B9F60CE31CABCDA5AE5615D&CPID=1559099457580&AC=1&CPH=542537ff&HV=1559099467; _EDGE_S=mkt=zh-cn&SID=2F80B1B05B9F60CE31CABCDA5AE5615D; SRCHUID=V=2&GUID=7BE0A9EA6C0D4E6EA18009E8604D1995&dmnchg=1; BFB=ARAm13voaJ6nhlYYgWHfGoUeZ3zlEad_VwZcpQ2LbStfqJ9sQZZOMuJC1ue0RmObKx3hGk6a_F4GHNB7TvnaRCkKO1hvSij_egTRnQl5a65dyP4j-W0msiP-ldTkFifjB9c; BFBD=yQokNzYxODQ2ZGQtZGQwYS00YWU3LWFjNDEtOTBkNjk1MTE2ODMzyxQNARAKAgjQMgDLRhABBgAAywoRAezMkZGvqdTUA8soEAEG0DIAyzwRAaqO4LOVpdTUAwAA; SRCHD=AF=NOFORM; _EDGE_V=1; MUID=195309CF6A3E696701CF052F6B4468BF; SRCHUSR=DOB=20190110; SRCHHPGUSR=LUT=1552277397313&CW=1904&CH=1046&DPR=1&UTC=480&WTS=63694696245&IPMH=350ee158&IPMID=1559099440783; _RwBf=s=70&o=18; CSRFCookie=80e160aa-d434-413d-9bd0-b8c27acca503; MicrosoftApplicationsTelemetryFirstLaunchTime=1547090515138; MicrosoftApplicationsTelemetryDeviceId=57f602bf-00c4-74cc-b8cf-b84c211e1b8a; MUIDB=195309CF6A3E696701CF052F6B4468BF',
   'Host': 'www.bing.com',
   'Referer': 'https://www.bing.com/dict/search?q=welcome&FORM=BDVSP6&mkt=zh-cn',
   'Upgrade-Insecure-Requests': '1',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
}

rlist=[]
for a in abs:
    print(a)
    now_list=[]
    url=f'https://cn.bing.com/dict/service?q={a}&dtype=sen'
    try:
        response=requests.get(url,headers=headers)
    except Exception as e:
        print(e)
        continue
    soup=bs(response.text,'lxml')
    if not soup.find('div',class_='se_li'):
        continue
    for div in soup.find_all('div',class_='se_li'):
        js={}
        js['abbr']=a
        js['en']=div.find('div',class_='sen_en').text.strip() if div.find('div',class_='sen_en') else ''
        js['cn']=div.find('div',class_='sen_cn').text.strip() if div.find('div',class_='sen_cn') else ''
        js['source']=div.find('div',class_='sen_li').text.strip() if div.find('div',class_='sen_li') else ''
        js['sound']=re.search('https:\S*mp3',div.find('div',class_='mm_div').a['onmousedown']).group()
        rlist.append(js)
        if len(rlist)<5:
            print(js)
    for i in range(10,10000,10):
        url = f'https://cn.bing.com/dict/service?q={a}&offset={i}&dtype=sen'
        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            print(e)
            continue
        soup = bs(response.text, 'lxml')
        if not soup.find('div', class_='se_li'):
            print(i)
            break
        for div in soup.find_all('div', class_='se_li'):
            js = {}
            js['abbr'] = a
            js['en'] = div.find('div', class_='sen_en').text.strip() if div.find('div', class_='sen_en') else ''
            js['cn'] = div.find('div', class_='sen_cn').text.strip() if div.find('div', class_='sen_cn') else ''
            js['source'] = div.find('div', class_='sen_li').text.strip() if div.find('div', class_='sen_li') else ''
            js['sound'] = re.search('https:\S*mp3', div.find('div', class_='mm_div').a['onmousedown']).group()
            rlist.append(js)
            now_list.append(js)
    with open('../../bing_examples_tmp.json', 'a', encoding='utf8') as f:
        f.write(json.dumps({a:now_list}, indent=0, ensure_ascii=False))
with open('../../bing_examples.json','w',encoding='utf8') as f:
    f.write(json.dumps(rlist,indent=0, ensure_ascii=False))


