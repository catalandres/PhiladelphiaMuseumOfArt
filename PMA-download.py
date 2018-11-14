
from queue import PriorityQueue
from pathlib import Path
import requests
import string
import threading
import bs4
import re
import os

NUM_WORKERS = 10
SEARCH_URL = 'http://www.philamuseum.org/collections/getArtistMaker.php?letter={0}'
ARTIST_URL = 'http://www.philamuseum.org/collections/results.html?results=54&searchNameID={0}&searchClassID=&provenance=0&audio=0&onView=0&searchOrigin=&searchDeptID=&page={1}&action=post'
WORK_URL = 'http://www.philamuseum.org/collections/permanent/{0}.html'

ARTIST_FOLDER = './artists'
WORK_FOLDER = './works'

class ArtWorker(threading.Thread):

    def __init__(self, queue, art, id):
        """Initialize instance by internalizing reference to queue."""
        threading.Thread.__init__(self)
        self.queue = queue
        self.art = art
        self.id = id

    def run(self):
        """Override run method to add process logic."""
        print("[{}]  Ready to work.".format(self.id))
        while True:
            (priority, content) = self.queue.get()
            if priority == 0:
                print("[{}]({})  🖼️ {}".format(
                    self.id, self.queue.qsize(), content))
                store_work_page(content)
            elif priority > 0:
                print("[{}]({})  🎨 {}".format(
                    self.id, self.queue.qsize(), content))
                parse_artist_page(content, self.queue)
            self.queue.task_done()


def parse_letter_page(letter):
    body = requests.get(SEARCH_URL. format(letter)).text
    return [x.split('"')[0] for x in body.split('<option value="')[2:]]


def parse_artist_page(artist_number, queue):
    artist_file = Path(ARTIST_FOLDER + '/artist-' + artist_number + '-1' + '.txt')
    if artist_file.is_file():
        text = artist_file.read_text()
    else:
        text = requests.get(ARTIST_URL. format(artist_number, 1)).text
        artist_file.write_text(text)
    matches = int(text.split('Results : <b>')[1].split('</b>')[0])
    pages = matches // 54 + 1
    for page in range(pages):
        artist_file = Path(ARTIST_FOLDER + '/artist-' + artist_number + '-' + str(page+1) + '.txt')
        if artist_file.is_file():
            text = artist_file.read_text()
        else:
            text = requests.get(ARTIST_URL. format(artist_number, page+1)).text
            artist_file.write_text(text)
        soup = bs4.BeautifulSoup(text, 'lxml')
        works = set(
            [x['href'].split('/')[3].split('.')[0]
            for x
            in soup.find_all('a', href=re.compile('/collections/permanent/'))]
        )
        for work_number in works:
            queue.put((0, work_number))


def store_work_page(work_number):
    work_file = Path(WORK_FOLDER + '/work-' + work_number + '.txt')
    if work_file.is_file():
        pass
    else:
        text = str(bs4.BeautifulSoup(requests.get(WORK_URL. format(work_number)).text, 'lxml').find('div', id='recordData'))
        work_file.write_text(text)


def main():
    if not Path(ARTIST_FOLDER).exists():
        os.mkdir(ARTIST_FOLDER)
    if not Path(WORK_FOLDER).exists():
        os.mkdir(WORK_FOLDER)
    queue = PriorityQueue()
    art = []
    for id in range(NUM_WORKERS):
        worker = ArtWorker(queue, art, id)
        worker.daemon = True
        worker.start()
    artist_numbers = []
    for letter in string.ascii_uppercase:
        artist_numbers = parse_letter_page(letter)
        print("[-]  Processed {}: {} artists".format(letter, len(artist_numbers)))
        for artist_number in artist_numbers:
            queue.put((100, artist_number))
    queue.join()


if __name__ == "__main__":
    main()
