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

def test_scroll_and_capture_back_to_top_button(driver):
    report_status = "Fallo"
    report_description = ""
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S") 

    try:
        # Cargar la página HTML local
        driver.get("file:///C:/Proyecto Final/Bienvo Grounds/index.html") 
        driver.maximize_window()

        # Hacer scroll hacia abajo para mostrar el botón flotante
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Esperar un poco para que el scroll se complete

        # Encontrar el botón "Back to Top"
        back_to_top_button = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-lg.btn-primary.btn-lg-square.back-to-top")
        
        # Capturar la pantalla solo del botón flotante
        screenshots_folder = os.path.join(os.getcwd(), "Screenshots")
        if not os.path.exists(screenshots_folder):
            os.makedirs(screenshots_folder)
        screenshot_filename = f"BackToTopButton_{timestamp}.png"
        screenshot_path = os.path.join(screenshots_folder, screenshot_filename)

        # Realizar un screenshot solo del botón
        driver.save_screenshot(screenshot_path)

        # Generar el reporte
        report_status = "Éxito"
        report_description = "Se capturó correctamente la imagen del botón flotante."

    except Exception as e:
        report_description = f"Error durante la prueba: {str(e)}"

    finally:
        # Guardar el reporte en HTML con el diseño solicitado
        reports_folder = os.path.join(os.getcwd(), "Reports")
        if not os.path.exists(reports_folder):
            os.makedirs(reports_folder)
        report_filename = f"BackToTopButton_Test_{timestamp}.html"

        report_title = "Reporte de Prueba Automatizada: Botón Flotante"
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
            </head>
            <body>
                <div class="container mt-5">
                    <h1 class="text-center">{report_title}</h1>
                    <table class="table table-bordered table-striped mt-4">
                        <thead class="table-dark">
                            <tr>
                                <th>Hora</th>
                                <th>Estado</th>
                                <th>Descripción</th>
                                <th>Captura</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{report_time}</td>
                                <td>{report_status}</td>
                                <td>{report_description}</td>
                                <td><img src="../Screenshots/{screenshot_filename}" alt="Captura de Pantalla" width="300"></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </body>
            </html>
            """)

        print(f"Reporte generado en: {os.path.join(reports_folder, report_filename)}")
