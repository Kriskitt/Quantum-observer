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
        """Carga y ajusta imágenes en ratio original"""
        assets_dir = Path("assets")
        
        if not assets_dir.exists():
            assets_dir.mkdir()
            print("Directorio 'assets' creado. Por favor, añade las imágenes WebP.")
            
        image_files = list(assets_dir.glob("*.webp"))
        
        for file_path in image_files[:12]:
            try:
                # load img og
                img = pygame.image.load(str(file_path)).convert_alpha()
                orig_width, orig_height = img.get_size()
                
                # calcular el factor de escala para X e Y
                ratio_x = self.width / orig_width
                ratio_y = self.height / orig_height
                
                # calcular ratio
                ratio = min(ratio_x, ratio_y)
                
                new_width = int(orig_width * ratio)
                new_height = int(orig_height * ratio)
                
                # antialising
                img_scaled = pygame.transform.smoothscale(img, (new_width, new_height))
                
                # black canvas (1920x1080)
                final_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                
                # Calcular coordenadas exactas para centrar la imagen en el lienzo
                x_pos = (self.width - new_width) // 2
                y_pos = (self.height - new_height) // 2
                
                # dibujar en el centro del lienzo
                final_surface.blit(img_scaled, (x_pos, y_pos))
                
                self.images.append(final_surface)
                
            except Exception as e:
                print(f"Error cargando el archivo {file_path}: {e}")


    def render_superposition(self, surface):
        """genera un estado de ruido cuántico."""
        if not self.images:
            surface.fill((15, 15, 15))
            font = pygame.font.SysFont("helvetica, arial", 42) 
            text = font.render("AÑADIR 6 IMÁGENES WEBP EN /ASSETS", True, (120, 120, 120))
            surface.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2))
            return

        surface.fill((0, 0, 0))

        # aleatorio
        random.shuffle(self.images)

        for img in self.images:
            alpha_value = random.randint(0, 255)
            
            temp_surface = img.copy()
            temp_surface.set_alpha(alpha_value)
            
            surface.blit(temp_surface, (0, 0))
