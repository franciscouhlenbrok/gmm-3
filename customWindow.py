"""
 -----------------------------------------------------------------------------
Created: 08.02.2021, 16:17
 -----------------------------------------------------------------------------
Author: Matthieu Scherpf
Email: Matthieu.Scherpf@tu-dresden.de
Website: https://becuriouss.github.io/matthieuscherpf/
 -----------------------------------------------------------------------------
Purpose: Spezielle Klasse zur Nutzung eines OpenCV Fensters mit entsprechenden Reglern
 -----------------------------------------------------------------------------
"""

# -----------------------------------------------------------------------------
# Import benötigter python Pakete bzw. Module
# -----------------------------------------------------------------------------
import cv2
import time
import numpy as np


def nothing(x):
    pass


class CustomWindow:

    _INSTANCE_NAME = None
    _TIMESTAMPS = []

    @staticmethod
    def namedWindow(name, flag):
        """Diese Methode ist genauso zu bedienen wie die gleichnamige Methode aus OpenCV (->cv2.namedWindow(...)): Der name des Fensters und die Größe können gesetzt werden. Hier wird die Funktion um einstellbare Sliderelemente erweitert.
        """
        CustomWindow._INSTANCE_NAME = name
        # erstelle das Fenster mit den notwendigen Slidern
        cv2.namedWindow(name, flag)
        cv2.createTrackbar('th_ch1_low', name, 0, 255, nothing)
        cv2.createTrackbar('th_ch1_up', name, 255, 255, nothing)
        cv2.createTrackbar('th_ch2_low', name, 0, 255, nothing)
        cv2.createTrackbar('th_ch2_up', name, 255, 255, nothing)
        cv2.createTrackbar('th_ch3_low', name, 0, 255, nothing)
        cv2.createTrackbar('th_ch3_up', name, 255, 255, nothing)
        cv2.createTrackbar('noise_suppr', name, 0, 6, nothing)

    @staticmethod
    def imshow(name, frame, showThresholds):
        """Diese Methode ist genauso zu bedienen wie die gleichnamige Methode aus OpenCV (->cv2.imshow(...)): Der name des Fensters und das anzuzeigende frame können gesetzt werden. Hier wird die Funktion um die Anzeige der Bilder pro Sekunde erweitert.
        """
        # zeige zusätzlich die Anzahl der Bilder pro Sekunde im Livestream an
        CustomWindow._TIMESTAMPS.append(time.time())
        if len(CustomWindow._TIMESTAMPS) > 100:
            fps = np.around(
                1 / np.mean(np.diff(CustomWindow._TIMESTAMPS[-100:])), decimals=1)
            cv2.putText(frame, 'fps: '+str(fps), (0, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        if showThresholds:
            cv2.putText(frame, 'th_ch1_low: '+str(cv2.getTrackbarPos('th_ch1_low', name)), (0, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, 'th_ch1_up: '+str(cv2.getTrackbarPos('th_ch1_up', name)), (0, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, 'th_ch2_low: '+str(cv2.getTrackbarPos('th_ch2_low', name)), (0, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, 'th_ch2_up: '+str(cv2.getTrackbarPos('th_ch2_up', name)), (0, 250),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, 'th_ch3_low: '+str(cv2.getTrackbarPos('th_ch3_low', name)), (0, 300),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, 'th_ch3_up: '+str(cv2.getTrackbarPos('th_ch3_up', name)), (0, 350),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, 'noise_suppr: '+str(cv2.getTrackbarPos('noise_suppr', name)), (0, 400),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


        cv2.imshow(name, frame)

    @staticmethod
    def _get_thresholds():
        name = CustomWindow._INSTANCE_NAME
        # lese den aktuellen Wert der Slider aus
        th_ch1_low = cv2.getTrackbarPos('th_ch1_low', name)
        th_ch2_low = cv2.getTrackbarPos('th_ch2_low', name)
        th_ch3_low = cv2.getTrackbarPos('th_ch3_low', name)
        th_ch1_up = cv2.getTrackbarPos('th_ch1_up', name)
        th_ch2_up = cv2.getTrackbarPos('th_ch2_up', name)
        th_ch3_up = cv2.getTrackbarPos('th_ch3_up', name)
        noise_suppr = cv2.getTrackbarPos('noise_suppr', name)

        th_ch1 = (th_ch1_low, th_ch1_up)
        th_ch2 = (th_ch2_low, th_ch2_up)
        th_ch3 = (th_ch3_low, th_ch3_up)

        return th_ch1, th_ch2, th_ch3, noise_suppr
