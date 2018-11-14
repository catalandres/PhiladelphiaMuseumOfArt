
from pathlib import Path
import bs4
import pandas
import os

WORK_URL = 'http://www.philamuseum.org/collections/permanent/{0}.html'

WORK_FOLDER = './works'
OUTPUT_FOLDER = './results'

WORKS_PER_CHUNK = 10000

GEOGRAPHY = 'Geography:'
DATE = 'Date:'
MEDIUM = 'Medium:'
DIMENSIONS = 'Dimensions:'
COPYRIGHT = 'Copyright:'
DEPARTMENT = 'Curatorial Department:'
LOCATION1 = 'Object Location:'
LOCATION2 = '* '
ACCESSION = 'Accession Number:'
CREDIT = 'Credit Line:'

def string_between(string, start, end):
    return string.split(start)[1].split(end)[0].strip()

def parse_work_file(work_file):
    text = work_file.read_text()
    soup = bs4.BeautifulSoup(text, 'lxml').find('div', id='recordData')
    art = {}
    art['id'] = work_file.name.split('-')[1].split('.')[0]
    art['url'] = WORK_URL.format(art['id'])
    art['title'] = soup.find('strong').text
    art['subtitle'] = soup('p')[0].text.split(art['title'])[1]
    art['author'] = soup('p')[1].text
    if GEOGRAPHY in soup.text:
        art['geography'] = string_between(soup.text, GEOGRAPHY, DATE)
    if DATE in soup.text:
        art['date'] = string_between(soup.text, DATE, MEDIUM)
    if MEDIUM in soup.text:
        art['medium'] = string_between(soup.text, MEDIUM, DIMENSIONS)
    if DIMENSIONS in soup.text:
        if COPYRIGHT in soup.text:
            art['dimensions'] = string_between(soup.text, DIMENSIONS, COPYRIGHT)
        else:
            art['dimensions'] = string_between(soup.text, DIMENSIONS, DEPARTMENT)
    if COPYRIGHT in soup.text:
        art['copyright'] = string_between(soup.text, COPYRIGHT, DEPARTMENT)
    if DEPARTMENT in soup.text:            
        if LOCATION1 in soup.text:
            art['curatorial_department'] = string_between(soup.text, DEPARTMENT, LOCATION1)
        elif LOCATION2 in soup.text:
            art['curatorial_department'] = string_between(soup.text, DEPARTMENT, LOCATION2)
        else:
            art['curatorial_department'] = soup.text.split(DEPARTMENT)[1].split(ACCESSION)[0].strip()
    if LOCATION1 in soup.text:
        art['location'] = string_between(soup.text, LOCATION1, ACCESSION)
    elif LOCATION2 in soup.text:
        art['location'] = string_between(soup.text, LOCATION2, ACCESSION)
    if ACCESSION in soup.text:
        art['accession_number'] = soup.text.split(ACCESSION)[1].split(CREDIT)[0].strip()
    if CREDIT in soup.text:
        art['credit_line'] = soup.text.split(CREDIT)[1].strip()
    return art


def main():
    if not Path(OUTPUT_FOLDER).exists():
        os.mkdir(OUTPUT_FOLDER)

    works_files = list(Path(WORK_FOLDER).glob('*'))
    works_count = len(list(Path(WORK_FOLDER).glob('*')))
    chunks_count = works_count // WORKS_PER_CHUNK + 1

    works_chunks = []

    for chunk_number in range(chunks_count):
        works_chunks.append(works_files[(WORKS_PER_CHUNK*chunk_number): min(WORKS_PER_CHUNK*(chunk_number+1), works_count)])

    for chunk in works_chunks:
        chunk_number = works_chunks.index(chunk) + 1
        chunk_file_name = OUTPUT_FOLDER + '/PhiladelphiaMuseumOfArt-{0}-of-{1}.csv'.format(chunk_number, chunks_count)
        if Path(chunk_file_name).exists():
            pass
        else:
            print('Working on chunk {0} of {1}'.format(chunk_number, chunks_count))
            works = []
            for work_file in chunk:
                works.append(parse_work_file(work_file))
            pandas.DataFrame.from_records(works).to_csv(chunk_file_name)


if __name__ == "__main__":
    main()
