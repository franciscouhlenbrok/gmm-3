"""
 -----------------------------------------------------------------------------
Created: 08.02.2021, 21:43
 -----------------------------------------------------------------------------
Author: Matthieu Scherpf
Email: Matthieu.Scherpf@tu-dresden.de
Website: https://becuriouss.github.io/matthieuscherpf/
 -----------------------------------------------------------------------------
Purpose: Die hier definierte Klasse extrahiert den Blutvolumenpuls (auch als PPG bezeichnet) aus einem Bild. Essentiell ist die vorherige Anwendung einer Hautdetektion bspw. auf Basis einer Schwellwerterkennung. Das genaue Verständnis dieses Programmcodes ist für das Praktikum nicht notwendig!
 -----------------------------------------------------------------------------
"""

# -----------------------------------------------------------------------------
# Import benötigter python Pakete bzw. Module
# -----------------------------------------------------------------------------
import cv2
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class PPGExtractor():

    def __init__(self, sample_freq=30, plot_secs=10, execs=5):

        self.sample_freq = sample_freq
        self.plot_secs = plot_secs
        self.execs = execs
        self.name = 'imaging photoplethysmogram'
        cv2.namedWindow(self.name, cv2.WINDOW_AUTOSIZE)
        self.fig, self.axs = plt.subplots(1, 1, figsize=(5, 5))
        self.pm = np.array([
            [0,   1,  -1],
            [-2,   1,   1]
        ])
        self.tmp_norm_n_frames = int(np.ceil(self.sample_freq * 1.6))
        self.rgb_seq = np.zeros(
            (self.sample_freq * self.plot_secs + self.execs+1, 3))
        self.counter = 0
        self.exec_counter = 0

    def process_frame(self, frame):
        """Diese Methode wertet das übergebene Bild aus und zeigt es im entsprechenden Fenster an. Hierfür wird direkt auf die Klasse CustomWindow zurückgegriffen.
        """

        n_skin_pixels = np.sum(frame != 0) / 3
        self.rgb_seq[self.counter, :] = (
            np.sum(frame, axis=(0, 1))/n_skin_pixels)
        self.counter += 1
        self.exec_counter += 1

        if (self.counter >= self.sample_freq * self.plot_secs + 1) \
                and self.exec_counter % self.execs == 0:
            bvp = self._extract_bvp().squeeze()
            i_end = bvp.shape[0] - int(self.sample_freq * 1.6)
            i_start = i_end - int(self.sample_freq * 3)
            self.axs.cla()
            sos = signal.butter(8, (0.5, 4.0), btype='bandpass',
                                fs=self.sample_freq, output='sos')
            y = signal.sosfilt(sos, bvp)[i_start:i_end]
            self.axs.plot(y)
            self.fig.canvas.draw()
            img = np.fromstring(self.fig.canvas.tostring_rgb(), dtype=np.uint8,
                                sep='')
            img = img.reshape(self.fig.canvas.get_width_height()[::-1] + (3,))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            cv2.imshow(self.name, img)
            self.rgb_seq = np.roll(self.rgb_seq, -self.execs, axis=0)
            self.counter -= self.execs

    def _extract_bvp(self):

        # compute bvp
        n = self.rgb_seq.shape[0]  # number of sample points, i.e. frames
        h = np.zeros((1, n))
        c = self.rgb_seq
        # loop over overlapping windows
        for i in range(n):
            m = i - self.tmp_norm_n_frames
            if m >= 0:
                # temporal normalization
                cn = c[m:i] / np.mean(c[m:i], axis=0)
                # projection
                s = np.matmul(self.pm, np.transpose(cn))
                s1 = s[0, :]
                s2 = s[1, :]
                # tuning
                hi = s1 + (s1.std() / s2.std()) * s2
                # overlap-adding
                h[0, m:i] = h[0, m:i] + (hi - hi.mean())/hi.std()

        return h.squeeze()[:, np.newaxis]
