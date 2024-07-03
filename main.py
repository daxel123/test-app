from flet import *
import numpy as np
import cv2
import base64

def main(page: Page):

    myresult = Column()

    # Create a black image as a placeholder
    black_image = np.zeros((480, 640, 3), np.uint8)
    _, buffer = cv2.imencode('.jpg', black_image)
    black_image_str = base64.b64encode(buffer).decode()
    image_control = Image(src_base64=black_image_str)

    def readqrcode(e):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture image")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detector = cv2.QRCodeDetector()
            data, points, _ = detector.detectAndDecode(gray)

            # If OpenCV found the QR code and got text from the QR code
            if data:
                cv2.polylines(frame, [np.int32(points)], True, (255, 0, 0), 2, cv2.LINE_AA)
                print(f"El residuo debe ir a: {data}")

                # Push to Text widget if found 
                myresult.controls.append(
                    Text(data, size=25, weight="bold")
                )
                page.update()

                cap.release()
                # Close webcam if found text from QR code
                break

            # Encode frame to base64 to display in Flet app
            _, buffer = cv2.imencode('.jpg', frame)
            img_str = base64.b64encode(buffer).decode()
            image_control.src_base64 = img_str
            page.update()

            # If you press 'q' in the webcam window then close the webcam
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if cap.isOpened():
            cap.release()

    page.add(
        Column([
            Text("Clasificador de residuos", size=30, weight="bold"),
            ElevatedButton("Abrir camara",
                           bgcolor="blue", color="white",
                           on_click=readqrcode
            ),
            # Show result from your QR code to text widget
            Text("El residuo debe ir a:", size=20, weight="bold"),
            Divider(),
            myresult,
            image_control
        ])
    )

app(main)
