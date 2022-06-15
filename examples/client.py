
import cv2
import glfw
import Syphon


def main():
    client1 = Syphon.Client("client 1", show=False) # Syphon.Client("window name", show)
    client2 = Syphon.Client("client 2", show=False)
    
    while not client1.should_close() and not client2.should_close():
        frame = client1.draw(True)  # Syphon.Client.draw(True) return numpy array
        client2.draw() # Syphon.Client.draw(False) does not return numpy array
        
        if frame is not None:
            cv2.imshow("client cv2", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    glfw.terminate()
    cv2.destroyAllWindows()
    exit()  

if __name__ == "__main__":
    main()
