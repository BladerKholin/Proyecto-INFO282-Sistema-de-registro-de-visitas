"""
Script de ejemplo para probar la integración con Jira
Ejecuta este script para verificar que la configuración de Jira esté correcta
"""
import os
from dotenv import load_dotenv
from jira_integration import JiraIntegration

load_dotenv()

def test_jira_configuration():
    """Prueba la configuración de Jira"""
    print("🔧 Probando configuración de Jira...")
    
    jira = JiraIntegration()
    
    if not jira.enabled:
        print("❌ Jira no está configurado correctamente.")
        print("Verifica las siguientes variables de entorno en tu archivo .env:")
        print("- JIRA_URL")
        print("- JIRA_USERNAME") 
        print("- JIRA_API_TOKEN")
        print("- JIRA_PROJECT_KEY")
        return False
    
    print("✅ Configuración de Jira válida")
    print(f"📍 URL: {jira.jira_url}")
    print(f"👤 Usuario: {jira.jira_username}")
    print(f"📋 Proyecto: {jira.jira_project_key}")
    
    return True

def create_test_issue():
    """Crea un incidente de prueba en Jira"""
    print("\n🧪 Creando incidente de prueba...")
    
    jira = JiraIntegration()
    
    if not jira.enabled:
        print("❌ Jira no está habilitado")
        return None
    
    # Datos de ejemplo de una prueba fallida
    test_data = {
        "test_iteration": 3,
        "input_text": "ejemplo de texto",
        "expected_output": "EJEMPLO DE TEXTO",
        "actual_output": "ejemplo de texto",
        "failure_stage": "execution",
        "error_type": "AssertionError"
    }
    
    error_details = """AssertionError: El texto no se convirtió a mayúsculas
    Expected: EJEMPLO DE TEXTO
    Actual: ejemplo de texto
    
    Stacktrace:
    File "test_example.py", line 45, in run
        assert actual_text == expected_text
    AssertionError: El texto no se convirtió a mayúsculas"""
    
    issue_key = jira.create_test_failure_issue(
        test_name="Test de Prueba - Integración Jira",
        test_description="Este es un incidente de prueba creado automáticamente para verificar la integración con Jira",
        error_details=error_details,
        test_data=test_data,
        screenshot_path=None  # No hay screenshot en este ejemplo
    )
    
    if issue_key:
        print(f"✅ Incidente creado exitosamente: {issue_key}")
        print(f"🔗 Ver en: {jira.jira_url}/browse/{issue_key}")
        
        # Agregar un comentario de prueba
        print("\n💬 Agregando comentario de prueba...")
        success = jira.add_comment_to_issue(
            issue_key, 
            "Este es un comentario de prueba agregado automáticamente para verificar la funcionalidad."
        )
        
        if success:
            print("✅ Comentario agregado exitosamente")
        
        return issue_key
    else:
        print("❌ Error al crear el incidente de prueba")
        return None

def main():
    """Función principal"""
    print("🚀 Iniciando prueba de integración con Jira\n")
    
    # Probar configuración
    if not test_jira_configuration():
        print("\n❌ Configuración incorrecta. Revisa tu archivo .env")
        return
    
    # Preguntar si crear incidente de prueba
    response = input("\n¿Deseas crear un incidente de prueba en Jira? (y/n): ").lower().strip()
    
    if response == 'y' or response == 'yes':
        issue_key = create_test_issue()
        if issue_key:
            print(f"\n🎉 Integración con Jira funcionando correctamente!")
            print(f"📋 Incidente creado: {issue_key}")
            print(f"⚠️  Recuerda eliminar este incidente de prueba si no lo necesitas")
    else:
        print("\n✅ Configuración válida. La integración está lista para usar.")
    
    print("\n🏁 Prueba completada")

if __name__ == "__main__":
    main()
