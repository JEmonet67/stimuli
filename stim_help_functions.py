import sys, os
import cv2
from os.path import isfile, join
import numpy as np
import math


def video_to_images(path_video, save=False):
    cam = cv2.VideoCapture(path_video)
    list_frame = []

    if save:
        current_frame = 0
        try:
            if not os.path.exists("data"):
                os.makedirs("data")
        except:
            print("Error in creating data directory.")

    
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



# def image_to_video():
#     print()




def images_to_video(nameVideo,input, c = True, path_video=None):
    if path_video != None:
        path_out = path_video + nameVideo
    else:
        path_out = "/user/jemonet/home/Documents/These/stimuli/" + nameVideo
    fps = 60
    list_frame = []
    ext = nameVideo[len(nameVideo)-3:]

    if isinstance(input,str):
        #path_in = "."
        files = [f for f in os.listdir(input) if isfile(join(input,f))]
        files.sort(key = lambda x: int(x[1:-4]))

        for current_frame in range(len(files)):
            filename = input + "/" + files[current_frame]
            if c:
                img = cv2.imread(filename)
            else:
                img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

            list_frame.append(img)

    if isinstance(input,list):
        for current_frame in range(len(input)):
            if isinstance(input[current_frame],np.ndarray):
                list_frame.append(input[current_frame])
            else:
                print("BEWARE, Element", current_frame, "isn't add because not a numpy.ndarray.")

    if len(list_frame[0].shape)==3:
        height, width, color = list_frame[0].shape
    else:
        height, width = list_frame[0].shape
    size = (width,height)
    print(size)
    if ext=="mp4":
        if c:
            out = cv2.VideoWriter(path_out, cv2.VideoWriter_fourcc(*'mp4v'), fps, size, 1)
        else:
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



# def clean_video():
#     print() # Fonction pour nettoyer les pixels qui ne sont pas à 0 ou 255. Il faudra retester
            # une nouvelle cam cv2 pour voir si c'est elle qui crée ces artefacts ou si ça vient de la vidéo d'origine.


# def white_begin():
#     print()



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
    

def create_flash_stimulus(X,Y,T, t_flash, value_flash=255, value_background=0, save=False):
    list_frame = []
    for k in range(T):
        current_frame = np.zeros(X*Y).reshape(X,Y)
        if k == t_flash:
            current_frame.fill(value_flash)
        else:
            current_frame.fill(value_background)

        list_frame += [current_frame]

        if save:
            name = "frame" + str(k)
            cv2.imwrite("./"+name+".jpg",current_frame)
        else:
            return list_frame

def create_apparent_motion_stimulus(X,Y,T, t_point, t_interpoint, d_point, save=True):
    list_frame = []
    diameter = 10 #pixels

    duration_begin = math.floor((T-2*t_point-t_interpoint)/2) #frames
    duration_end = math.ceil((T-2*t_point-t_interpoint)/2) #frames

    d_edge = (Y - 2*diameter - d_point)/2 #pixels
    center_first_point = (X/2,d_edge + diameter/2) #pixels
    center_second_point = (X/2,Y-d_edge - diameter/2) #pixels

    for k in range(1,T+1):
        current_frame = np.zeros(X*Y).reshape(X,Y)
        if k>duration_begin and k<=duration_begin+t_point:
            for x in range(X):
                for y in range(Y):
                    if ((x-center_first_point[0])**2 + (y-center_first_point[1])**2) < (diameter/2) **2:
                        current_frame[x,y] = 255
        

        if k>T-duration_end-t_point and k<=T-duration_end:
            for x in range(X):
                for y in range(Y):
                    if ((x-center_second_point[0])**2 + (y-center_second_point[1])**2) < (diameter/2) **2:
                        current_frame[x,y] = 255

        list_frame += [current_frame]

        if save:
            name = "frame" + str(k)
            cv2.imwrite("/user/jemonet/home/Documents/Thèse/Code/Stimuli/apparent_motion_stimulus/"+name+".jpg",current_frame)
    
    # return list_frame



def create_fixedpoint_stimulus(X,Y,T, t_point, save=True):
    list_frame = []
    diameter = 10 #pixels

    duration_begin = math.floor(T/2 - t_point/2) #frames
    duration_end = math.ceil(T/2 + t_point/2) #frames

    center_first_point = (X/2,Y/2) #pixels

    for k in range(1,T+1):
        current_frame = np.zeros(X*Y).reshape(X,Y)
        if k>duration_begin and k<duration_end:
            for x in range(X):
                for y in range(Y):
                    if ((x-center_first_point[0])**2 + (y-center_first_point[1])**2) < (diameter/2) **2:
                        current_frame[x,y] = 255

        list_frame += [current_frame]

        if save:
            name = "frame" + str(k)
            cv2.imwrite("/user/jemonet/home/Documents/Thèse/Code/Stimuli/fixedpoint_stimulus/"+name+".jpg",current_frame)
    
    # return list_frame

