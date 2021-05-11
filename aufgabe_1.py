"""
 -----------------------------------------------------------------------------
Created: 08.02.2021, 13:04
 -----------------------------------------------------------------------------
Author: Matthieu Scherpf
Email: Matthieu.Scherpf@tu-dresden.de
Website: https://becuriouss.github.io/matthieuscherpf/
 -----------------------------------------------------------------------------
Purpose: Für Praktikum Mikrorechentechnik 2 - Versuch GMM 3 - Bildaufnahme und -verarbeitung mit OpenCV und Python
 -----------------------------------------------------------------------------
"""

# -----------------------------------------------------------------------------
# Import benötigter python Pakete bzw. Module
# -----------------------------------------------------------------------------
import cv2  # OpenCV Paket für Python
import numpy as np

# wenn dieses Skript über den Pythoninterpreter im Terminal gestartet wird, dann wird der folgende Code ausgeführt
if __name__ == '__main__':
    # -------------------------------------------------------------------------
    # Dem Konstruktor muss die ID (ein integer) der Kamera übergeben werden. Wenn nur eine Kamera am System angeschlossen ist, ist die ID <0>. Eventuell muss dieser Wert auf <1> gesetzt werden, sofern das System bspw. Front- und Rückkamera besitzt -> ausprobieren.
    # -------------------------------------------------------------------------
    cam_stream = cv2.VideoCapture(0)

    # -------------------------------------------------------------------------
    # OPTIONAL (zum experimentieren): Parameter können gesetzt werden (mit welcher Auflösung soll die Kamera ausgelesen werden, mit wie vielen Bildern pro Sekunde, etc.); Die Parameter werden nicht zwingend von der verwendeten Kamera unterstützt und es kann sein, dass die Kamera nicht mehr korrekt ausgelesen werden kann!
    # -------------------------------------------------------------------------
    # cam_stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # defaults to: 640
    # cam_stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # defaults to: 480
    # cam_stream.set(cv2.CAP_PROP_FPS, 30)  # defaults to: 30

    # -------------------------------------------------------------------------
    # Initialisiere ein Fenster, zur anzeige der Bilder; Das Fenster passt sich automatisch der Größe bzw. der Auflösung der Aufnahme an; Das Fenster wird später über den ersten Übergabeparameter <'Demo'> referenziert
    # -------------------------------------------------------------------------
    cv2.namedWindow('Aufgabe 1', cv2.WINDOW_AUTOSIZE)
    
    # -------------------------------------------------------------------------
    # Lese die Bilder der Kamera aus, bis die "ESC" Taste betätigt wird (Das Fenster muss hierbei angewählt (im Fokus) sein.)
    # -------------------------------------------------------------------------
    while True:
        # ---------------------------------------------------------------------
        # lese das nächste verfügbare frame der Kamera ein; Es werden zwei Werte zurückgegeben: boolean check (True, wenn das frame erfolgreich ausgelesen wurde, was hier nicht weiter geprüft wird; False sonst), frame (ein array, was die Werte des ausgelesenen frames enthält)
        # ---------------------------------------------------------------------
        check, frame = cam_stream.read()

        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # Verarbeitung des eingelesenen Bildes
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        img = frame
        img = cv2.resize(img, (0, 0), None, .5, .5)

        grey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        grey_3_channel = cv2.cvtColor(grey, cv2.COLOR_GRAY2BGR)  # Make the grey scale image have three channels

        ## convert to hsv
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        ## mask of green (36,25,25) ~ (86, 255,255)
        # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
        mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))

        ## slice the green
        imask = mask>0
        green = np.zeros_like(img, np.uint8)
        green[imask] = img[imask]

        ## save 
        #cv2.imwrite("green.png", green)

        numpy_vertical = np.vstack((img, green))
        # ---------------------------------------------------------------------
        # Anzeigen des manipulierten frames
        # ---------------------------------------------------------------------
        cv2.imshow('1 Heftiger Dude', numpy_vertical)
        
        # ---------------------------------------------------------------------
        # Prüfen, ob eine Nutzereingabe getätigt wurde um das Programm zu beenden; 27 entspricht der Escape-Taste (siehe ASCII Tabelle: http://www.asciitable.com/)
        # ---------------------------------------------------------------------
        if cv2.waitKey(1) == 27:
            break

        
    

    

    # -------------------------------------------------------------------------
    # Wenn das Programm via Escape-Taste beendet wurde muss die Kamera hierrüber informiert werden und noch geöffnete Fenster sauber geschlossen werden
    # -------------------------------------------------------------------------
    cam_stream.release()
    cv2.destroyAllWindows()
