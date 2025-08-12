#!/usr/bin/env python3
"""
Script simple para ejecutar el análisis del caso de Workana
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def main():
    print("🚀 INICIANDO ANÁLISIS COMPLETO DEL EXPERIMENTO DE WORKANA")
    print("="*70)
    
    # 1. Cargar datos
    print("📊 Cargando datos del experimento de Workana...")
    
    try:
        # Cargar todas las pestañas
        abtests = pd.read_excel('data/challenge_workana.xlsx', sheet_name='abtests')
        projects = pd.read_excel('data/challenge_workana.xlsx', sheet_name='projects')
        bids = pd.read_excel('data/challenge_workana.xlsx', sheet_name='bids')
        threads = pd.read_excel('data/challenge_workana.xlsx', sheet_name='threads')
        accepted_bids = pd.read_excel('data/challenge_workana.xlsx', sheet_name='accepted_bids')
        payments = pd.read_excel('data/challenge_workana.xlsx', sheet_name='payments')
        skills = pd.read_excel('data/challenge_workana.xlsx', sheet_name='skills')
        
        print("✅ Datos cargados exitosamente!")
        print(f"   - A/B Tests: {len(abtests)} registros")
        print(f"   - Proyectos: {len(projects)} registros")
        print(f"   - Propuestas: {len(bids)} registros")
        print(f"   - Conversaciones: {len(threads)} registros")
        print(f"   - Propuestas aceptadas: {len(accepted_bids)} registros")
        print(f"   - Pagos: {len(payments)} registros")
        print(f"   - Habilidades: {len(skills)} registros")
        
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return
    
    # 2. Preparar datos del experimento
    print("\n🔧 Preparando datos para el análisis...")
    
    # Unir datos de A/B tests con proyectos
    experiment_data = abtests.merge(
        projects, 
        left_on='project_id', 
        right_on='id', 
        how='left'
    )
    
    # Unir con propuestas para obtener métricas de freelancers
    bids_summary = bids.groupby('project_id').agg({
        'worker_position_label': 'count',
        'usd_amount': ['mean', 'min', 'max']
    }).reset_index()
    
    # Limpiar nombres de columnas
    bids_summary.columns = [col[0] if col[1] == '' else f"{col[0]}_{col[1]}" 
                           for col in bids_summary.columns]
    
    # Renombrar columnas importantes
    bids_summary = bids_summary.rename(columns={
        'worker_position_label_count': 'total_bids',
        'usd_amount_mean': 'avg_bid_amount',
        'usd_amount_min': 'min_bid_amount',
        'usd_amount_max': 'max_bid_amount'
    })
    
    # Unir con el experimento
    experiment_data = experiment_data.merge(
        bids_summary,
        left_on='project_id',
        right_on='project_id',
        how='left'
    )
    
    # Separar grupos de control y test
    control_group = experiment_data[experiment_data['segment'] == 'default'].copy()
    test_group = experiment_data[experiment_data['segment'] == 'evalbidsNewOrder'].copy()
    
    print(f"✅ Datos preparados:")
    print(f"   - Grupo Control: {len(control_group)} proyectos")
    print(f"   - Grupo Test: {len(test_group)} proyectos")
    
    # 3. Analizar métrica principal
    print("\n" + "="*60)
    print("🎯 ANÁLISIS DE LA MÉTRICA PRINCIPAL: EL1 CONVERSION RATE")
    print("="*60)
    
    # Calcular tasas de conversión EL1
    control_el1_rate = control_group['el1'].mean()
    test_el1_rate = test_group['el1'].mean()
    
    # Diferencia absoluta y relativa
    absolute_diff = test_el1_rate - control_el1_rate
    relative_diff = (test_el1_rate / control_el1_rate - 1) * 100
    
    # Test de significancia estadística
    contingency_table = pd.crosstab(
        pd.concat([control_group['el1'], test_group['el1']]),
        pd.concat([pd.Series(['control']*len(control_group)), 
                  pd.Series(['test']*len(test_group))])
    )
    
    chi2, p_value = stats.chi2_contingency(contingency_table)[0:2]
    
    # Mostrar resultados
    print(f"📊 RESULTADOS DEL EXPERIMENTO:")
    print(f"   Grupo Control: {control_el1_rate:.3f} ({control_el1_rate*100:.1f}%)")
    print(f"   Grupo Test: {test_el1_rate:.3f} ({test_el1_rate*100:.1f}%)")
    print(f"   Diferencia Absoluta: {absolute_diff:.3f}")
    print(f"   Diferencia Relativa: {relative_diff:.1f}%")
    print(f"\n📈 SIGNIFICANCIA ESTADÍSTICA:")
    print(f"   p-value: {p_value:.4f}")
    print(f"   {'✅ Diferencia SIGNIFICATIVA' if p_value < 0.05 else '❌ Diferencia NO significativa'}")
    
    # Interpretación del impacto
    if p_value < 0.05:
        if relative_diff > 0:
            print(f"\n🎉 IMPACTO POSITIVO: El nuevo algoritmo mejoró la conversión EL1 en {relative_diff:.1f}%")
        else:
            print(f"\n⚠️ IMPACTO NEGATIVO: El nuevo algoritmo redujo la conversión EL1 en {abs(relative_diff):.1f}%")
    else:
        print(f"\n🔍 SIN IMPACTO SIGNIFICATIVO: No hay evidencia estadística de diferencia entre grupos")
    
    # 4. Analizar métricas complementarias
    print("\n" + "="*60)
    print("📊 ANÁLISIS DE MÉTRICAS COMPLEMENTARIAS")
    print("="*60)
    
    # 1. Tasa de propuestas aceptadas
    print("\n1️⃣ TASA DE PROPUESTAS ACEPTADAS:")
    control_acceptance = control_group['total_bids'].mean()
    test_acceptance = test_group['total_bids'].mean()
    
    acceptance_diff = test_acceptance - control_acceptance
    acceptance_relative = (test_acceptance / control_acceptance - 1) * 100 if control_acceptance > 0 else 0
    
    print(f"   Control: {control_acceptance:.1f} propuestas promedio")
    print(f"   Test: {test_acceptance:.1f} propuestas promedio")
    print(f"   Diferencia: {acceptance_diff:.1f} ({acceptance_relative:.1f}%)")
    
    # 2. Calidad de freelancers (gamification levels)
    print("\n2️⃣ CALIDAD DE FREELANCERS (Gamification Levels):")
    
    # Obtener distribución de niveles por grupo
    control_levels = bids[bids['project_id'].isin(control_group['project_id'])]['worker_position_label'].value_counts()
    test_levels = bids[bids['project_id'].isin(test_group['project_id'])]['worker_position_label'].value_counts()
    
    gamification_levels = ['hero', 'platinum', 'gold', 'silver', 'bronze', 'iron']
    
    print("   Distribución por grupo:")
    for level in gamification_levels:
        control_pct = control_levels.get(level, 0) / len(control_levels) * 100 if len(control_levels) > 0 else 0
        test_pct = test_levels.get(level, 0) / len(test_levels) * 100 if len(test_levels) > 0 else 0
        print(f"     {level.title()}: Control {control_pct:.1f}% | Test {test_pct:.1f}%")
    
    # 3. Tipos de clientes
    print("\n3️⃣ DISTRIBUCIÓN DE TIPOS DE CLIENTES:")
    control_client_types = control_group['client_type'].value_counts()
    test_client_types = test_group['client_type'].value_counts()
    
    print("   Por grupo:")
    for client_type in ['new', 'rebuy']:
        control_pct = control_client_types.get(client_type, 0) / len(control_group) * 100
        test_pct = test_client_types.get(client_type, 0) / len(test_group) * 100
        print(f"     {client_type.title()}: Control {control_pct:.1f}% | Test {test_pct:.1f}%")
    
    # 5. Generar recomendaciones de negocio
    print("\n" + "="*60)
    print("💼 RECOMENDACIONES DE NEGOCIO Y TOMA DE DECISIONES")
    print("="*60)
    
    print("\n📊 RESUMEN DE RESULTADOS:")
    print(f"   Métrica Principal (EL1): {'✅ Mejoró' if relative_diff > 0 else '❌ Empeoró'}")
    print(f"   Significancia Estadística: {'✅ Sí' if p_value < 0.05 else '❌ No'}")
    
    print("\n🎯 RECOMENDACIÓN PRINCIPAL:")
    
    if p_value < 0.05:
        if relative_diff > 0:
            print("   🚀 IMPLEMENTAR: El nuevo algoritmo mejoró significativamente la conversión EL1")
            print("   ✅ Avanzar con esta solución")
        else:
            print("   ⚠️ DESCARTAR: El nuevo algoritmo redujo significativamente la conversión EL1")
            print("   ❌ No implementar esta solución")
    else:
        print("   🔍 ITERAR: No hay evidencia estadística de impacto")
        print("   📝 Considerar mejoras en el experimento")
    
    print("\n📈 PRÓXIMOS PASOS RECOMENDADOS:")
    
    if p_value < 0.05 and relative_diff > 0:
        print("   1. Implementar el nuevo algoritmo en toda la plataforma")
        print("   2. Monitorear métricas complementarias durante el rollout")
        print("   3. Planificar experimentos A/B para otras categorías")
        print("   4. Analizar el impacto en métricas de negocio (ingresos, retención)")
    
    elif p_value < 0.05 and relative_diff < 0:
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
    
    # 6. Resumen ejecutivo
    print("\n" + "="*70)
    print("📋 RESUMEN EJECUTIVO DEL EXPERIMENTO")
    print("="*70)
    
    print(f"\n🎯 MÉTRICA PRINCIPAL (EL1 Conversion Rate):")
    print(f"   Impacto: {relative_diff:.1f}%")
    print(f"   Significancia: {'SÍ' if p_value < 0.05 else 'NO'}")
    
    if p_value < 0.05 and relative_diff > 0:
        next_steps = "Implementar nuevo algoritmo"
    elif p_value < 0.05 and relative_diff < 0:
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
