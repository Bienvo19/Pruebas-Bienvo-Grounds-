import time
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium import webdriver
import pytest


@pytest.fixture(scope="module")
def driver():
    service = Service('../EdgeWebDriver/msedgedriver.exe')  
    driver = webdriver.Edge(service=service)
    yield driver
    driver.quit()


def test_navigation_menu(driver):
    report_status = "Fallo"
    report_description = ""
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S") 

    # Lista para almacenar las rutas de las capturas
    screenshots_list = []

    try:
        # Cargar la página HTML local
        driver.get("file:///C:/Proyecto Final/Bienvo Grounds/index.html") 
        driver.maximize_window()

        # Esperar a que la página cargue completamente
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "nav.navbar")))

        # Capturar la pantalla inicial
        screenshots_folder = os.path.join(os.getcwd(), "Screenshots")
        if not os.path.exists(screenshots_folder):
            os.makedirs(screenshots_folder)
        screenshot_filename = f"Nav_Menu_{timestamp}_Home.png"
        screenshot_path = os.path.join(screenshots_folder, screenshot_filename)
        driver.save_screenshot(screenshot_path)

        # Añadir la captura inicial a la lista de capturas
        screenshots_list.append(screenshot_filename)

        # Generar el reporte de la pantalla inicial
        report_status = "Éxito"
        report_description = "Se cargó la página y se capturó la pantalla inicial."

        # Función para hacer scroll y capturar la pantalla de cada sección
        def navigate_and_capture(link_selector, section_name):
            # Hacer scroll hacia el enlace para que no quede cubierto por el nav
            link = driver.find_element(By.CSS_SELECTOR, link_selector)
            actions = ActionChains(driver)
            actions.move_to_element(link).perform()
            time.sleep(1)  # Esperar un poco para el scroll

            # Hacer clic en el enlace
            link.click()
            time.sleep(2)  # Esperar a que la sección se despliegue correctamente

            # Capturar la pantalla después de navegar
            screenshot_filename = f"Nav_Menu_{timestamp}_{section_name}.png"
            screenshot_path = os.path.join(screenshots_folder, screenshot_filename)
            driver.save_screenshot(screenshot_path)

            # Añadir la captura a la lista
            screenshots_list.append(screenshot_filename)
        
        # Navegar por las secciones del nav y capturar pantallas
        navigate_and_capture(".nav-item.nav-link.active", "Home")
        navigate_and_capture(".nav-item.nav-link[href='#about']", "About")
        navigate_and_capture(".nav-item.nav-link[href='#Service']", "Service")
        navigate_and_capture(".nav-item.nav-link[href='#Menu']", "Menu")
        navigate_and_capture(".nav-item.nav-link[href='#Reservation']", "Reservation")
        navigate_and_capture(".nav-item.nav-link[href='#Testimonial']", "Testimonial")

    except Exception as e:
        report_description = f"Error durante la prueba: {str(e)}"

    finally:
        # Guardar el reporte en HTML
        reports_folder = os.path.join(os.getcwd(), "Reports")
        if not os.path.exists(reports_folder):
            os.makedirs(reports_folder)
        report_filename = f"NavMenu_Test_{timestamp}.html"

        report_title = "Reporte de Prueba Automatizada: Navegación del Menú"
        report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Generar el reporte HTML
        with open(os.path.join(reports_folder, report_filename), "w", encoding="utf-8") as report_file:
            report_file.write(f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{report_title}</title>
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
                    <h1 class="text-center mb-4">{report_title}</h1>
                    <div class="alert { 'alert-success' if report_status == 'Éxito' else 'alert-danger' }" role="alert">
                        <strong>{report_status}</strong> - {report_description}
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
                                <td>{report_time}</td>
                                <td>{report_description}</td>
                                <td class="{'table-success' if report_status == 'Éxito' else 'table-danger'}">{report_status}</td>
                                <td>{'<img src="../Screenshots/' + screenshots_list[0] + '" alt="Captura de Navegación" class="img-fluid" width="300">' if report_status == "Éxito" else "No disponible"}</td>
                            </tr>
                        </tbody>
                    </table>
                    <h2 class="text-center mt-5">Capturas por Sección</h2>
                    <div class="row">
        """)

            # Agregar todas las capturas de pantalla tomadas
            for screenshot in screenshots_list:
                report_file.write(f"""
                    <div class="col-md-4 text-center mb-4">
                        <img src="../Screenshots/{screenshot}" alt="Captura" class="img-fluid" width="300">
                    </div>
                """)

            report_file.write(f"""
                    </div>
                </div>
            </body>
            </html>
            """)

        print(f"Reporte generado en: {os.path.join(reports_folder, report_filename)}")
