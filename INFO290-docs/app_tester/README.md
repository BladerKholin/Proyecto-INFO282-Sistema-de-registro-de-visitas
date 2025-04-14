### Crear y ejecutar pruebas:
En la ultima version, main.py permite ejecutar pruebas paso a paso, permitiendo desacoplar la iniciación del socket de las pruebas en si.
Para escribir una prueba, se debe escribir una clase que implemente los metodos definidos en la interfaz de [casos de prueba](https://github.com/BladerKholin/Proyecto-INFO282-Sistema-de-registro-de-visitas/blob/prod/INFO290-docs/app_tester/TestCases/TestCaseInterface.py) (run, setup y teardown, entre otros) y agregarlo al arreglo de casos de pruebas del main.py.

Respecto a las configuraciónes de entorno, se proporciona un archivo de configuración .env para facilitar su uso.

Actualmente, hay dos pruebas automatizadas, siendo la segunda la que usa las mejoras descritas.</br>
- **Prueba 1:** [No funcional - Se pueden crear al menos 15 formularios](https://github.com/BladerKholin/Proyecto-INFO282-Sistema-de-registro-de-visitas/blob/prod/INFO290-docs/app_tester/old/crear_formularios.py)</br>
- **Prueba 2:** [Funcional - Se colocan los textos en mayusculas con el filtro activado](https://github.com/BladerKholin/Proyecto-INFO282-Sistema-de-registro-de-visitas/blob/prod/INFO290-docs/app_tester/TestCases/TestTextboxMayus/TestTexboxMayus.py)</br>
El primer caso se debe ejecutar independientemente, ya que no usa el nuevo software, un ejemplo de esta ejecución se encuentra visible en [este enlace.](https://drive.google.com/file/d/1PRabIMa2BzyQrrGjBSVxp2GSw2kpmQFG/view?usp=sharing)

Para ejecutar, simplemente ejecutar main.py desde la carpeta app_tester como se muestra a continuación.
```powershell
python main.py
```

-------------------------------------------------------------------------------------------------------------------------------------

El resto del readme sirve para entender los requisitos previos a la ejecucion de las pruebas sin necesidad de un dispositivo externo.

### Instalación y configuración para pruebas automatizadas con Appium

#### 1. Instalar Android SDK (con Java)
Antes de comenzar, asegúrate de tener instalado el Android SDK y configurado correctamente en tu sistema. Esto incluye:

- Descargar e instalar el Android SDK desde [Android Studio](https://developer.android.com/studio).
- Configurar las variables de entorno `ANDROID_HOME` y `ANDROID_SDK_ROOT` para que apunten a la ubicación del SDK en tu sistema.

#### 2. Ejecutar el emulador de Android
Para iniciar un emulador de Android, utiliza el siguiente comando en PowerShell. Este comando ejecuta un emulador específico llamado `Formulapp_Test` y configura un servidor DNS personalizado:

```powershell
& "$env:LOCALAPPDATA\Android\Sdk\emulator\emulator.exe" -avd Formulapp_Test -dns-server 8.8.8.8
```

**Nota:** Asegúrate de que el emulador `Formulapp_Test` esté configurado previamente en el Android Virtual Device (AVD) Manager.

#### 3. Iniciar el servidor de Appium
Appium es el servidor que se conecta al emulador y permite ejecutar pruebas automatizadas. Para iniciarlo, usa el siguiente comando:

```powershell
npx appium --use-drivers=uiautomator2
```

**Nota:** Este comando asume que tienes Appium instalado globalmente o que estás utilizando `npx` para ejecutarlo directamente desde tu proyecto.

#### 4. Programa de prueba para automatizar una aplicación Android (comprobación opcional)
El siguiente script de ejemplo de Python utiliza Appium para conectarse al emulador y realizar pruebas automatizadas en una aplicación Android. Deben ajustarse las rutas y configuraciones según su entorno.

```python
from appium import webdriver
from appium.options.android import UiAutomator2Options
import os

# Verifica variables de entorno (para debugging)
print(f"ANDROID_HOME: {os.getenv('ANDROID_HOME')}")
print(f"ANDROID_SDK_ROOT: {os.getenv('ANDROID_SDK_ROOT')}")

# Configuración de Appium
options = UiAutomator2Options()
options.platform_name = 'Android'
options.device_name = 'emulator-5554'  # Usa el mismo nombre que aparece en 'adb devices'
options.app = r'C:\Users\benja\Downloads\v1.10.12.Android.apk'  # Ruta ABSOLUTA al APK
options.automation_name = 'UiAutomator2'
options.new_command_timeout = 300  # Timeout extendido para comandos

try:
    # Conexión al servidor de Appium
    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4723',  # Dirección del servidor Appium
        options=options
    )
    print(f"Sesión iniciada correctamente en dispositivo: {driver.capabilities['deviceName']}")

    # Aquí puedes agregar la lógica de tus pruebas automatizadas
    # Ejemplo: driver.find_element(...).click()

except Exception as e:
    print(f"Error al conectar con Appium: {str(e)}")
    raise
finally:
    # Cierra la sesión de Appium si fue iniciada
    if 'driver' in locals():
        driver.quit()
```

#### Notas adicionales:
- **Ruta del APK:** Asegúrate de proporcionar la ruta absoluta al archivo APK que deseas probar.
- **Emulador:** El nombre del dispositivo (`emulator-5554`) debe coincidir con el que aparece al ejecutar `adb devices`.
- **Depuración:** Si encuentras problemas, verifica que las variables de entorno `ANDROID_HOME` y `ANDROID_SDK_ROOT` estén configuradas correctamente.

Con estas instrucciones, deberías poder configurar y ejecutar pruebas automatizadas en tu aplicación Android utilizando Appium.
