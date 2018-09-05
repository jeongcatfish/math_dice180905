
import cv2
import numpy as np
import time
import pyautogui

screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()
pyautogui.moveTo(2400, 600)

status=1
cam = cv2.VideoCapture(1)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,800)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,500)

lower_blue = np.array([100, 120, 120])
upper_blue = np.array([120, 255, 155])
lower_red = np.array([160,150,150])
upper_red = np.array([180,255,255])
kernel = np.ones((5, 5), np.uint8)

kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))
pp=0

def detect_Redcolor(img,image):

    try:
        mask= cv2.inRange(hsv,lower_red,upper_red)
        mask_red=cv2.bitwise_and(frame,frame,mask=mask)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        gradient = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)
        x,y,w,h= cv2.boundingRect(gradient)

        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,255),1)

        cv2.imshow('red_mask',mask_red)
        cv2.imshow('frame2',image)
        img_trim = image[y:y+h ,x:x+w]
        cv2.imwrite("C:/rec_dice/red_dice.jpg", img_trim)

        return x,y,w,h
    except:
        print("error in function detect_Redcolor")

def detect_Bluecolor(img,image):
    try:
        mask= cv2.inRange(hsv,lower_blue,upper_blue)
        mask_blue=cv2.bitwise_and(frame,frame,mask=mask)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        gradient = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)
        x,y,w,h= cv2.boundingRect(gradient)

        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,255),1)

        cv2.imshow('blue_mask',mask_blue)
        cv2.imshow('frame1',image)
        img_trim = image[y:y+h ,x:x+w]
        cv2.imwrite("C:/rec_dice/blue_dice.jpg", img_trim)

        return x,y,w,h
    except:
        print("error in function detect_Bluecolor")

def detect_circle(st):
    r_ct=0
    b_ct = 0
    data = 0 # r_ct + b_ctq

    try:
        blue_dice=cv2.imread('C:/rec_dice/blue_dice.jpg',0)
        zoom_blue = cv2.resize(blue_dice, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        zoom_blue = cv2.medianBlur(zoom_blue,5)
        cblue_dice = cv2.cvtColor(zoom_blue, cv2.COLOR_GRAY2BGR)

        circles2 = cv2.HoughCircles(zoom_blue, cv2.HOUGH_GRADIENT, 1, 10, param1=50, param2=25, minRadius=10, maxRadius=50)

        circles2 = np.uint16(np.around(circles2))

        for i in circles2[0, :]:
            cv2.circle(cblue_dice, (i[0], i[1]), i[2], (0, 255, 0), 1)
            cv2.circle(cblue_dice, (i[0], i[1]), 2, (0, 0, 255), 2)
            b_ct=b_ct+1

        #cv2.imshow('Blue', cblue_dice)
        print("blue dice : %d" %(b_ct))
        #print(b_ct)
        cv2.imshow('Blue', cblue_dice)
    except:
        print("error at [blue_dice] there is no circle to detect...")

    finally:
        print("blue finished")


    try:
        red_dice=cv2.imread('C:/rec_dice/red_dice.jpg',0)
        zoom2 = cv2.resize(red_dice, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        zoom2 = cv2.medianBlur(zoom2,5)
        cred_dice = cv2.cvtColor(zoom2, cv2.COLOR_GRAY2BGR)

        circles1 = cv2.HoughCircles(zoom2, cv2.HOUGH_GRADIENT, 1, 10, param1=50, param2=25, minRadius=10, maxRadius=50)

        circles1 = np.uint16(np.around(circles1))

        for i in circles1[0, :]:
            cv2.circle(cred_dice, (i[0], i[1]), i[2], (0, 255, 0), 1)
            cv2.circle(cred_dice, (i[0], i[1]), 2, (0, 0, 255), 2)
            r_ct=r_ct+1

        #cv2.imshow('Red', cred_dice)
        print("red dice : %d" %(r_ct))
        cv2.imshow('Red', cred_dice)
        cv2.waitKey(0)   ###### 주사위 체크 ###### ###### 주사위 체크 ######  ###### 주사위 체크 ######
    except:
        print("error at red_dice there is no circle to detect...")

    finally:
        print("red finished")

    data = r_ct + b_ct
    print("dice : %d" % (data))
    data = str(data)

    print("number thrown = %d" %(st))

    if(st % 2 == 1):
        print("in st 11111")
        #with open(r"\\192.168.1.4\test1\table2_data.txt", 'w') as f:  #메인 PC 아이피, 메인 PC에서 공유폴더를 생성해야 동작.
        with open(r"\\192.168.200.111\test1\table2_data.txt", 'w') as f:
            f.write('3')
            f.write(data)
        st=2
    elif(st % 2 == 0):
        print("in st 222222")
        #with open(r"\\192.168.1.4\test1\table2_data.txt", 'w') as f:  #메인 PC 아이피, 메인 PC에서 공유폴더를 생성해야 동작.
        with open(r"\\192.168.200.111\test1\table2_data.txt", 'w') as f:
            f.write('4')
            f.write(data)
        st=1

    cv2.destroyAllWindows()
    return data,st

if __name__ == '__main__':
    st = 1
    pt=0
    preprevent=0
    while True:
        if (st > 10):
            st = 1;
        ret,frame = cam.read()
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        red_edge=detect_Redcolor(hsv,frame)
        blue_edge=detect_Bluecolor(hsv, frame)
        pp = pp + 1
        k=cv2.waitKey(1)
        if k== 113: ##Enter
            prevent,qq = detect_circle(st)
            #print("prevent : : :  %d"  %(qq))
            if(prevent == preprevent):
                pt=pt+1
            if(pt>=10):
                print("time to sleep ~~~~~~~~~~~~~~~~~")
                #with open(r"\\192.168.1.4\test1\table2_data.txt", 'w') as f:  # 메인 PC 아이피, 메인 PC에서 공유폴더를 생성해야 동작
                with open(r"\\192.168.200.111\test1\table2_data.txt", 'w') as f:  # 메인 PC 아이피, 메인 PC에서 공유폴더를 생성해야 동작# .
                    if(qq % 2 == 1):
                        f.write('399')  #index.html에서는 99로 전달. data.substring(1,3) == 99
                    elif(qq % 2 == 0):
                        f.write('498')
                time.sleep(1)
                pt=0
            st=st+1
            preprevent = prevent
            pyautogui.click()

        if k== 27:
            break
        if not ret:
            print('error')
            break

    cv2.destroyAllWindows()
