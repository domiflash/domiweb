#!/usr/bin/env python3
"""
ANÁLISIS COMPLETO DEL PROYECTO DOMIWEB
=====================================

Este script analiza todos los módulos, rutas y funcionalidades
del proyecto DomiFlash sin necesidad de ejecutar el servidor.
"""

import os
import sys
import ast
import re
from pathlib import Path

class DomiWebAnalyzer:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.analysis_results = {
            'estructura': {},
            'rutas': {},
            'errores': [],
            'recomendaciones': [],
            'estadisticas': {}
        }
    
    def analyze_project_structure(self):
        """Analiza la estructura del proyecto"""
        print("🔍 ANALIZANDO ESTRUCTURA DEL PROYECTO...")
        
        structure = {}
        for root, dirs, files in os.walk(self.project_path):
            # Excluir directorios innecesarios
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'venv', 'flask_session', '.env']]
            
            rel_path = os.path.relpath(root, self.project_path)
            if rel_path == '.':
                rel_path = 'root'
            
            structure[rel_path] = {
                'directories': dirs,
                'files': [f for f in files if not f.endswith('.pyc')]
            }
        
        self.analysis_results['estructura'] = structure
        return structure
    
    def analyze_routes(self):
        """Analiza todas las rutas definidas en los blueprints"""
        print("🛣️ ANALIZANDO RUTAS...")
        
        routes_dir = self.project_path / 'routes'
        routes_analysis = {}
        
        for py_file in routes_dir.glob('*.py'):
            if py_file.name == '__init__.py':
                continue
                
            module_name = py_file.stem
            routes_analysis[module_name] = self.analyze_single_route_file(py_file)
        
        self.analysis_results['rutas'] = routes_analysis
        return routes_analysis
    
    def analyze_single_route_file(self, file_path):
        """Analiza un archivo de rutas específico"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parsear AST para extraer información
            tree = ast.parse(content)
            
            routes = []
            imports = []
            functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Buscar decoradores de ruta
                    route_info = self.extract_route_info(node)
                    if route_info:
                        routes.append(route_info)
                    functions.append(node.name)
                
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    imports.append(ast.unparse(node))
            
            return {
                'file': str(file_path),
                'routes': routes,
                'functions': functions,
                'imports': imports,
                'total_routes': len(routes),
                'total_functions': len(functions)
            }
        
        except Exception as e:
            self.analysis_results['errores'].append(f"Error analizando {file_path}: {str(e)}")
            return {'error': str(e)}
    
    def extract_route_info(self, func_node):
        """Extrae información de rutas de un nodo de función"""
        route_info = {
            'function_name': func_node.name,
            'decorators': [],
            'route_path': None,
            'methods': ['GET'],  # Default
            'requires_auth': False,
            'required_role': None
        }
        
        for decorator in func_node.decorator_list:
            if isinstance(decorator, ast.Attribute):
                # Ejemplo: @cliente_bp.route("/menu")
                if hasattr(decorator.value, 'id') and decorator.attr == 'route':
                    route_info['decorators'].append(f"{decorator.value.id}.route")
                    # Extraer path de los argumentos
                    if func_node.decorator_list:
                        for dec in func_node.decorator_list:
                            if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                                if dec.func.attr == 'route' and dec.args:
                                    if isinstance(dec.args[0], ast.Constant):
                                        route_info['route_path'] = dec.args[0].value
                                    # Buscar methods en keywords
                                    for keyword in dec.keywords:
                                        if keyword.arg == 'methods' and isinstance(keyword.value, ast.List):
                                            route_info['methods'] = [el.value for el in keyword.value.elts if isinstance(el, ast.Constant)]
            
            elif isinstance(decorator, ast.Name):
                # Ejemplo: @login_required
                if decorator.id == 'login_required':
                    route_info['requires_auth'] = True
                    route_info['decorators'].append('login_required')
            
            elif isinstance(decorator, ast.Call):
                # Ejemplo: @role_required("cliente")
                if isinstance(decorator.func, ast.Name) and decorator.func.id == 'role_required':
                    route_info['requires_auth'] = True
                    if decorator.args and isinstance(decorator.args[0], ast.Constant):
                        route_info['required_role'] = decorator.args[0].value
                    route_info['decorators'].append(f"role_required({route_info['required_role']})")
        
        # Solo retornar si realmente es una ruta
        if route_info['route_path']:
            return route_info
        return None
    
    def analyze_database_usage(self):
        """Analiza el uso de la base de datos"""
        print("🗄️ ANALIZANDO USO DE BASE DE DATOS...")
        
        db_analysis = {
            'stored_procedures': [],
            'direct_queries': [],
            'tables_used': set()
        }
        
        # Buscar en todos los archivos Python
        for py_file in self.project_path.rglob('*.py'):
            if 'venv' in str(py_file) or '__pycache__' in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Buscar procedimientos almacenados
                sp_matches = re.findall(r'callproc\s*\(\s*["\']([^"\']+)["\']', content)
                db_analysis['stored_procedures'].extend(sp_matches)
                
                # Buscar consultas directas
                query_matches = re.findall(r'execute\s*\(\s*["\']([^"\']+)["\']', content)
                db_analysis['direct_queries'].extend(query_matches)
                
                # Buscar nombres de tablas
                table_matches = re.findall(r'FROM\s+(\w+)|JOIN\s+(\w+)|UPDATE\s+(\w+)|INSERT\s+INTO\s+(\w+)', content, re.IGNORECASE)
                for match in table_matches:
                    for table in match:
                        if table:
                            db_analysis['tables_used'].add(table)
            
            except Exception:
                continue
        
        db_analysis['tables_used'] = list(db_analysis['tables_used'])
        self.analysis_results['database'] = db_analysis
        return db_analysis
    
    def check_security_issues(self):
        """Busca potenciales problemas de seguridad"""
        print("🔒 ANALIZANDO SEGURIDAD...")
        
        security_issues = []
        
        for py_file in self.project_path.rglob('*.py'):
            if 'venv' in str(py_file) or '__pycache__' in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Buscar problemas potenciales
                if 'password' in content.lower() and 'hash' not in content.lower():
                    security_issues.append(f"Posible manejo inseguro de contraseñas en {py_file}")
                
                if re.search(r'execute\s*\(\s*["\'][^"\']*%s', content):
                    # Esto es OK, pero verificar si hay concatenación directa
                    if re.search(r'execute\s*\(\s*["\'][^"\']*\+', content):
                        security_issues.append(f"Posible SQL injection en {py_file}")
                
                if 'SECRET_KEY' in content and 'fallback' in content:
                    security_issues.append(f"Clave secreta insegura en {py_file}")
            
            except Exception:
                continue
        
        self.analysis_results['security'] = security_issues
        return security_issues
    
    def generate_recommendations(self):
        """Genera recomendaciones basadas en el análisis"""
        print("💡 GENERANDO RECOMENDACIONES...")
        
        recommendations = []
        
        # Basado en rutas
        total_routes = sum(
            module_info.get('total_routes', 0) 
            for module_info in self.analysis_results['rutas'].values()
            if isinstance(module_info, dict)
        )
        
        if total_routes < 10:
            recommendations.append("Considerar agregar más funcionalidades al sistema")
        
        # Basado en seguridad
        if self.analysis_results.get('security'):
            recommendations.append("Revisar y corregir problemas de seguridad identificados")
        
        # Basado en estructura
        if 'tests' not in self.analysis_results['estructura']:
            recommendations.append("Agregar tests automatizados al proyecto")
        
        recommendations.extend([
            "Implementar logging más detallado",
            "Agregar validación de datos en formularios",
            "Considerar implementar cache para consultas frecuentes",
            "Documentar APIs con Swagger/OpenAPI",
            "Implementar rate limiting para APIs",
            "Agregar monitoreo de performance"
        ])
        
        self.analysis_results['recomendaciones'] = recommendations
        return recommendations
    
    def calculate_statistics(self):
        """Calcula estadísticas del proyecto"""
        print("📊 CALCULANDO ESTADÍSTICAS...")
        
        stats = {
            'total_files': 0,
            'python_files': 0,
            'html_files': 0,
            'css_files': 0,
            'js_files': 0,
            'total_routes': 0,
            'total_functions': 0,
            'lines_of_code': 0
        }
        
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'venv', 'flask_session']]
            
            for file in files:
                if file.endswith('.pyc'):
                    continue
                
                stats['total_files'] += 1
                file_path = os.path.join(root, file)
                
                if file.endswith('.py'):
                    stats['python_files'] += 1
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            stats['lines_of_code'] += len(f.readlines())
                    except:
                        pass
                elif file.endswith('.html'):
                    stats['html_files'] += 1
                elif file.endswith('.css'):
                    stats['css_files'] += 1
                elif file.endswith('.js'):
                    stats['js_files'] += 1
        
        # Estadísticas de rutas
        for module_info in self.analysis_results['rutas'].values():
            if isinstance(module_info, dict):
                stats['total_routes'] += module_info.get('total_routes', 0)
                stats['total_functions'] += module_info.get('total_functions', 0)
        
        self.analysis_results['estadisticas'] = stats
        return stats
    
    def run_complete_analysis(self):
        """Ejecuta análisis completo"""
        print("🚀 INICIANDO ANÁLISIS COMPLETO DE DOMIWEB")
        print("=" * 50)
        
        # Ejecutar todos los análisis
        self.analyze_project_structure()
        self.analyze_routes()
        self.analyze_database_usage()
        self.check_security_issues()
        self.calculate_statistics()
        self.generate_recommendations()
        
        return self.analysis_results
    
    def print_results(self):
        """Imprime resultados del análisis"""
        results = self.analysis_results
        
        print("\n📈 ESTADÍSTICAS DEL PROYECTO")
        print("-" * 30)
        stats = results['estadisticas']
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        print("\n🛣️ RUTAS POR MÓDULO")
        print("-" * 30)
        for module, info in results['rutas'].items():
            if isinstance(info, dict) and 'routes' in info:
                print(f"\n{module.upper()}:")
                for route in info['routes']:
                    auth_info = ""
                    if route['requires_auth']:
                        auth_info = f" [AUTH: {route.get('required_role', 'any')}]"
                    methods = ', '.join(route['methods'])
                    print(f"  {methods}: {route['route_path']} -> {route['function_name']}{auth_info}")
        
        print("\n🗄️ USO DE BASE DE DATOS")
        print("-" * 30)
        db_info = results.get('database', {})
        print(f"Procedimientos almacenados usados: {len(set(db_info.get('stored_procedures', [])))}")
        print(f"Consultas directas: {len(db_info.get('direct_queries', []))}")
        print(f"Tablas identificadas: {', '.join(db_info.get('tables_used', []))}")
        
        if results.get('security'):
            print("\n🔒 PROBLEMAS DE SEGURIDAD")
            print("-" * 30)
            for issue in results['security']:
                print(f"⚠️ {issue}")
        
        print("\n💡 RECOMENDACIONES")
        print("-" * 30)
        for i, rec in enumerate(results['recomendaciones'], 1):
            print(f"{i}. {rec}")
        
        if results['errores']:
            print("\n❌ ERRORES ENCONTRADOS")
            print("-" * 30)
            for error in results['errores']:
                print(f"❌ {error}")

def main():
    """Función principal"""
    project_path = os.getcwd()
    
    analyzer = DomiWebAnalyzer(project_path)
    analyzer.run_complete_analysis()
    analyzer.print_results()
    
    print("\n✅ ANÁLISIS COMPLETADO")
    print("=" * 50)

if __name__ == "__main__":
    main()