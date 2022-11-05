"""
 Developed by: KenDzz
 Name: VO VAN QUA (KenDzz)
 Class: 19IT4
 ID: 19IT266
 GITHUB: https://github.com/kendzz
 FB: https://www.facebook.com/Rin.Boss.Rin/
 Date: 23:19, Thứ Năm, 15 tháng 9, 2022 (GMT+7)
"""

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json
import re



url = "https://vietnamnet.vn/thoi-su-page1"
html = urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")
num = 1
trang = 1
numNewss = 1


def getCommentNews(getAttrNews,numNews,url):
    urlJsonCommentNews = Request(
        url='https://comment.vietnamnet.vn/api/Comment/Gets?SortType=2&objectId=' + getAttrNews.attrs[
            'data-objectid'] + '&pageIndex=0&websiteId=' + getAttrNews.attrs['data-websiteid'],
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    print("Đang cào bình luận trang : " + str(url))
    htmlJsonCommentNews = urlopen(urlJsonCommentNews).read()
    data_json = json.loads(htmlJsonCommentNews)
    # print(data_json["data"])
    totalComment = data_json["data"]["totalComment"]
    pageSizeComment = data_json["data"]["pageSize"]
    pageIndexComment = data_json["data"]["pageIndex"]
    file = open("Tittle/" + str(numNews) + ".txt", "a", encoding="utf-8")
    file.write("\n Tổng bình luận của trang này là:" + str(totalComment))
    if totalComment > 0:
        for x in range(pageSizeComment):
            urlJsonCommentNewsPage = Request(
                url='https://comment.vietnamnet.vn/api/Comment/Gets?SortType=2&objectId=' + getAttrNews.attrs[
                    'data-objectid'] + '&pageIndex='+str(x)+'&websiteId=' + getAttrNews.attrs['data-websiteid'],
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            htmlJsonCommentNewsPage = urlopen(urlJsonCommentNewsPage).read()
            data_json_Page = json.loads(htmlJsonCommentNewsPage)
            dataComment = data_json_Page["data"]["comments"]
            if dataComment:
                if len(dataComment) > 1:
                    for data in dataComment:
                        # print(data['userId'])
                        file.write("\n User Id:" + str(data['userId']) + "| Tài khoản:"+ str(data['userName']) + "| Lượt thích bình luận: "+ str(data['totalLike']) +"| Bình luận:" + str(data['commentContent']) +"| Thời gian bình luận: "+ str(data['createdDate']))
                else:
                    file.write("\n User Id:" + str(dataComment[0]['userId']) + "| Tài khoản:" + str(dataComment[0]['userName']) + "| Lượt thích bình luận: " + str(dataComment[0]['totalLike']) + "| Bình luận:" + str(dataComment[0]['commentContent']) + "| Thời gian bình luận: " + str(dataComment[0]['createdDate']))
    file.close()


def Find(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]

def checkUrl(url):
    if Find(url):
        status_code = urlopen(url).getcode()
        website_is_up = status_code == 200
    else:
        website_is_up = False
    return website_is_up

def getContentNews(h3, numNewss):
    for matchDiv in h3:
        if checkUrl(matchDiv.find("a").get("href")):
            h3Url = matchDiv.find("a").get("href")
        else:
            h3Url = "https://vietnamnet.vn" + matchDiv.find("a").get("href")
        print("Đang cào dữ liệu nội dung chi tiết trang : " + str(h3Url))
        htmlNews = urlopen(h3Url).read()
        soupNews = BeautifulSoup(htmlNews, "html.parser")
        getAttrNews = soupNews.find("div", {"class": "comment__iframe"})
        resultNews = soupNews.find("div", {"class": "maincontent"})
        file = open("Tittle/" + str(numNewss) + ".txt", "a", encoding="utf-8")
        file.write("\n Nội dung:" + resultNews.text)
        file.close()
        getCommentNews(getAttrNews,numNewss,h3Url)
        print(numNewss)
        numNewss += 1
    print(numNewss)
    return numNewss


while trang != 41:
    url = "https://vietnamnet.vn/thoi-su-page" + str(trang)
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    h3 = soup.find_all("h3", {"class": "feature-box__content--title vnn-title"})
    hrefNews = soup.find_all("a", {"class": "feature-box__content--title vnn-title"})
    d = soup.find_all("div", {"class": "feature-box__content--desc"})
    trang += 1
    for content in h3:
        file = open("Tittle/" + str(num) + ".txt", "w", encoding="utf-8")
        file.write("Tiêu đề:" + content.text)
        print("Đang cào dữ liệu tiêu đề , nội dung tóm tắt trang: https://vietnamnet.vn/thoi-su-page"+ str(trang))
        file.close()
        num += 1
    numGetContent = getContentNews(h3,numNewss)
    numNewss = numGetContent