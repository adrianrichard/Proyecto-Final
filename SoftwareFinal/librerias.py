import os
import ast
import pkg_resources

def get_imports_from_file(filepath):
    """Extrae los módulos importados de un archivo .py usando AST."""
    with open(filepath, "r", encoding="utf-8") as file:
        node = ast.parse(file.read(), filename=filepath)
    
    imports = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            for alias in n.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(n, ast.ImportFrom):
            if n.module:
                imports.add(n.module.split(".")[0])
    return imports

def get_all_imports_from_project(root_path):
    """Busca en todos los archivos .py del proyecto."""
    all_imports = set()
    for root, _, files in os.walk(root_path):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    imports = get_imports_from_file(filepath)
                    all_imports.update(imports)
                except Exception as e:
                    print(f"⚠️ Error analizando {filepath}: {e}")
    return all_imports

def show_versions(imports):
    """Muestra la versión de cada librería si está instalada."""
    installed = {dist.project_name.lower(): dist.version for dist in pkg_resources.working_set}
    
    for lib in sorted(imports):
        if lib.lower() in installed:
            print(f"{lib} == {installed[lib.lower()]}")
        else:
            print(f"{lib} (no instalada o parte de la librería estándar)")

if __name__ == "__main__":
    ruta_proyecto = os.path.dirname(os.path.abspath(__file__))  # Directorio actual
    imports = get_all_imports_from_project(ruta_proyecto)
    print("\n📦 Librerías detectadas en el proyecto:\n")
    show_versions(imports)
