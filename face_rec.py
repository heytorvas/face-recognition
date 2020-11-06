import os, cv2, face_recognition, sqlite3, shutil
import numpy as np
import face_recognition as fr
from util import reverse_slug
import threading

class Thread:
    def __init__(self, images_list):
        self.encoded = {}
        self.images_list = images_list

    def encode_face(self, f):
        try:
            face = fr.load_image_file("faces/" + f)
            encoding = fr.face_encodings(face)[0]
            self.encoded[f.split(".")[0]] = encoding

        except Exception as e:
            print(e)

    def manageThread(self):
        counter = 0

        while counter < len(self.images_list):
            if threading.active_count() <= 100:
                t = threading.Thread(target=self.encode_face, args=(self.images_list[counter],))
                t.start()
                counter = counter + 1

def writeTofile(data, filename):
    filename = '{}.jpg'.format(filename)
    with open('faces/{}'.format(filename),'wb') as file:
        file.write(data)

def get_encoded_faces_database():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute('''SELECT * from file_contents''')
    record = cursor.fetchall()
    for row in record:
        print("Id= ", row[0], "Name= ", row[1])
        writeTofile(row[2], row[1])

    cursor.close()

def get_encoded_faces():
    os.mkdir('faces')
    get_encoded_faces_database()

    lista_imagens = []

    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                lista_imagens.append(f)


    thread = Thread(lista_imagens)
    thread.manageThread()
    encoded = thread.encoded
    
    shutil.rmtree('{}/faces'.format(os.getcwd()))
    return encoded


def unknown_image_encoded(img):
    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]

    return encoding


def classify_face(im):
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = cv2.imread(im, 1)
    #img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    #img = img[:,:,::-1]
 
    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "unknown"

        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(reverse_slug(name))

        # for (top, right, bottom, left), name in zip(face_locations, face_names):
        #     # Draw a box around the face
        #     cv2.rectangle(img, (left-20, top-20), (right+20, bottom+20), (255, 0, 0), 2)

        #     # Draw a label with a name below the face
        #     cv2.rectangle(img, (left-20, bottom -15), (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
        #     font = cv2.FONT_HERSHEY_DUPLEX
        #     cv2.putText(img, name, (left -20, bottom + 15), font, 1.0, (255, 255, 255), 2)


    # # Display the resulting image
    # while True:

    #     cv2.imshow('Video', img)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         return face_names 
    return face_names
