import cv2
import numpy as np
import pyautogui

def capture_screen():
    # Capture a screenshot using pyautogui
    screenshot = pyautogui.screenshot(region=(0, 500, 1920, 300))

    # Convert the screenshot to a NumPy array (for OpenCV)
    frame = np.array(screenshot)

    # Convert it from RGB (PyAutoGUI format) to BGR (OpenCV format)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    return frame

def find_green_stars(frame):
    # Convert BGR to HSV for better color segmentation
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of green based on the approximate color of the stars
    lower_green = np.array([30, 100, 100])  # Adjusted HSV lower bound for bright green stars
    upper_green = np.array([90, 255, 255])  # Adjusted HSV upper bound for bright green stars

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv_frame, lower_green, upper_green)

    # Find contours in the masked image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter the contours to detect star-like shapes based on area and aspect ratio
    star_contours = []
    for contour in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)
        
        # Only consider contours with an area within a reasonable range for stars
        if 30 < area < 5000:  # Adjust the range as necessary for the star size
            # Calculate the bounding rectangle of the contour
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter out the grid lines (they will be long and thin)
            aspect_ratio = w / float(h)
            if 0.75 < aspect_ratio < 1.25:  # Stars will have aspect ratios close to 1 (more circular)
                star_contours.append((x, y, w, h))

    return star_contours

def find_white_buttons(frame):
    # Convert BGR to HSV for better color segmentation
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of white based on the color of the buttons
    lower_white = np.array([0, 0, 200])  # HSV lower bound for white
    upper_white = np.array([180, 30, 255])  # HSV upper bound for white

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv_frame, lower_white, upper_white)

    # Find contours in the masked image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter the contours to detect button-like shapes based on area and aspect ratio
    button_contours = []
    for contour in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)
        
        # Only consider contours with an area within a reasonable range for buttons
        if 600 < area < 50000:  # Adjust the range as necessary for the button size
            # Calculate the bounding rectangle of the contour
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter out the grid lines (they will be long and thin)
            aspect_ratio = w / float(h)
            if 0.75 < aspect_ratio < 6.5:  # Buttons are typically rectangular but not too elongated
                button_contours.append((x, y, w, h))

    return button_contours

def find_gray_bombs(frame):
    # Convert BGR to HSV for better color segmentation
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of gray based on the approximate color of the bombs
    lower_gray = np.array([0, 0, 40])  # Adjusted HSV lower bound for gray bombs
    upper_gray = np.array([180, 50, 220])  # Adjusted HSV upper bound for gray bombs

    # Threshold the HSV image to get only gray colors
    mask = cv2.inRange(hsv_frame, lower_gray, upper_gray)

    # Find contours in the masked image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter the contours to detect bomb-like shapes based on area and aspect ratio
    bomb_contours = []
    for contour in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)
        
        # Only consider contours with an area within a reasonable range for bombs
        if 30 < area < 5000:  # Adjust the range as necessary for the bomb size
            # Calculate the bounding rectangle of the contour
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter out the grid lines (they will be long and thin)
            aspect_ratio = w / float(h)
            if 0.75 < aspect_ratio < 1.25:  # Bombs will have aspect ratios close to 1 (more circular)
                bomb_contours.append((x, y, w, h))

    return bomb_contours

def main():
    # Capture the screen
    frame = capture_screen()

    # Find green stars
    stars = find_green_stars(frame)
    
    # Find gray bombs
    bombs = find_gray_bombs(frame)

    # Find white buttons
    buttons = find_white_buttons(frame)

    # Click on white buttons
    if len(buttons) > 0:
        for (x_button, y_button, w_button, h_button) in buttons:
            pyautogui.click(x_button + w_button // 2, y_button + h_button // 2 + 500)
            print(x_button, " ", y_button)

    # #print the coordinates of green stars that are not near bombs
    if len(stars) > 0:
        for (x_star, y_star, w_star, h_star) in stars:
            # Check if the star is too close to a bomb
            is_near_bomb = False
            for (x_bomb, y_bomb, w_bomb, h_bomb) in bombs:
                # Define the threshold distance to consider a star as near a bomb
                if abs(x_star - x_bomb) < w_star and abs(y_star - y_bomb) < h_star:
                    is_near_bomb = True
                    break
            
            # Only aim at stars not near bombs
            if not is_near_bomb:
                pyautogui.click(x_star , y_star + 500)
                cv2.rectangle(frame, (x_star, y_star), (x_star + w_star, y_star + h_star), (0, 255, 0), 2)
    
    cv2.imshow("Detected Stars", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()
