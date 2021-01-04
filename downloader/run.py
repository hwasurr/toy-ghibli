from PIL import Image
from bs4 import BeautifulSoup
import requests
import os


class Downloader:

    baseUrl = 'https://www.ghibli.jp'
    listUrl = '/info/013409/'

    def download(self):
        self.__getList()
        self.__getPictureList()
        self.__downloadPicture()

    def parseSoup(self, html, selector):
        bs = BeautifulSoup(html, 'html.parser')
        return bs.select(selector)

    def __getList(self):
        res = requests.get(self.baseUrl + self.listUrl)

        if res.status_code == 200:
            tags = self.parseSoup(res.text, "div > a.panelarea")

            workList = []
            for tag in tags:
                worktitle = tag['href'].split(
                    'works/')[1].replace('/#frame', '')
                work = {
                    "href": tag['href'],
                    "title": worktitle,
                }
                if work not in workList:
                    workList.append(work)

            self.workList = workList

        else:
            print(res.status_code)

    def __getPictureList(self):
        pictureList = []
        for work in self.workList:
            res = requests.get(work['href'])

            if res.status_code == 200:
                tags = self.parseSoup(res.text, "figure > a.panelarea")
                for tag in tags:
                    picture = {
                        "href": tag["href"],
                        "worktitle": work['title'],
                        "title": tag["title"],
                    }
                    if picture not in pictureList:
                        pictureList.append(picture)

        self.pictureList = pictureList

    def __downloadPicture(self):
        for picture in self.pictureList:
            # 디렉토리 생성
            if picture['worktitle'] not in (
                os.listdir(os.path.join(os.getcwd(), 'images'))
            ):
                os.mkdir(
                    os.path.join(os.getcwd(), 'images', picture['worktitle']))

            img = Image.open(requests.get(picture['href'], stream=True).raw)

            try:
                img.save(
                    './images' + "/" + picture['worktitle'] +
                    '/' + picture['title'] + '.jpg'
                )
                print('image download complete - ' + picture['title'])
            except FileExistsError:
                pass

    def makeImagesFolder(self):
        if 'images' not in os.listdir(os.getcwd()):
            os.mkdir('images')


if __name__ == '__main__':
    downloader = Downloader()
    downloader.makeImagesFolder()
    downloader.download()
