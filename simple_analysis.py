#!/usr/bin/env python3
"""
Análisis completo del experimento de Workana
"""

import pandas as pd
import numpy as np
from scipy import stats

def main():
    print("🚀 ANÁLISIS COMPLETO DEL EXPERIMENTO DE WORKANA")
    print("="*60)
    
    # Cargar datos
    print("📊 Cargando datos...")
    abtests = pd.read_excel('data/challenge_workana.xlsx', sheet_name='abtests')
    projects = pd.read_excel('data/challenge_workana.xlsx', sheet_name='projects')
    bids = pd.read_excel('data/challenge_workana.xlsx', sheet_name='bids')
    skills = pd.read_excel('data/challenge_workana.xlsx', sheet_name='skills')
    
    print(f"✅ Datos cargados: {len(abtests)} A/B tests, {len(projects)} proyectos, {len(bids)} propuestas")
    
    # Unir datos
    experiment_data = abtests.merge(projects, left_on='project_id', right_on='id', how='left')
    
    # Separar grupos
    control = experiment_data[experiment_data['segment'] == 'default']
    test = experiment_data[experiment_data['segment'] == 'evalbidsNewOrder']
    
    print(f"\n📊 Grupos: Control {len(control)}, Test {len(test)}")
    
    # ===== MÉTRICA PRINCIPAL: EL1 =====
    print("\n" + "="*60)
    print("🎯 ANÁLISIS DE LA MÉTRICA PRINCIPAL: EL1 CONVERSION RATE")
    print("="*60)
    
    control_el1 = control['el1'].mean()
    test_el1 = test['el1'].mean()
    
    print(f"📊 RESULTADOS DEL EXPERIMENTO:")
    print(f"   Grupo Control: {control_el1:.3f} ({control_el1*100:.1f}%)")
    print(f"   Grupo Test: {test_el1:.3f} ({test_el1*100:.1f}%)")
    
    # Diferencia
    diff = test_el1 - control_el1
    diff_pct = (test_el1 / control_el1 - 1) * 100
    
    print(f"   Diferencia Absoluta: {diff:.3f}")
    print(f"   Diferencia Relativa: {diff_pct:.1f}%")
    
    # Test estadístico
    control_el1_count = control['el1'].sum()
    control_total = len(control)
    test_el1_count = test['el1'].sum()
    test_total = len(test)
    
    contingency = np.array([
        [control_el1_count, control_total - control_el1_count],
        [test_el1_count, test_total - test_el1_count]
    ])
    
    chi2, p_value = stats.chi2_contingency(contingency)[0:2]
    
    print(f"\n📈 SIGNIFICANCIA ESTADÍSTICA:")
    print(f"   p-value: {p_value:.4f}")
    print(f"   {'✅ Diferencia SIGNIFICATIVA' if p_value < 0.05 else '❌ Diferencia NO significativa'}")
    
    # Interpretación del impacto
    if p_value < 0.05:
        if diff_pct > 0:
            print(f"\n🎉 IMPACTO POSITIVO: El nuevo algoritmo mejoró la conversión EL1 en {diff_pct:.1f}%")
        else:
            print(f"\n⚠️ IMPACTO NEGATIVO: El nuevo algoritmo redujo la conversión EL1 en {abs(diff_pct):.1f}%")
    else:
        print(f"\n🔍 SIN IMPACTO SIGNIFICATIVO: No hay evidencia estadística de diferencia entre grupos")
    
    # ===== MÉTRICAS COMPLEMENTARIAS =====
    print("\n" + "="*60)
    print("📊 ANÁLISIS DE MÉTRICAS COMPLEMENTARIAS")
    print("="*60)
    
    # 1. Calidad de freelancers (gamification levels)
    print("\n1️⃣ CALIDAD DE FREELANCERS (Gamification Levels):")
    
    # Obtener distribución de niveles por grupo
    control_bids = bids[bids['project_id'].isin(control['project_id'])]
    test_bids = bids[bids['project_id'].isin(test['project_id'])]
    
    control_levels = control_bids['worker_position_label'].value_counts()
    test_levels = test_bids['worker_position_label'].value_counts()
    
    gamification_levels = ['hero', 'platinum', 'gold', 'silver', 'bronze', 'iron']
    
    print("   Distribución por grupo:")
    for level in gamification_levels:
        control_pct = control_levels.get(level, 0) / len(control_levels) * 100 if len(control_levels) > 0 else 0
        test_pct = test_levels.get(level, 0) / len(test_levels) * 100 if len(test_levels) > 0 else 0
        print(f"     {level.title()}: Control {control_pct:.1f}% | Test {test_pct:.1f}%")
    
    # 2. Tipos de clientes
    print("\n2️⃣ DISTRIBUCIÓN DE TIPOS DE CLIENTES:")
    control_client_types = control['client_type'].value_counts()
    test_client_types = test['client_type'].value_counts()
    
    print("   Por grupo:")
    for client_type in ['new', 'rebuy']:
        control_pct = control_client_types.get(client_type, 0) / len(control) * 100
        test_pct = test_client_types.get(client_type, 0) / len(test) * 100
        print(f"     {client_type.title()}: Control {control_pct:.1f}% | Test {test_pct:.1f}%")
    
    # 3. Presupuestos de proyectos
    print("\n3️⃣ PRESUPUESTOS DE PROYECTOS:")
    control_budget = control['budget'].value_counts()
    test_budget = test['budget'].value_counts()
    
    print("   Distribución de presupuestos:")
    for budget in control_budget.index:
        control_pct = control_budget.get(budget, 0) / len(control) * 100
        test_pct = test_budget.get(budget, 0) / len(test) * 100
        print(f"     {budget}: Control {control_pct:.1f}% | Test {test_pct:.1f}%")
    
    # ===== HALLAZGOS INESPERADOS =====
    print("\n" + "="*60)
    print("🔍 ANÁLISIS DE HALLAZGOS INESPERADOS Y PATRONES")
    print("="*60)
    
    # 1. Análisis temporal
    print("\n1️⃣ ANÁLISIS TEMPORAL:")
    
    # Convertir fechas
    control['created'] = pd.to_datetime(control['created'])
    test['created'] = pd.to_datetime(test['created'])
    
    # Agrupar por día
    control_daily = control.groupby(control['created'].dt.date)['el1'].mean()
    test_daily = test.groupby(test['created'].dt.date)['el1'].mean()
    
    print(f"   Variación diaria de conversión EL1:")
    print(f"     Control: {control_daily.std():.3f} (estabilidad)")
    print(f"     Test: {test_daily.std():.3f} (estabilidad)")
    
    if abs(control_daily.std() - test_daily.std()) > 0.01:
        print("   🔍 HALLAZGO: Diferencia en estabilidad temporal entre grupos")
    
    # 2. Análisis de outliers
    print("\n2️⃣ ANÁLISIS DE OUTLIERS:")
    
    # Proyectos con conversión EL1 muy alta
    control_high_conv = control[control['el1'] == 1]
    test_high_conv = test[test['el1'] == 1]
    
    print(f"   Proyectos con conversión EL1 alta:")
    print(f"     Control: {len(control_high_conv)} proyectos ({len(control_high_conv)/len(control)*100:.1f}%)")
    print(f"     Test: {len(test_high_conv)} proyectos ({len(test_high_conv)/len(test)*100:.1f}%)")
    
    # ===== RECOMENDACIONES DE NEGOCIO =====
    print("\n" + "="*60)
    print("💼 RECOMENDACIONES DE NEGOCIO Y TOMA DE DECISIONES")
    print("="*60)
    
    print("\n📊 RESUMEN DE RESULTADOS:")
    print(f"   Métrica Principal (EL1): {'✅ Mejoró' if diff_pct > 0 else '❌ Empeoró'}")
    print(f"   Significancia Estadística: {'✅ Sí' if p_value < 0.05 else '❌ No'}")
    
    print("\n🎯 RECOMENDACIÓN PRINCIPAL:")
    
    if p_value < 0.05:
        if diff_pct > 0:
            print("   🚀 IMPLEMENTAR: El nuevo algoritmo mejoró significativamente la conversión EL1")
            print("   ✅ Avanzar con esta solución")
        else:
            print("   ⚠️ DESCARTAR: El nuevo algoritmo redujo significativamente la conversión EL1")
            print("   ❌ No implementar esta solución")
    else:
        print("   🔍 ITERAR: No hay evidencia estadística de impacto")
        print("   📝 Considerar mejoras en el experimento")
    
    print("\n📈 PRÓXIMOS PASOS RECOMENDADOS:")
    
    if p_value < 0.05 and diff_pct > 0:
        print("   1. Implementar el nuevo algoritmo en toda la plataforma")
        print("   2. Monitorear métricas complementarias durante el rollout")
        print("   3. Planificar experimentos A/B para otras categorías")
        print("   4. Analizar el impacto en métricas de negocio (ingresos, retención)")
    
    elif p_value < 0.05 and diff_pct < 0:
        print("   1. Revertir inmediatamente el nuevo algoritmo")
        print("   2. Investigar por qué empeoró la conversión")
        print("   3. Revisar la lógica de scoring y filtrado")
        print("   4. Diseñar un nuevo experimento con ajustes")
    
    else:
        print("   1. Aumentar el tamaño de muestra del experimento")
        print("   2. Extender la duración del experimento")
        print("   3. Revisar la segmentación y randomización")
        print("   4. Considerar métricas alternativas de éxito")
    
    print("\n🔬 HIPÓTESIS PARA FUTUROS EXPERIMENTOS:")
    print("   1. Ajustar los pesos del algoritmo de scoring")
    print("   2. Probar diferentes umbrales de filtrado")
    print("   3. Experimentar con categorías específicas")
    print("   4. Analizar el impacto por tipo de cliente (New vs Rebuy)")
    
    # ===== RESUMEN EJECUTIVO =====
    print("\n" + "="*70)
    print("📋 RESUMEN EJECUTIVO DEL EXPERIMENTO")
    print("="*70)
    
    print(f"\n🎯 MÉTRICA PRINCIPAL (EL1 Conversion Rate):")
    print(f"   Impacto: {diff_pct:.1f}%")
    print(f"   Significancia: {'SÍ' if p_value < 0.05 else 'NO'}")
    
    if p_value < 0.05 and diff_pct > 0:
        next_steps = "Implementar nuevo algoritmo"
    elif p_value < 0.05 and diff_pct < 0:
        next_steps = "Revertir cambios"
    else:
        next_steps = "Mejorar experimento"
    
    print(f"\n💼 RECOMENDACIÓN:")
    print(f"   {next_steps}")
    
    print(f"\n📈 PRÓXIMOS PASOS:")
    print("   1. Preparar presentación para stakeholders")
    print("   2. Implementar recomendaciones de negocio")
    print("   3. Planificar próximos experimentos")
    
    print("\n✅ Análisis completo finalizado!")

if __name__ == "__main__":
    main()
