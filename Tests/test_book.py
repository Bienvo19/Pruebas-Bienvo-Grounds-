import time
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.edge.service import Service
import pytest


@pytest.fixture(scope="module")
def driver():
    service = Service('../EdgeWebDriver/msedgedriver.exe')
    driver = webdriver.Edge(service=service)
    yield driver
    driver.quit()


def test_form_submission(driver):
    report_status = "Fallo"
    report_description = ""
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    try:
        # Cargar la página HTML local
        driver.get("file:///C:/Proyecto Final/Bienvo Grounds/index.html")
        driver.maximize_window()

        # Hacer scroll hasta el formulario
        form_element = driver.find_element(By.CSS_SELECTOR, "form.mb-5")
        driver.execute_script("arguments[0].scrollIntoView(true);", form_element)
        time.sleep(1)  # Esperar un poco para asegurar que el formulario esté visible

        # Capturar la pantalla antes de completar el formulario
        screenshots_folder = os.path.join(os.getcwd(), "Screenshots")
        if not os.path.exists(screenshots_folder):
            os.makedirs(screenshots_folder)
        screenshot_filename = f"Form_Before_{timestamp}.png"
        screenshot_path = os.path.join(screenshots_folder, screenshot_filename)
        driver.save_screenshot(screenshot_path)

        # Completar los campos del formulario
        name_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Name']")
        email_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Email']")
        date_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Date']")
        time_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Time']")
        select_input = driver.find_element(By.CSS_SELECTOR, "select.custom-select")

        # Rellenar los campos
        name_input.send_keys("John Doe")
        email_input.send_keys("john.doe@example.com")
        date_input.send_keys("2024-12-10")
        time_input.send_keys("14:00")
        select_input.send_keys(Keys.DOWN)  # Seleccionar "Person 1"

        # Capturar la pantalla después de completar el formulario
        screenshot_filename = f"Form_After_{timestamp}.png"
        screenshot_path = os.path.join(screenshots_folder, screenshot_filename)
        driver.save_screenshot(screenshot_path)

        # Hacer clic en el botón de enviar
        submit_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
        submit_button.click()

        # Capturar la pantalla después de hacer clic en el botón "Book Now"
        time.sleep(1)  # Esperar un poco después de hacer clic
        screenshot_filename = f"Form_Submitted_{timestamp}.png"
        screenshot_path = os.path.join(screenshots_folder, screenshot_filename)
        driver.save_screenshot(screenshot_path)

        # Generar el reporte
        report_status = "Éxito"
        report_description = "Formulario completado y enviado correctamente."

    except Exception as e:
        report_description = f"Error durante la prueba: {str(e)}"

    finally:
        # Guardar el reporte en HTML
        reports_folder = os.path.join(os.getcwd(), "Reports")
        if not os.path.exists(reports_folder):
            os.makedirs(reports_folder)
        report_filename = f"Form_Test_{timestamp}.html"

        report_title = "Reporte de Prueba Automatizada: Formulario"
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
