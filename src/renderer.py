##import pygame
##import math
##import time
##from pathlib import Path
##
##class QuantumRenderer:
##    def __init__(self, width, height):
##        self.width = width
##        self.height = height
##        self.images = []
##        self.offsets = []
##        self.load_assets()
##
##    def load_assets(self):
##        """Carga y decodifica las imágenes WebP en la memoria RAM."""
##        assets_dir = Path("assets")
##        
##        # Crear el directorio si no existe para evitar bloqueos
##        if not assets_dir.exists():
##            assets_dir.mkdir()
##            print("Directorio 'assets' creado. Por favor, añade las imágenes WebP.")
##            
##        # Buscar todos los archivos .webp en la carpeta assets
##        image_files = list(assets_dir.glob("*.webp"))
##        
##        # Cargamos hasta un máximo de 6 imágenes
##        for i, file_path in enumerate(image_files[:6]):
##            try:
##                # convert_alpha() es crucial: optimiza la imagen para mezcla por hardware en Pygame
##                img = pygame.image.load(str(file_path)).convert_alpha()
##                img = pygame.transform.scale(img, (self.width, self.height))
##                self.images.append(img)
##                
##                # Asignamos un desfase temporal distinto (fase de la onda) a cada imagen
##                # math.pi / 3 distribuye equitativamente las 6 imágenes en el ciclo de la onda
##                self.offsets.append(i * (math.pi / 3)) 
##            except Exception as e:
##                print(f"Error cargando el archivo {file_path}: {e}")
##
##    def render_superposition(self, surface):
##        """Mezcla las imágenes con opacidades dinámicas y las proyecta en la superficie."""
##        # Fallback en caso de que la carpeta assets esté vacía
##        if not self.images:
##            surface.fill((15, 15, 15))
##            # Utilizando una fuente de corte contemporáneo y limpio para mantener la dirección de arte
##            font = pygame.font.SysFont("helvetica, arial", 42) 
##            text = font.render("AÑADIR 6 IMÁGENES WEBP EN /ASSETS", True, (120, 120, 120))
##            surface.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2))
##            return
##
##        current_time = time.time()
##        surface.fill((0, 0, 0)) # Fondo negro base para evitar estelas
##
##        for img, offset in zip(self.images, self.offsets):
##            # 1. Calculamos la onda: math.sin devuelve un valor entre -1.0 y 1.0
##            # 2. El multiplicador (ej. 1.2) controla la velocidad de la transición
##            # 3. Normalizamos el resultado para que oscile entre 0 y 255 (el canal alfa)
##            sine_value = math.sin(current_time * 1.2 + offset)
##            alpha_value = int(((sine_value + 1) / 2) * 255)
##            
##            # Aplicamos la opacidad a una copia temporal de la imagen para no modificar el original
##            temp_surface = img.copy()
##            temp_surface.set_alpha(alpha_value)
##            
##            # Mezclamos esta capa sobre la superficie principal (la pantalla)
##            surface.blit(temp_surface, (0, 0))
import pygame
import random
from pathlib import Path

class QuantumRenderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.images = []
        self.load_assets()

    def load_assets(self):
        """Carga y decodifica las imágenes WebP en la memoria RAM."""
        assets_dir = Path("assets")
        
        if not assets_dir.exists():
            assets_dir.mkdir()
            print("Directorio 'assets' creado. Por favor, añade las imágenes WebP.")
            
        image_files = list(assets_dir.glob("*.webp"))
        
        for file_path in image_files[:6]:
            try:
                img = pygame.image.load(str(file_path)).convert_alpha()
                img = pygame.transform.scale(img, (self.width, self.height))
                self.images.append(img)
            except Exception as e:
                print(f"Error cargando el archivo {file_path}: {e}")

    def render_superposition(self, surface):
        """Genera un estado de ruido cuántico con transiciones imperceptibles."""
        if not self.images:
            surface.fill((15, 15, 15))
            font = pygame.font.SysFont("helvetica, arial", 42) 
            text = font.render("AÑADIR 6 IMÁGENES WEBP EN /ASSETS", True, (120, 120, 120))
            surface.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2))
            return

        surface.fill((0, 0, 0))

        # Aleatorizamos el orden de renderizado en cada frame para maximizar el caos
        # y evitar que la misma imagen quede siempre arriba
        random.shuffle(self.images)

        for img in self.images:
            # Generamos una opacidad completamente aleatoria entre 0 y 255 por cada frame
            # Al correr a 60 FPS, esto crea un efecto de ruido visual extremo
            alpha_value = random.randint(0, 255)
            
            temp_surface = img.copy()
            temp_surface.set_alpha(alpha_value)
            
            surface.blit(temp_surface, (0, 0))
