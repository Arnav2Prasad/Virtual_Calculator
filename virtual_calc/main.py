import cv2

# to see if we have clicked on the button
from cvzone.HandTrackingModule import HandDetector


class Button:
    def __init__(self,pos , width , height , value):

        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

        # we are not drawing in the init as draw is being done in the while loop
        # so we create a seperate method , that we will call it in the while loop

    def draw(self,img):
        # draw rectangle
        cv2.rectangle(img , self.pos , (self.pos[0] + self.width ,self.pos[1] +  self.height), 
            (225,225,225) , cv2.FILLED)
        cv2.rectangle(img , self.pos , (self.pos[0] + self.width ,self.pos[1] +  self.height), 
        (50,50,50) , 3)
        cv2.putText(img , self.value , (self.pos[0] + 40 , self.pos[1] + 60) , 
            cv2.FONT_HERSHEY_PLAIN , 2,(50,50,50) , 2)



# webcam
# 0 : default camera
cap = cv2.VideoCapture(0)

# the initial size is not sufficient to put all keys of calc in the frame,
# so we increase the frame size(we could also had decreased the key size but we didnt!)
cap.set(3,1280)  #width
cap.set(4,720)  #height


# INITIALIZARION
# normally its 0.5
# so if its confident of more than 80% then it will detect the hand! as we dont falso click so we 
# bring it to max value
# we need only 1 hand , not multiple hand
detector = HandDetector(detectionCon = 0.8 , maxHands = 1)


# Creatuing buttons
buttonListValues = [['7','8','9','*'], 
                ['4','5','6','-'],
                ['1','2','3','+'],
                ['0','/','.','=']]

# creating 16 buttons
# button1 = Button((700,150) , 100,100 , '5')
# creating button1 button2 button3 4 5 6.. variables are not good so we create a list
buttonList=[]
# 4 by 4
for x in range(4):
    for y in range(4):  
        # offset 800
        # y pos = 100
        xpos = x*100 + 800
        ypos = y*100 + 150
        buttonList.append(Button((xpos,ypos) , 100,100 , buttonListValues[y][x]))


# variables
myEquation = '10+5'



# loop
while True:
    # Get image from webcam
    success , img = cap.read()

    # we have to flip the image as our left is right and R->L
    # so flip horizontally (1)
    # 0 : vertically
    img = cv2.flip(img,1)

    # now we have to detect our hand
    # detection of 1 hand(not many)
    # send all list of points to hands and also image
    hands,img = detector.findHands(img , flipType = False)

    # now create buttons for each of the calculator
    # so create class button and so create 16 objects
    # hard coding all buttons seperately wll be difficult
    # so use OOPs

    # approach : first create a button , hardcode it 
    # and then use the logic to create class!
    # we need text , pin  point location , have some border
    #  Know dimension , location
    
    # # draw rectangle
    # cv2.rectangle(img , (100,100) , (200,200), (225,225,225) , cv2.FILLED)
    # # add border around it
    # cv2.rectangle(img , (100,100) , (200,200), (50,50,50) , 3)

    # # border : 50,50,50
    # # thickness = 2
    # cv2.putText(img , "9" , (100+20 , 100+50) , cv2.FONT_HERSHEY_PLAIN , 2,(50,50,50) , 2)


    # Draw all buttons
    # draw rectangle
    cv2.rectangle(img , (800,50) , (800 + 400, 70 + 100), 
            (225,225,225) , cv2.FILLED)
    cv2.rectangle(img , (800,50) , (800 + 400, 70 + 100), 
        (50,50,50) , 3)

    
    for button in buttonList:
        button.draw(img)
    # button1.draw(img)

    # check for hand
    if hands :
        # we will find disatnce betwene our fingers
        # lm : landmark
        lmList = hands[0]['lmList']
        # 8 : index
        # 12 : thumb
        length , _ , img = detector.findDistance(lmList[8][:2] , lmList[12][:2] , img)
        x , y = lmList[8]
        print(length)
        if length < 50:
            # check each of buttons which one was pressed get loc 
            pass

    # processing

    # display the Equation/Result
    cv2.putText(img , myEquation , (810 , 120) , 
            cv2.FONT_HERSHEY_PLAIN , 3,(50,50,50) , 3)


    # display image
    cv2.imshow("Image" , img)
    # 1 milli sec delay
    cv2.waitKey(1)

