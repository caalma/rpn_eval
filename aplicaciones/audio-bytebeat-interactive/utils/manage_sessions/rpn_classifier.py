#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from collections import defaultdict

class RPNClassifier:
    def __init__(self):
        # Definición de patrones estructurales con regex
        self.patterns = [
            # Ordenados de más específico a menos específico

            # t [const] &
            {'name': 'Bitmask', 'regex': r'\b\d+\s+t\s+&\b'},

            # t [const] %
            {'name': 'ModPeriod', 'regex': r'\bt\s+\d+\s+%\b'},

            # [value] [const] >>
            {'name': 'BitShift', 'regex': r'\b\d+\s+>>\b'},

            # [const] * [const] +
            {'name': 'LinearScale', 'regex': r'\d+\s+\*\s+\d+\s+\+'},

            # t [const] % pick
            {'name': 'ValueSelect', 'regex': r'\bt\s+\d+\s+% pick\b'},

            # Combinación aritmética
            {'name': 'ArithCombine', 'regex': r'[\+\-\*]\s+\d+\s+[\+\-\*]'},

            # >> [const] >>
            {'name': 'ShiftChain', 'regex': r'(>>\s+\d+\s+>>)'},

            # Operación bitwise seguida de shift
            {'name': 'BitArith', 'regex': r'[&|^]\s+\d+\s+>>'},

            # dup [const] t
            {'name': 'DupReuse', 'regex': r'dup\s+\d+\s+t'},

            # t [const] % ... >>
            {'name': 'ModShift', 'regex': r'\bt\s+\d+\s+%.*?>>'},

            # swap o pick
            {'name': 'StackOps', 'regex': r'(swap|pick)\b'},

            # Funciones trigonométricas
            {'name': 'TrigFunc', 'regex': r'\b(sin|cos|tan)\b'},

            # Operaciones condicionales
            {'name': 'Conditional', 'regex': r'\d+\s+[<>=!]+\s+\d+\s+\*|\d+\s+[<>=!]+\s+\d+\s+\+'},

            # Valor absoluto derivado de comparaciones
            {'name': 'AbsValue', 'regex': r'dup\s+-?\d+\s+%'},

            # Modificación de máscaras con operadores lógicos
            {'name': 'MaskModifier', 'regex': r't\s+\d+\s+&\s+t\s+\d+\s+\|'},

            # Combinación de múltiples máscaras
            {'name': 'MultiMask', 'regex': r't\s+\d+\s+&\s+t\s+\d+\s+&'},

            # Desplazamiento combinado con máscaras
            {'name': 'ShiftWithMask', 'regex': r't\s+\d+\s+&\s+t\s+\d+\s+>>|t\s+\d+\s+&\s+t\s+\d+\s+<<'},

            # Selección de valores con índices dinámicos
            {'name': 'DynamicPick', 'regex': r't\s+\d+\s+% pick'},

            # Reutilización de valores con "dup"
            {'name': 'DupReuse', 'regex': r'dup\s+t\s+swap'},

            # Patrón de desplazamiento y máscara en secuencia
            {'name': 'ShiftAndMask', 'regex': r't\s+\d+\s+>>\s+t\s+\d+\s+&'},

            # Patrón de operaciones trigonométricas extendidas
            {'name': 'ExtendedTrig', 'regex': r't\s+(sin|cos|tan)\s+\d+\s+\*'},

            # Patrón de combinación aritmética compleja
            {'name': 'ArithCombine', 'regex': r'\d+\s+\d+\s+\*\s+\d+\s+\+'},

            # Patrón de división modular
            {'name': 'ModPeriod', 'regex': r't\s+\d+\s+%'},

            # Patrón de máscara de bits
            {'name': 'Bitmask', 'regex': r't\s+\d+\s+&'},

            # Patrón de desplazamiento de bits
            {'name': 'BitShift', 'regex': r't\s+\d+\s+>>|t\s+\d+\s+<<'},

            # Patrón de selección de valores
            {'name': 'ValueSelect', 'regex': r't\s+\d+\s+% pick'},
        ]

        # Contador de macroestructuras
        self.macro_counts = defaultdict(int)

        # Usamos defaultdict para facilitar el manejo
        self.dependencies = defaultdict(list)

        self.pattern_weights = {
            'Bitmask': 3,               # Máscaras son comunes pero importantes
            'ModPeriod': 5,             # Módulos periódicos son clave en muchas expresiones
            'BitShift': 4,              # Desplazamientos son específicos pero no críticos
            'LinearScale': 6,           # Combinaciones lineales son relevantes
            'ValueSelect': 7,           # Selección dinámica de valores es crítica
            'ArithCombine': 5,          # Combinaciones aritméticas son importantes
            'ShiftChain': 6,            # Cadenas de desplazamiento son avanzadas
            'BitArith': 5,              # Operaciones bitwise + shift son específicas
            'DupReuse': 2,              # Reutilización es común pero menos crítica
            'ModShift': 8,              # Módulo seguido de shift es avanzado
            'StackOps': 3,              # Operaciones de pila son básicas pero útiles
            'TrigFunc': 9,              # Funciones trigonométricas son muy específicas
            'Conditional': 10,          # Operaciones condicionales son muy relevantes
            'AbsValue': 7,              # Valor absoluto derivado es específico
            'MaskModifier': 8,          # Modificación de máscaras es avanzada
            'MultiMask': 9,             # Combinación de múltiples máscaras es avanzada
            'ShiftWithMask': 10,        # Desplazamiento con máscara es muy específico
            'DynamicPick': 11,          # Selección dinámica es crítica y avanzada
            'DupReuse': 3,              # Reutilización con "dup" es básica
            'ShiftAndMask': 9,          # Desplazamiento y máscara en secuencia es avanzado
            'ExtendedTrig': 10,         # Trigonometría extendida es muy específica
            'ArithCombine': 6,          # Combinación aritmética compleja es relevante
            }

        self.frequency_multiplier = {
            'Bitmask': 1.0,             # Común
            'ModPeriod': 1.2,           # Menos común
            'BitShift': 1.1,            # Moderadamente común
            'LinearScale': 1.3,         # Menos común
            'ValueSelect': 1.5,         # Raro
            'ArithCombine': 1.2,        # Moderadamente común
            'ShiftChain': 1.4,          # Raro
            'BitArith': 1.3,            # Menos común
            'DupReuse': 1.0,            # Muy común
            'ModShift': 1.6,            # Muy raro
            'StackOps': 1.0,            # Común
            'TrigFunc': 1.8,            # Muy raro
            'Conditional': 1.7,         # Raro
            'AbsValue': 1.4,            # Menos común
            'MaskModifier': 1.5,        # Raro
            'MultiMask': 1.6,           # Muy raro
            'ShiftWithMask': 1.7,       # Muy raro
            'DynamicPick': 1.8,         # Muy raro
            'ShiftAndMask': 1.6,        # Muy raro
            'ExtendedTrig': 1.7,        # Muy raro
            'ArithCombine': 1.3,        # Menos común
            }

        self.dependency_bonus = {
            'ValueSelect': 2,           # Depende de ModPeriod
            'ModShift': 3,              # Combina ModPeriod y BitShift
            'MaskModifier': 2,          # Combina múltiples máscaras
            'MultiMask': 3,             # Combina múltiples máscaras
            'ShiftWithMask': 4,         # Combina Bitmask y BitShift
            'DynamicPick': 5,           # Combina ModPeriod y ValueSelect
            'ShiftAndMask': 3,          # Combina Bitmask y BitShift
            'ExtendedTrig': 2,          # Combina TrigFunc y operaciones adicionales
            'ArithCombine': 2,          # Puede depender de LinearScale
            }


    def classify_expression(self, expr):
        found = []
        for pattern in self.patterns:
            if re.search(pattern['regex'], expr):
                found.append(pattern['name'])

        # Detectar macroestructuras
        macro = tuple(sorted(found))
        if len(macro) > 1:
            self.macro_counts[macro] += 1

        return {
            'structures': found,
            'order': self.detect_order(expr),
            'macro_structure': macro if len(macro) > 1 else None
        }

    def detect_order(self, expr):
        order = []
        tokens = expr.split()
        for i, token in enumerate(tokens):
            for pattern in self.patterns:
                if re.match(pattern['regex'], ' '.join(tokens[i:i+3])):
                    order.append((i, pattern['name']))
        return sorted(order, key=lambda x: x[0])

    def add_pattern(self, name, regex):
        self.patterns.append({'name': name, 'regex': regex})
        # Mantener orden por especificidad
        self.patterns.sort(key=lambda x: len(x['regex']), reverse=True)

    def get_macro_statistics(self):
        return self.macro_counts


    # --- dependencias

    def analyze_dependencies(self, expr):
        tokens = expr.split()
        stack = []
        structure_positions = self.detect_structure_positions(expr)

        for i, token in enumerate(tokens):
            current_structure = self.find_current_structure(i, structure_positions)

            if current_structure:
                # Obtener operandos necesarios para esta estructura
                operands_needed = self.get_operands_needed(current_structure)
                operands = stack[-operands_needed:] if operands_needed else []

                # Registrar dependencias
                for operand in operands:
                    if operand.startswith("STRUCT_") or operand.startswith("VALUE_"):
                        self.dependencies[f"STRUCT_{current_structure}"].append(operand)

                # Actualizar el stack con el resultado de la estructura
                stack = stack[:-operands_needed]
                stack.append(f"STRUCT_{current_structure}")

            else:
                # Manejar operadores individuales
                if token in {'+', '-', '*', '/', '&', '|', '^', 'swap', 'pick'}:
                    operands_needed = 2 if token != 'pick' else 1
                    operands = stack[-operands_needed:]

                    # Registrar dependencias
                    self.dependencies[f"OP_{token}"].extend(operands)

                    # Actualizar stack
                    stack = stack[:-operands_needed]
                    stack.append(f"OP_{token}")

                elif token.isdigit() or token == 't':
                    stack.append(f"VALUE_{token}")

        return self.format_dependencies(self.dependencies)

    def get_operands_needed(self, structure_name):
        operand_rules = {
            'Bitmask': 2,
            'ModPeriod': 2,
            'BitShift': 2,
            'LinearScale': 2,
            'ValueSelect': 2,
            'ArithCombine': 2,
            'ShiftChain': 2,
            'BitArith': 2,
            'DupReuse': 1,
            'ModShift': 2,
            'StackOps': 1,
            'TrigFunc': 1,
            'Conditional': 2,
            'AbsValue': 1,
            'MaskModifier': 2,
            'MultiMask': 2,
            'ShiftWithMask': 2,
            'DynamicPick': 2,
            'ExtendedTrig': 2,
        }
        return operand_rules.get(structure_name, 0)

    def detect_structure_positions(self, expr):
        # Retorna un diccionario {posición: nombre_de_estructura}
        positions = {}
        for pattern in self.patterns:
            for match in re.finditer(pattern['regex'], expr):
                start = match.start()
                end = match.end()
                # Marcar todas las posiciones cubiertas por la estructura
                for i in range(start, end):  # -- previo -- start, end1+
                    positions[i] = pattern['name']
        return positions

    def find_current_structure(self, index, structure_positions):
        # Retorna el nombre de la estructura que cubre este índice
        return structure_positions.get(index, None)

    def get_operands_needed(self, structure_name):
        # Define cuántos operandos consume cada estructura
        # Ejemplo: Bitmask (t [const] &) consume 2 operandos (t y const)
        operand_rules = {
            'Bitmask': 2,
            'ModPeriod': 2,
            'BitShift': 2,
            # ... (completar para todas las estructuras)
        }
        return operand_rules.get(structure_name, 0)


    def format_dependencies(self, dependencies):
        # Convierte dependencias en una lista legible
        formatted = []
        for consumer, producers in dependencies.items():
            if producers:
                formatted.append(f"{consumer} depends on: {', '.join(producers)}")
        return formatted

    # --- pesos

    def calculate_pattern_weight(self, pattern_name, dependencies):
        """Calcula el peso total de un patrón."""
        base_weight = self.pattern_weights.get(pattern_name, 1)
        freq_mult = self.frequency_multiplier.get(pattern_name, 1.0)
        dep_bonus = sum(self.dependency_bonus.get(dep, 0) for dep in dependencies)
        return base_weight * freq_mult + dep_bonus

    def classify_expression_with_weights(self, expr):
        """Clasifica una expresión y calcula los pesos de los patrones encontrados."""
        result = self.classify_expression(expr)  # Usa tu método existente
        structures = result['structures']
        dependencies = self.analyze_dependencies(expr)  # Usa tu método de dependencias

        weighted_structures = []
        for struct in structures:
            struct_deps = [dep for dep in dependencies if dep.startswith(f"STRUCT_{struct}")]
            weight = self.calculate_pattern_weight(struct, struct_deps)
            weighted_structures.append((struct, weight))

        # Ordenar por peso descendente
        weighted_structures.sort(key=lambda x: x[1], reverse=True)
        return weighted_structures

    def get_macro_statistics_with_weights(self, expressions):
        """Calcula estadísticas ponderadas para todas las expresiones."""
        stats = defaultdict(float)
        for expr in expressions:
            weighted_structures = self.classify_expression_with_weights(expr)
            for struct, weight in weighted_structures:
                stats[struct] += weight
        return stats

# Ejemplo de uso
if __name__ == "__main__":
    classifier = RPNClassifier()

    # Clasificar una expresión
    expr = sys.argv[1]
    result = classifier.classify_expression(expr)

    print(f'\n------ ANALIZANDO ------ {expr}')
    print("Estructuras encontradas:", result['structures'])
    print("Orden de aparición:", [n for i,n in result['order']])
    print("Macroestructura:", result['macro_structure'])
    print("Macro-estructuras más comunes:", classifier.get_macro_statistics())

    # Análisis de dependencias (opcional)
    dependencies = classifier.analyze_dependencies(expr)
    print("\nDependencias entre estructuras:")
    for dep in dependencies:
        print(f"- {dep}")

    # Clasificar y calcular pesos
    weighted_structures = classifier.classify_expression_with_weights(expr)
    print("\nEstructuras con pesos:")
    for struct, weight in weighted_structures:
        print(f"{struct}: {weight}")
