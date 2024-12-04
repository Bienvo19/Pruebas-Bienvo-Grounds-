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

def test_special_offer_section(driver):
    report_status = "Fallo"
    report_description = ""
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S") 

    try:
        # Cargar la página HTML local
        driver.get("file:///C:/Proyecto Final/Bienvo Grounds/index.html") 
        driver.maximize_window()

        # Realizar scroll hasta la sección de oferta
        offer_section = driver.find_element(By.CSS_SELECTOR, ".offer.container-fluid.my-5.py-5.text-center")
        driver.execute_script("arguments[0].scrollIntoView(true);", offer_section)

        # Esperar un poco para asegurar que la sección esté visible
        time.sleep(2)

        # Capturar la pantalla de la sección de oferta
        screenshot_folder = os.path.join(os.getcwd(), "Screenshots")
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)
        screenshot_filename = f"Special_Offer_{timestamp}.png"
        screenshot_path = os.path.join(screenshot_folder, screenshot_filename)
        driver.save_screenshot(screenshot_path)

        # Generar el reporte
        report_status = "Éxito"
        report_description = "Se capturó correctamente la sección de oferta especial."

    except Exception as e:
        report_description = f"Error durante la prueba: {str(e)}"

    finally:
        # Guardar el reporte en HTML con el diseño solicitado
        reports_folder = os.path.join(os.getcwd(), "Reports")
        if not os.path.exists(reports_folder):
            os.makedirs(reports_folder)
        report_filename = f"Special_Offer_Test_{timestamp}.html"

        report_title = "Reporte de Prueba Automatizada: Oferta Especial"
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
                                <th>Captura</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{report_time}</td>
                                <td>{report_status}</td>
                                <td>{report_description}</td>
                                <td><img src="../Screenshots/{screenshot_filename}" alt="Captura de la oferta especial" width="300"></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </body>
            </html>
            """)

        print(f"Reporte generado en: {os.path.join(reports_folder, report_filename)}")
