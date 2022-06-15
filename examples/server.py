
import cv2
import Syphon
import glfw

def main():

    # window details
    size = (1280, 720)

    # window setup
    server1 = Syphon.Server("Server RGB", size, show=False) # Syphon.Server("window and syphon server name", frame size, show)
    server2 = Syphon.Server("Server Gray", size, show=False)


    cap = cv2.VideoCapture(1)
    if cap.isOpened() is False:
        raise("IO Error")
        
    # loop
    while not server1.should_close() and not server2.should_close():
        ret, frame = cap.read() #read camera image
        frame = cv2.resize(frame, size)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #BGR --> RGB
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #BGR --> GRAY
        frame_gray = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2RGB) # GRAY (3 channels)
        
        cv2.imshow("rgb", frame)
        server1.draw_and_send(frame_rgb) # Syphon.Server.draw_and_send(frame) draw frame using opengl and send it to syphon
        
        cv2.imshow("gray", frame_gray)
        server2.draw_and_send(frame_gray)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    glfw.terminate()
    cv2.destroyAllWindows()
    exit()


if __name__ == "__main__":
    main()
