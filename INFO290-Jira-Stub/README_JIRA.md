# Automated Testing Framework with Jira Integration

Este framework de pruebas automatizadas para aplicaciones móviles Android incluye integración automática con Jira para la creación de incidentes cuando fallan las pruebas.

## 🆕 Nuevas Características - Integración con Jira

- ✅ Pruebas automatizadas con Appium y Selenium
- 🐛 **Creación automática de incidentes en Jira al fallar pruebas**
- 📸 **Captura automática de screenshots en fallos**
- 📊 **Reporte detallado de datos de prueba**
- 🔧 Configuración flexible mediante variables de entorno

## Instalación

1. **Instalar dependencias adicionales:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno:**
   - Copia `.env.example` a `.env`
   - Añade las nuevas variables de Jira a tu archivo `.env`

## 🔧 Configuración de Jira (NUEVO)

### 1. Obtener API Token de Jira

1. Ve a [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Haz clic en **"Create API token"**
3. Dale un nombre descriptivo (ej: "Test Automation")
4. Copia el token generado

### 2. Añadir variables de entorno a tu `.env`

```env
# Jira Integration Configuration
JIRA_URL=https://tu-empresa.atlassian.net
JIRA_USERNAME=tu-email@empresa.com
JIRA_API_TOKEN=tu-api-token-aqui
JIRA_PROJECT_KEY=TEST
JIRA_ISSUE_TYPE=Bug

# Screenshot Configuration
ENABLE_SCREENSHOTS=true
SCREENSHOTS_DIR=screenshots

# Appium Configuration (nuevas opciones configurables)
DEVICE_NAME=emulator-5554
COMMAND_TIMEOUT=350
NO_RESET=false
FULL_RESET=false
```

## 🐛 Funcionalidad de Incidentes Automáticos

Cuando falla una prueba, el sistema automáticamente:

1. **Captura screenshot** del momento del fallo
2. **Recopila datos de prueba** (entrada, salida esperada, salida actual)
3. **Crea incidente en Jira** con:
   - Resumen descriptivo
   - Descripción detallada con stack trace
   - Datos de prueba en formato JSON
   - Screenshot adjunto
   - Etiquetas: `automated-test`, `test-failure`, `appium`

### Ejemplo de incidente creado:

**Resumen:** `[Automated Test Failure] Textbox Uppercase Test`

**Descripción incluye:**
- Detalles del error y stack trace
- Datos de prueba al momento del fallo
- Información del entorno (Android, emulador, etc.)
- Timestamp del fallo

## 📊 Captura de Datos de Prueba

Los tests ahora pueden capturar datos relevantes usando:

```python
# En tu test
self.capture_test_data('current_input', 'texto_de_prueba')
self.capture_test_data('expected_output', 'TEXTO_DE_PRUEBA')
self.capture_test_data('actual_output', resultado_obtenido)

# Tomar screenshot con descripción
screenshot_path = self.take_screenshot('error_en_validacion')
```

## 🚀 Mejoras en el Framework

### Variables de entorno configurables:
- `DEVICE_NAME`: Nombre del dispositivo/emulador
- `COMMAND_TIMEOUT`: Timeout para comandos de Appium
- `NO_RESET`: Si mantener el estado de la app entre pruebas
- `FULL_RESET`: Si hacer reset completo de la app

### Mejor manejo de errores:
- Captura de datos en cada fase (setup, run, teardown)
- Screenshots automáticos en fallos
- Información detallada para debugging

---

## Documentación Original

### Crear y ejecutar pruebas:
En la ultima versión, main.py permite ejecutar pruebas paso a paso, permitiendo desacoplar la iniciación del socket de las pruebas en si.
Para escribir una prueba, se debe escribir una clase que implemente los métodos definidos en la interfaz de [casos de prueba](https://github.com/BladerKholin/Proyecto-INFO282-Sistema-de-registro-de-visitas/blob/prod/INFO290-docs/app_tester/TestCases/TestCaseInterface.py) (run, setup y teardown, entre otros) y agregarlo al arreglo de casos de pruebas del main.py.

Respecto a las configuraciones de entorno, se proporciona un archivo de configuración .env para facilitar su uso.

**Pruebas actuales:**
- **Prueba 1:** [No funcional - Se pueden crear al menos 15 formularios](https://github.com/BladerKholin/Proyecto-INFO282-Sistema-de-registro-de-visitas/blob/prod/INFO290-docs/app_tester/old/crear_formularios.py)
- **Prueba 2:** [Funcional - Se colocan los textos en mayúsculas con el filtro activado](https://github.com/BladerKholin/Proyecto-INFO282-Sistema-de-registro-de-visitas/blob/prod/INFO290-docs/app_tester/TestCases/TestTextboxMayus/TestTexboxMayus.py)

Para ejecutar:
```powershell
python main.py
```

### Instalación y configuración para pruebas automatizadas con Appium

#### 1. Instalar Android SDK (con Java)
- Descargar e instalar el Android SDK desde [Android Studio](https://developer.android.com/studio)
- Configurar las variables de entorno `ANDROID_HOME` y `ANDROID_SDK_ROOT`

#### 2. Ejecutar el emulador de Android
```powershell
& "$env:LOCALAPPDATA\Android\Sdk\emulator\emulator.exe" -avd Formulapp_Test -dns-server 8.8.8.8
```

#### 3. Iniciar el servidor de Appium
```powershell
npx appium --use-drivers=uiautomator2
```
