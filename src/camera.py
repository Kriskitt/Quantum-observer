##import cv2
##import mediapipe as mp
##import threading
##import time
##
##class CameraManager:
##    def __init__(self, camera_index=0):
##        self.camera_index = camera_index
##        self.cap = None
##        self.current_frame = None
##        self.is_observing = False
##        self.running = False
##        self.lock = threading.Lock()
##
##        # Configuración de MediaPipe Face Mesh para detección de Iris
##        self.mp_face_mesh = mp.solutions.face_mesh
##        self.face_mesh = self.mp_face_mesh.FaceMesh(
##            max_num_faces=1,
##            refine_landmarks=True, # Crucial para habilitar los puntos del iris
##            min_detection_confidence=0.5,
##            min_tracking_confidence=0.5
##        )
##
##    def start(self):
##        self.cap = cv2.VideoCapture(self.camera_index)
##        self.running = True
##        self.thread = threading.Thread(target=self._update, daemon=True)
##        self.thread.start()
##
##    def _update(self):
##        while self.running:
##            ret, frame = self.cap.read()
##            if not ret:
##                print("⚠️ OpenCV no recibe video: Revisa los permisos o el índice de la cámara en config.json")
##                time.sleep(1) # Espera 1 segundo para no saturar la terminal
##                continue
##
##            # Invertir el frame (efecto espejo) para una interacción natural
##            frame = cv2.flip(frame, 1)
##            # MediaPipe y Pygame usan RGB; OpenCV usa BGR por defecto
##            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
##            
##            results = self.face_mesh.process(rgb_frame)
##            observing = False
##
##            if results.multi_face_landmarks:
##                for face_landmarks in results.multi_face_landmarks:
##                    # Aquí implementaremos más adelante el vector de mirada estricto.
##                    # Por ahora, la simple presencia del iris de frente a la cámara 
##                    # activa el estado de colapso.
##                    observing = True 
##
##            # Usamos Lock para que Pygame pueda leer estas variables sin bloqueos
##            with self.lock:
##                self.current_frame = rgb_frame
##                self.is_observing = observing
##
##            # Pequeña pausa para no saturar la CPU
##            time.sleep(0.01) 
##
##    def get_state(self):
##        """Retorna el estado actual de observación y el último frame limpio"""
##        with self.lock:
##            return self.is_observing, self.current_frame
##
##    def stop(self):
##        self.running = False
##        if self.thread.is_alive():
##            self.thread.join()
##        if self.cap:
##            self.cap.release()
##        self.face_mesh.close()
##
import cv2
import mediapipe as mp
import threading
import time
import math # Necesario para calcular distancias matemáticas

class CameraManager:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.current_frame = None
        self.is_observing = False
        self.running = False
        self.lock = threading.Lock()

        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def start(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        self.running = True
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

    def _get_distance(self, p1, p2, landmarks):
        """Calcula la distancia euclidiana entre dos puntos de la malla facial."""
        x1, y1 = landmarks.landmark[p1].x, landmarks.landmark[p1].y
        x2, y2 = landmarks.landmark[p2].x, landmarks.landmark[p2].y
        return math.hypot(x2 - x1, y2 - y1)

    def _update(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("⚠️ OpenCV no recibe video.")
                time.sleep(1)
                continue

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            observing = False

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Índices de MediaPipe para el Ojo Izquierdo
                    # Horizontal: 33 a 133 | Vertical: 159 a 145
                    izq_h = self._get_distance(33, 133, face_landmarks)
                    izq_v = self._get_distance(159, 145, face_landmarks)
                    ear_izq = izq_v / izq_h if izq_h > 0 else 0

                    # Índices de MediaPipe para el Ojo Derecho
                    # Horizontal: 362 a 263 | Vertical: 386 a 374
                    der_h = self._get_distance(362, 263, face_landmarks)
                    der_v = self._get_distance(386, 374, face_landmarks)
                    ear_der = der_v / der_h if der_h > 0 else 0

                    # Umbral de apertura: ~0.22 es el estándar para un ojo abierto
                    # Si ambos ojos superan el umbral, significa que estás observando
                    if ear_izq > 0.22 and ear_der > 0.22:
                        observing = True
                    else:
                        observing = False

            with self.lock:
                self.current_frame = rgb_frame
                self.is_observing = observing

            time.sleep(0.01)

    def get_state(self):
        with self.lock:
            return self.is_observing, self.current_frame

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
        if self.cap:
            self.cap.release()
        self.face_mesh.close()
