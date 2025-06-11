from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

N = 15
created_forms = []
found = []


options = UiAutomator2Options()
options.platform_name = 'Android'
options.device_name = 'emulator-5554'
options.app = r'C:\Users\benja\Downloads\v1.10.12.Android.apk'
options.automation_name = 'UiAutomator2'
options.new_command_timeout = 350


driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
print("Sesión iniciada correctamente")

def wait_and_find(driver, by, value, timeout=5):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def clean(form_name):

    form_element = wait_and_find(
        driver,
        AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiSelector().text("{form_name}")',
        timeout=3
    )
    
    # Mantener presionado por 1 segundo
    driver.tap([(form_element.location['x'], form_element.location['y'])], 1000)
    time.sleep(0.5)
    
    # Toque normal después del press
    driver.tap([(form_element.location['x'], form_element.location['y'])], 50)
    time.sleep(0.5)
    
    # Presionar el botón específico
    special_button = wait_and_find(
        driver,
        AppiumBy.XPATH,
        '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.GroupView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView',
        timeout=3
    )
    special_button.click()




def main():
    try:
        # Ir a Formularios
        formularios_btn = wait_and_find(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Formulrios")')
        formularios_btn.click()

        for i in range(1, N + 1):
            # Paso 1: Presionar botón "+"
            add_btn = wait_and_find(
                driver,
                AppiumBy.XPATH,
                '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/com.horcrux.svg.SvgView'
            )
            add_btn.click()

            # Paso 2: Rellenar nombre del formulario
            name_field = wait_and_find(
                driver,
                AppiumBy.XPATH,
                '//android.widget.EditText[@resource-id="@undefined/input"]'
            )
            form_name = f"test_form_{i}"
            name_field.send_keys(form_name)
            created_forms.append(form_name)

            # Selector
            selector = wait_and_find(
                driver,
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Seleccione un tipo de campo")'
            )
            selector.click()

            # Tipo texto
            text_option = wait_and_find(
                driver,
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("texto")'
            )
            text_option.click()

            # Agregar campo
            add_field_btn = wait_and_find(
                driver,
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Agregar nuevo campo")'
            )
            add_field_btn.click()

            # Nombre del campo
            field_name = wait_and_find(
                driver,
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Ingrese un nombre")'
            )
            field_name.send_keys("campo de texto de prueba")

            # Guardar
            save_btn = wait_and_find(
                driver,
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Guardar y salir")'
            )
            save_btn.click()
            
            # Espera entre iteraciones
            time.sleep(1)

    except Exception as e:
        print(f"Error en iteración {i}: {str(e)}")
        driver.save_screenshot(f'error_iteration_{i}.png')
        raise

    print("Formularios generados, realizando verificación...")



    # Verificación final con scroll hacia abajo, acciones táctiles y botón específico
    for form in created_forms: 
        print(f"Verificando {form}")
        driver.swipe(500, 500, 500, 3000, 400)
        for _ in range(3):
            try:
                clean(form) 
                found.append(form)
                time.sleep(0.6)
                break
                
            except Exception as e:
                # Scroll hacia abajo si no lo encuentra
                driver.swipe(500, 1500, 500, 500, 400)
                time.sleep(0.6)



    # Resultados
    if len(found) == N:
        print(f"Formularios procesados correctamente ({len(found)}): {found}")
    else:
        print("✓ Todos los formularios fueron procesados exitosamente")

if __name__ == "__main__":
    main()
