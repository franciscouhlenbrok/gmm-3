"""
 -----------------------------------------------------------------------------
Created: 08.02.2021, 13:10
 -----------------------------------------------------------------------------
Author: Matthieu Scherpf
Email: Matthieu.Scherpf@tu-dresden.de
Website: https://becuriouss.github.io/matthieuscherpf/
 -----------------------------------------------------------------------------
Purpose: Schwellwertfilter für die Erkennung von Haut in einem Bild; Dies ist ein notwendiger Schritt, um das PPG (wird im Krankenhaus über das bekannte Pulsoximeter aufgenommen) zu extrahieren; Aus diesem können dann Vitalparameter wie Herzrate und Atemrate abgeleitet werden; Das genaue Verständnis dieses Programmcodes ist für das Praktikum nicht notwendig!
 -----------------------------------------------------------------------------
"""

# -----------------------------------------------------------------------------
# Import benötigter python Pakete bzw. Module
# -----------------------------------------------------------------------------
import numpy as np
import cv2
from customWindow import CustomWindow

# -----------------------------------------------------------------------------
# Funktion zur Anwendung eines Schwellwerts auf ein von der Kamera aufgenommenes und mit OpenCV ausgelesenes frame; Die Funktion verlangt obligatorisch ein frame als Übergabeparameter und optional die Übergabe der Schwellwerte; Die Schwellwerte können angepasst werden, um die Güte der Hautdetektion zu verbessern
# -----------------------------------------------------------------------------


def apply_threshold(frame,
                    th_ch_1=(0, 255),
                    th_ch_2=(0, 255),
                    th_ch_3=(0, 255),
                    transform='hsv'):
    """Diese Funktion wendet einen Schwellwertfilter auf das übergebene Bild an. Die Schwellwerte können über ein Fenster der Klasse CustomWindow eingestellt werden.
    """

    # -------------------------------------------------------------------------
    # Prüfe ob eine Instanz von CustomWindow existiert und somit die Schwellwerte aus den Slidereinstellungen genommen werden können
    # -------------------------------------------------------------------------
    if CustomWindow._INSTANCE_NAME != None:
        th_ch_1, th_ch_2, th_ch_3, noise_suppr = CustomWindow._get_thresholds()

    # -------------------------------------------------------------------------
    # Durchführung einer Farbraumtransformation; Die Idee ist, dass sich Haut von nicht-Haut in einem anderen Farbraum als RGB besser voneinander trennen lassen
    # -------------------------------------------------------------------------
    if transform == 'hsv':
        frame_tr = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    elif transform == 'ycrcb':
        frame_tr = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)

    # -------------------------------------------------------------------------
    # Definition der Schwellwert-arrays
    # -------------------------------------------------------------------------
    lower_tr_values = np.array(
        [th_ch_1[0], th_ch_2[0], th_ch_3[0]], dtype="uint8")
    upper_tr_values = np.array(
        [th_ch_1[1], th_ch_2[1], th_ch_3[1]], dtype="uint8")

    # -------------------------------------------------------------------------
    # Anwendung der Schwellwerte auf das Originalbild
    # -------------------------------------------------------------------------
    mask_tr = cv2.inRange(
        frame_tr, lower_tr_values, upper_tr_values)

    # -------------------------------------------------------------------------
    # Rauschverminderung
    # -------------------------------------------------------------------------
    mask_tr = cv2.erode(mask_tr, None, iterations=noise_suppr)

    # -------------------------------------------------------------------------
    # Anwendung der finalen Hautmaske auf das Originalbild
    # -------------------------------------------------------------------------
    frame_roi = cv2.bitwise_and(frame, frame, mask=mask_tr)

    return frame_roi
