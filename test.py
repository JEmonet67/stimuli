

def zzz(path_video, save=False):
    cam = cv2.VideoCapture(path_video)
    i = 0
    list_frame = []

    if save:
        try:
            if not os.path.exists("data"):
                os.makedirs("data")
        except:
            Print("Error in creating data directory.")

    
    has_frames,frame = cam.read()
    
    while has_frames:
        name = "frame" + str(i)
        print("Creating..." + name)

        if save:
            cv2.imwrite("./data/"+name+".jpg",frame)
        
        else:
            list_frame += [frame]
        
        i += 1
        has_frames,frame = cam.read()