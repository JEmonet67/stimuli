import sys, os
import cv2
from os.path import isfile, join
import numpy as np


def video_to_images(path_video, save=False):
    cam = cv2.VideoCapture(path_video)
    list_frame = []

    if save:
        current_frame = 0
        try:
            if not os.path.exists("data"):
                os.makedirs("data")
        except:
            Print("Error in creating data directory.")

    
    has_frames,frame = cam.read()
    
    while has_frames:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if save:
            name = "frame" + str(current_frame)
            #print("Creating..." + name)
            cv2.imwrite("./data/"+name+".jpg",frame)
            current_frame += 1
        
        else:
            list_frame += [frame]
        
        has_frames,frame = cam.read()
        
    
    cam.release()
    cv2.destroyAllWindows()

    return list_frame



def image_to_video():
    print()




def images_to_video(nameVideo,input):
    path_out = "/user/jemonet/home/Documents/Thèse/Stimuli/" + nameVideo
    fps = 60
    list_frame = []
    ext = nameVideo[len(nameVideo)-3:]

    if isinstance(input,str):
        #path_in = "."
        files = [f for f in os.listdir(input) if isfile(join(input,f))]
        files.sort(key = lambda x: int(x[5:-4]))

        for current_frame in range(len(files)):
            filename = input + "/" + files[current_frame]
            img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            list_frame.append(img)

    if isinstance(input,list):
        for current_frame in range(len(input)):
            if isinstance(input[current_frame],np.ndarray):
                list_frame.append(input[current_frame])
            else:
                print("BEWARE, Element", current_frame, "isn't add because not a numpy.ndarray.")

                
    height, width = list_frame[0].shape
    size = (width,height)
    if ext=="mp4":
        out = cv2.VideoWriter(path_out, cv2.VideoWriter_fourcc(*'mp4v'), fps, size, 0)
        for current_frame in range(len(list_frame)):
            out.write(list_frame[current_frame])
        out.release()


    elif ext=="avi":
        out = cv2.VideoWriter(path_out, cv2.VideoWriter_fourcc(*'DIVX'), fps, size, 0)
        for current_frame in range(len(list_frame)):
            out.write(list_frame[current_frame])
        out.release()

    else:
        print("Format not found")



def clean_video():
    print() # Fonction pour nettoyer les pixels qui ne sont pas à 0 ou 255. Il faudra retester
            # une nouvelle cam cv2 pour voir si c'est elle qui crée ces artefacts ou si ça vient de la vidéo d'origine.


def white_begin():
    print()



def invert_black_white(list_frame):
    current_frame = 0
    for frame in list_frame:
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                if frame[i][j]<127:
                    frame[i][j] = 255
                else:
                    frame[i][j] = 0
        cv2.imwrite("/user/jemonet/home/Documents/Thèse/Stimuli/WhiteBar_Whitefont/frame"+str(current_frame)+".jpg",frame)
        current_frame+=1

    return list_frame
    

def create_flash_stimulus(length):
    for i in range(length):
        
