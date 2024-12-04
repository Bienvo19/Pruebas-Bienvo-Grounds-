import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import pytest

@pytest.fixture(scope="module")
def driver():
    service = Service('../EdgeWebDriver/msedgedriver.exe')  
    driver = webdriver.Edge(service=service)
    yield driver
    driver.quit()

def test_carousel_images(driver):
    report_status = "Fallo"
    report_description = ""
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S") 

    try:
        # Cargar la página HTML local
        driver.get("file:///C:/Proyecto Final/Bienvo Grounds/index.html") 
        driver.maximize_window()

        # Capturar la primera imagen del carrusel
        screenshot_folder = os.path.join(os.getcwd(), "Screenshots")
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)
        screenshot_filename_1 = f"Carousel_1_{timestamp}.png"
        screenshot_path_1 = os.path.join(screenshot_folder, screenshot_filename_1)
        driver.save_screenshot(screenshot_path_1)

        # Hacer clic en el siguiente botón para pasar a la siguiente imagen
        next_button = driver.find_element(By.CSS_SELECTOR, "a.carousel-control-next")
        next_button.click()

        # Esperar a que la segunda imagen se cargue
        time.sleep(2)

        # Capturar la segunda imagen del carrusel
        screenshot_filename_2 = f"Carousel_2_{timestamp}.png"
        screenshot_path_2 = os.path.join(screenshot_folder, screenshot_filename_2)
        driver.save_screenshot(screenshot_path_2)

        # Generar el reporte
        report_status = "Éxito"
        report_description = "Se capturaron correctamente las imágenes del carrusel."

    except Exception as e:
        report_description = f"Error durante la prueba: {str(e)}"

    finally:
        # Guardar el reporte en HTML con el diseño solicitado
        reports_folder = os.path.join(os.getcwd(), "Reports")
        if not os.path.exists(reports_folder):
            os.makedirs(reports_folder)
        report_filename = f"Carousel_Images_Test_{timestamp}.html"

        report_title = "Reporte de Prueba Automatizada: Carrusel de Imágenes"
        report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(os.path.join(reports_folder, report_filename), "w", encoding="utf-8") as report_file:
            report_file.write(f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{report_title}</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f8f9fa;
                    }}
                    h1 {{
                        color: #007bff;
                    }}
                    .table {{
                        background-color: #ffffff;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }}
                    .table th {{
                        background-color: #343a40;
                        color: #ffffff;
                    }}
                    .table td {{
                        vertical-align: middle;
                    }}
                    img {{
                        border-radius: 8px;
                    }}
                </style>
            </head>
            <body>
                <div class="container mt-5">
                    <h1 class="text-center">{report_title}</h1>
                    <table class="table table-bordered table-striped mt-4">
                        <thead>
                            <tr>
                                <th>Hora</th>
                                <th>Estado</th>
                                <th>Descripción</th>
                                <th>Captura 1</th>
                                <th>Captura 2</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{report_time}</td>
                                <td>{report_status}</td>
                                <td>{report_description}</td>
                                <td><img src="../Screenshots/{screenshot_filename_1}" alt="Captura de la primera imagen" width="300"></td>
                                <td><img src="../Screenshots/{screenshot_filename_2}" alt="Captura de la segunda imagen" width="300"></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </body>
            </html>
            """)

        print(f"Reporte generado en: {os.path.join(reports_folder, report_filename)}")
