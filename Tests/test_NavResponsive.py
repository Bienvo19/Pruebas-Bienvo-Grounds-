import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.edge.service import Service
import pytest


@pytest.fixture(scope="module")
def driver():
    service = Service('../EdgeWebDriver/msedgedriver.exe')
    driver = webdriver.Edge(service=service)
    yield driver
    driver.quit()


def test_navigation_responsive(driver):
    estado = "Éxito"
    descripcion = "Se realizó la prueba del navegador en modo responsive correctamente."
    try:
        
        driver.get("file:///C:/Proyecto Final/Bienvo Grounds/index.html")
        driver.maximize_window()

        
        driver.set_window_size(375, 812) 
        time.sleep(2)  

       
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshots_folder = os.path.join(os.getcwd(), "Screenshots")
        if not os.path.exists(screenshots_folder):
            os.makedirs(screenshots_folder)
        screenshot_filename = f"NavResponsive_{timestamp}.png"
        screenshot_path = os.path.join(screenshots_folder, screenshot_filename)
        driver.save_screenshot(screenshot_path)
        print(f"Captura de pantalla guardada en: {screenshot_path}")

    except Exception as e:
        estado = "Fallo"
        descripcion = f"Error durante la prueba: {str(e)}"
        print(descripcion)

    finally:
      
        reports_folder = os.path.join(os.getcwd(), "Reports")
        if not os.path.exists(reports_folder):
            os.makedirs(reports_folder)
        report_filename = f"NavResponsive_{timestamp}.html"
        report_html_path = os.path.join(reports_folder, report_filename)

        with open(report_html_path, "w", encoding="utf-8") as report_file:
            report_file.write(f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Reporte de Navegación Responsive</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body {{
                        font-family: 'Arial', sans-serif;
                        background-color: #f8f9fa;
                    }}
                    .container {{
                        max-width: 900px;
                        margin-top: 50px;
                    }}
                    h1 {{
                        color: #28a745;
                        text-transform: uppercase;
                        font-size: 2.5rem;
                    }}
                    .table {{
                        background-color: #fff;
                        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    }}
                    .table th {{
                        background-color: #343a40;
                        color: #fff;
                    }}
                    .table td {{
                        vertical-align: middle;
                    }}
                    .table img {{
                        border-radius: 5px;
                    }}
                    .alert {{
                        font-size: 1.25rem;
                        text-align: center;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1 class="text-center mb-4">Reporte de Navegación Responsive</h1>
                    <div class="alert { 'alert-success' if estado == 'Éxito' else 'alert-danger' }" role="alert">
                        <strong>{estado}</strong> - {descripcion}
                    </div>
                    <table class="table table-bordered table-striped">
                        <thead class="table-dark">
                            <tr>
                                <th scope="col">Fecha y Hora</th>
                                <th scope="col">Descripción</th>
                                <th scope="col">Estado</th>
                                <th scope="col">Captura</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{timestamp}</td>
                                <td>{descripcion}</td>
                                <td class="{'table-success' if estado == 'Éxito' else 'table-danger'}">{estado}</td>
                                <td>{'<img src="../Screenshots/' + screenshot_filename + '" alt="Captura de Navegación Responsive" class="img-fluid" width="300">' if estado == "Éxito" else "No disponible"}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </body>
            </html>
            """)

        print(f"Reporte generado en: {report_html_path}")
