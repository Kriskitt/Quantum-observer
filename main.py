import pygame
import sys
import json
from pathlib import Path
from src.camera import CameraManager
from src.renderer import QuantumRenderer

def main():
    config_path = Path("config.json")
    if not config_path.exists():
        print("Error: config.json no encontrado.")
        sys.exit(1)
        
    with open(config_path, "r") as f:
        config = json.load(f)

    pygame.init()
    screen = pygame.display.set_mode((config["width"], config["height"]), pygame.FULLSCREEN)
    pygame.display.set_caption("El Observador - Estado Cuántico")
    clock = pygame.time.Clock()

    # Iniciar el módulo de renderizado visual
    renderer = QuantumRenderer(config["width"], config["height"])

    # Iniciar la cámara en segundo plano
    cam_manager = CameraManager(camera_index=config["camera_index"])
    cam_manager.start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        is_observing, frame = cam_manager.get_state()
        
        # Lógica central del estado cuántico
        if is_observing and frame is not None:
            # --- ESTADO 1: COLAPSO EN LA REALIDAD ---
            # Mostramos directamente lo que ve la cámara (el observador)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            frame_surface = pygame.transform.scale(frame_surface, (config["width"], config["height"]))
            screen.blit(frame_surface, (0, 0))
        else:
            # --- ESTADO 0: SUPERPOSICIÓN ---
            # El motor se encarga de calcular y mezclar las 6 imágenes
            renderer.render_superposition(screen)

        pygame.display.flip()
        clock.tick(config["fps"])

    cam_manager.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
