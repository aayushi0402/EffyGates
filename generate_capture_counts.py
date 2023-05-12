import cv2 as cv
import os
from time import time
import os.path
import csv
from datetime import date

def run_count(captured_img_path,img_timestamp):
  img = transform(Image.open(captured_img_path).convert('RGB')).cuda()
  output = model(img.unsqueeze(0))
  predicted_cnt = int(output.detach().cpu().sum().numpy())
  return (img_timestamp,captured_img_path,"front_gate",predicted_cnt)


def write_counts(img_details):
    if os.path.isfile(os.getcwd()+f'/Count_Reports/Count_Report_{date.today().strftime("%Y%m%d")}.csv'):
        with open(os.getcwd()+f'/Count_Reports/Count_Report_{date.today().strftime("%Y%m%d")}.csv', 'a') as file:
            writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([f"{img_details[0]}", f"{img_details[1]}", f"{img_details[2]}",f"{img_details[3]}"])
    else:
        cr_path = os.getcwd()+f'/Count_Reports/'
        isExist = os.path.exists(os.getcwd()+f'/Count_Reports/')
        if not isExist:
            os.makedirs(cr_path)
        with open(os.getcwd()+f'/Count_Reports/Count_Report_{date.today().strftime("%Y%m%d")}.csv', 'w') as file:
            writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            field = ["capture_timestamp", "image_path", "location","count"]
        
            writer.writerow(field)
            writer.writerow([f"{img_details[0]}", f"{img_details[1]}", f"{img_details[2]}",f"{img_details[3]}"])

file = "realshort.mp4"

if not os.path.isfile(file):
    print("File not found!")

# images forder name
folder_name = base=os.path.basename(file) + " frames"

# create folder for images in current path if not exists
current_path = os.getcwd()
folder_path = os.path.join(current_path, folder_name)

if not os.path.exists(folder_path):
    os.mkdir(folder_path)

cap = cv.VideoCapture(file)

total_frame = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

# save frame every # seconds
seconds = 10
fps = cap.get(cv.CAP_PROP_FPS) # Gets the frames per second
# calculates number of frames that creates 10 seconds of video
multiplier = fps * seconds

# Check if camera opened successfully
if (cap.isOpened()== False):
    print("Error opening video stream or file")

frame_counter = 1

while frame_counter <= total_frame:

    cap.set(cv.CAP_PROP_POS_FRAMES, frame_counter)

    ret, frame = cap.read()

    # save frame
    # file path
    file_path = os.path.join(folder_path, str(time()) + ".jpg")
    cv.imwrite(file_path, frame)
    #count to sheet script
    img_details = run_count(captured_img_path,img_timestamp)
    write_counts(img_details)
    frame_counter += multiplier