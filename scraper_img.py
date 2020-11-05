import requests, re, shutil, sqlite3
from bs4 import BeautifulSoup
from slugify import slugify
from util import remove_bad_words

def save_image_database(name, data):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute('''INSERT INTO file_contents (name, data) VALUES (?, ?)''', (name, data))
    # sql = '''INSERT INTO file_contents (name, data) VALUES (?, ?)'''
    # cursor.execute(sql, (name, data))
    con.commit()
    cursor.close()

def get_body_site(url, uri):
    return requests.get('{}{}'.format(url, uri)).text

def get_images_site(url, uri):
    html = requests.get('{}{}'.format(url, uri)).text
    bs = BeautifulSoup(html, 'lxml')
    images = bs.find_all('img', {'src':re.compile('.jpg')})
    images_list = []
    
    for image in images: 
        images_list.append(image['src'].split('//')[1])

    return images_list

def save_images(href, name):
    image_url = 'https://{}'.format(href)
    r = requests.get(image_url, stream = True)

    if r.status_code == 200:
        r.raw.decode_content = True
        
        filename = slugify(name)
        save_image_database(filename, r.content)

        # save image locally

        # filename = '{}.jpg'.format(slugify(name))
        # with open('faces/{}'.format(filename),'wb') as f:
        #     shutil.copyfileobj(r.raw, f)
            
        print('Image sucessfully Downloaded: ', filename)
    else:
        print('Image Couldn\'t be retreived')

def get_href_names(text):
    soup = BeautifulSoup(text, 'lxml')
    table = soup.find_all('div', {'class': 'div-col columns column-width'})

    href_list = []
    for i in table:
        names = i.find_all('a')
        for j in names:
            try:
                if '(page does not exist)' not in j['title'] and 'Edit' not in j['title']:
                    href_list.append(
                        {
                            "name": remove_bad_words(j['title']),
                            "href": j['href']
                        }
                    )
            except:
                pass

    return href_list


url = 'https://en.wikipedia.org'
uri = '/wiki/List_of_Brazilian_actors'

wikipedia_names_list = get_body_site(url, uri)
links_list = get_href_names(wikipedia_names_list)

# for i in links_list:
#     print('name: {} | href: {}'.format(i['name'], i['href']))

urls = []
for i in links_list:
    urls = get_images_site(url, i['href'])

    if urls: # if list is empty
        save_images(urls[0], i['name'])
