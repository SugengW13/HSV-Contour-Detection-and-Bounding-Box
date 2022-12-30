import cv2
import numpy as np

# Trackbars Initialization
def callback(x):
    pass

def init_trackbars():
    cv2.namedWindow('HSV Trackbars')
    cv2.createTrackbar('LH', 'HSV Trackbars', 0, 255, callback)
    cv2.createTrackbar('LS', 'HSV Trackbars', 0, 255, callback)
    cv2.createTrackbar('LV', 'HSV Trackbars', 0, 255, callback)
    cv2.createTrackbar('UH', 'HSV Trackbars', 255, 255, callback)
    cv2.createTrackbar('US', 'HSV Trackbars', 255, 255, callback)
    cv2.createTrackbar('UV', 'HSV Trackbars', 255, 255, callback)

def get_lower_value():
    lower_hue = cv2.getTrackbarPos('LH', 'HSV Trackbars')
    lower_sat = cv2.getTrackbarPos('LS', 'HSV Trackbars')
    lower_val = cv2.getTrackbarPos('LV', 'HSV Trackbars')

    return (lower_hue, lower_sat, lower_val)

def get_upper_value():
    upper_hue = cv2.getTrackbarPos('UH', 'HSV Trackbars')
    upper_sat = cv2.getTrackbarPos('US', 'HSV Trackbars')
    upper_val = cv2.getTrackbarPos('UV', 'HSV Trackbars')

    return (upper_hue, upper_sat, upper_val)

# Get Contour
def set_contour(image):
    # Create Array 5 x 5 with values of 1
    kernel = np.ones((5, 5), np.uint8)
    # Remove noises
    mask = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    # Close small holes
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    return contours

def main(capture):
    while True:
        ret, frame = capture.read()
        
        try:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lower_hsv = get_lower_value()
            upper_hsv = get_upper_value()

            thresh = cv2.inRange(hsv, lower_hsv, upper_hsv)
            
            contours = set_contour(thresh)

            outlined_frame = cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

            cv2.imshow('Threshold', thresh)
            cv2.imshow('Contours', outlined_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            continue

    frame.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    init_trackbars()

    camera = cv2.VideoCapture(0)
    
    main(camera)
