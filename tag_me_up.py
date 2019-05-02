import cv2
import argparse, os
from copy import deepcopy
import json

colors = [
    # B, G, R
    (0, 255, 0),     # green
    (255, 0, 0),     # blue
    (0, 0, 255),     # red
    (255, 0, 255),   # magenta
    (0, 255, 255),   # yellow
    (255, 255, 0),   # cyan
    (0, 0, 0),       # black
    (255, 255, 255), # white
]

# ----------------------------------------------------------------- GLOBAL VARIABLES 
def_wid = 32
def_hei = 32
init_point = 'c'
num_classes = 1
output = os.path.dirname(os.path.realpath(__file__)) + "/output/"
output_ext = 'png'

patches = []
patches_deleted = []

prev_imgs = []
next_imgs = []
current_img = ""

current_class = 0
current_patch = {
    'p1'    : [],
    'p2'    : [],
    'class' : 0
}

# ------------------------------------------------------------------- Helper Functions
def get_file_name():
    global current_img

    file_name = current_img.split('/')
    return file_name[len(file_name)-1].split('.')[0]

def get_prev_img():
    global current_img
    global next_imgs
    global prev_imgs

    # conc at the beginning
    next_imgs = [current_img] + next_imgs
    current_img = prev_imgs.pop()

    return cv2.imread(current_img, -1)

def get_next_img():
    global current_img
    global next_imgs
    global prev_imgs

    prev_imgs.append(current_img)
    current_img = next_imgs.pop(0)

    return cv2.imread(current_img, -1)

def load_imgs(image):
    global current_img
    
    if os.path.isdir(image):
        global next_imgs
        list_imgs = os.listdir(image)
        current_img = image + list_imgs[0]
        next_imgs = [image + i for i in list_imgs[1:]]
        print("Number of files read as input: {}\n".format(len(next_imgs) + 1))

    elif os.path.isfile(image):
        print("Number of files read as input: 1\n")
        current_img = image

    else:
        print("Wrong input image/dir!")
        return []

    return cv2.imread(current_img, -1)

def get_json(file_name):
    global patches
    global output

    if os.path.isfile(output + "json/" + file_name + ".json"):
        with open(output + "json/" + file_name + ".json", 'r') as jfile:
            patches = json.loads(jfile.read())
    

def non_required_args_reader(args, img, file_name):
    global def_wid
    global def_hei
    global init_point
    global num_classes
    global output
    global output_ext
    global patches

    if 'x' in args["dimensions"]:
        def_hei, def_wid = [int(i) for i in args["dimensions"].split('x')]
    else:
        print(img.shape)
        def_hei, def_wid = img.shape[:2]
        def_hei, def_wid = int(def_wid * float(args["dimensions"])), int(def_hei * float(args["dimensions"]))
        print(def_hei, def_wid)

    init_point = args["init_point"]
    num_classes = int(args["num_classes"])
    output = args["output"]
    output_ext = args['extension']

    if not os.path.exists(output + "json/"):
        os.mkdir(output + "json/")
    else:
        get_json(file_name)

    if not os.path.exists(output + "tags/"):
        os.mkdir(output + "tags/")
    
    if not os.path.exists(output + "crops/"):
        os.mkdir(output + "crops/")

    

def crop(img, file_name):
    global patches
    global output
    global num_classes
    global output_ext


    for i, patch in zip(range(len(patches)), patches):
        out_file = "{}crops/{}${}.{}".format(output, file_name, i, output_ext)
        
        new_img = img[patch['p1'][1]:patch['p2'][1], patch['p1'][0]:patch['p2'][0], :]
        cv2.imwrite(out_file, new_img)
        

def draw_rect(img, i):
    global patches
    global colors
    global current_class

    if patches[i]['p1'] == patches[i]['p2']:
        if init_point  == 'tl':
            patches[i]['p2'][0] += def_hei-1
            patches[i]['p2'][1] += def_wid-1
        else:
            half_wid = def_wid//2 - 1
            half_hei = def_hei//2 - 1
            patches[i]['p1'][0] -= half_hei
            patches[i]['p1'][1] -= half_wid
            patches[i]['p2'][0] += half_hei
            patches[i]['p2'][1] += half_wid

    patches[i]['p1']  = tuple(patches[i]['p1'])
    patches[i]['p2']  = tuple(patches[i]['p2'])

    #print(patches[i])
    cv2.rectangle(img, patches[i]['p1'], patches[i]['p2'], colors[patches[i]['class'] % 8], 1)

def redraw_img(img):
    global patches

    for i in range(len(patches)):
        draw_rect(img, i)
    cv2.imshow("labelMeUp", img)

def insert_new_rect(img):
    global patches

    draw_rect(img, len(patches)-1)
    cv2.imshow("labelMeUp", img)

# ------------------------------------------------------- Callback function

def get_patch(event, x, y, flags, param):
    global patches

    if event == cv2.EVENT_LBUTTONDOWN:
        current_patch['p1'] = [x, y]
    
    elif event == cv2.EVENT_LBUTTONUP:
        current_patch['p2'] = [x, y]
        current_patch['class'] = current_class

        patches.append(deepcopy(current_patch))
        insert_new_rect(img)

# ---------------------------------------------------------- Main
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help=" Path to the image sample or directory of images to be labelled.")
ap.add_argument("-d", "--dimensions" , required=False, default="32x32", help="Annotation's default size. Can be used as HEIGHTxWIDHT (ex.: '96x128') or as a proportion of the original input image sample (ex.: 0.1). Default: '32x32'.")
ap.add_argument("-p", "--init_point" , required=False, default="c"    , help="Initial point of the annotation. Options:  tl (Top Left) or c (Center). Default: 'c'.")
ap.add_argument("-n", "--num_classes", required=False, default=1      , help="Total of classes. Default: 1.")
ap.add_argument("-o", "--output"     , required=False, default=output , help="Output directory.")
ap.add_argument("-e", "--extension"  , required=False, default='png'  , help="Output image file format (png or jpg). Dafault: 'png'.")

# parse the args and save them
args = vars(ap.parse_args())
#img = cv2.imread(args["image"], -1)
img = load_imgs(args["image"]) 


if len(img):
    file_name = get_file_name()

    count = 1
    print("Image read: " + file_name + " / Count: " + str(count))

    non_required_args_reader(args, img, file_name)

    backup = img.copy()
    cv2.namedWindow("labelMeUp")
    cv2.setMouseCallback("labelMeUp", get_patch)

    if patches:
        redraw_img(img)
    else:
        cv2.imshow("labelMeUp", img)
    
    break_point = False
else:
    break_point = True

while not break_point:
    key = cv2.waitKey(1) & 0xFF

    # press 'r' to reset img
    if key == ord("r"):
        img = backup.copy()
        patches_deleted.extend(patches)
        patches = []
        redraw_img(img)

    # press 'w' to change class
    elif key == ord("w"):
        print(">>> Please insert new class tag: ")
        aux = int(input())
        while (aux >= num_classes):
            print(">>> Class tag must be a number between 0 and {}!".format(num_classes-1))
            print(">>> Please insert new class tag: ")
            aux = int(input())
        current_class = aux

    # press 'z' to cancel last patch
    elif key == ord("z"):
        if patches:
            img = backup.copy()
            patches_deleted.append(patches.pop())
            redraw_img(img)

    # press 'x' to reinsert last deleted patch
    elif key == ord("c"):
        if patches_deleted:
            patches.append(patches_deleted.pop())
            insert_new_rect(img)

    # press 'c' to crop imgs from tagged patches
    elif key == ord("x"):
        print("Cropping...")
        crop(backup, file_name)

    # press 'd' to get next image
    elif key == ord("d"):
        if next_imgs:
            patches = []
            patches_deleted = []
            
            print("\nGetting next image...")
            img = get_next_img()
            backup = img.copy()
            file_name = get_file_name()
            get_json(file_name)

            count += 1
            print("Image read: " + file_name + " / Count: " + str(count) + "\n")
            redraw_img(img)
    
     # press 'a' to get previous image
    elif key == ord("a"):
        if prev_imgs:
            patches = []
            patches_deleted = []

            print("\nGetting previous image...")
            img = get_prev_img()
            backup = img.copy()
            file_name = get_file_name()
            get_json(file_name)

            count -= 1
            print("Image read: " + file_name + " / Count: " + str(count) + "\n")
            redraw_img(img)

    # press 's' to save labels to jason file
    elif key == ord("s"):
        print("Saving output...")
        with open(output +"json/"+file_name+'.json', 'w') as json_file:
                json.dump(patches, json_file, indent=2)
                json_file.write("\n")
        cv2.imwrite("{}tags/{}.{}".format( output, file_name, output_ext), img)

    # press 'esc' to quit
    elif key == 27:
        print("Quitting...")
        break_point = True

cv2.destroyAllWindows()
