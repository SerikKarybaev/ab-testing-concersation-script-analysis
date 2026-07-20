"""
Генерация синтетических данных для A/B теста скриптов разговора.

Эксперимент: Сравнение Control vs Treatment скрипта для сегмента "3-6 НБ"
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

def generate_ab_test_data(
    n_calls_per_variant=5000,
    control_result_rate=0.08,
    treatment_result_rate=0.12,  # Новый скрипт на 50% лучше
    random_state=42
):
    """
    Генерирует данные A/B теста.
    
    Parameters:
    -----------
    n_calls_per_variant : int
        Количество звонков на каждый вариант
    control_result_rate : float
        Result rate для контрольной группы
    treatment_result_rate : float
        Result rate для тестовой группы
    random_state : int
        Random seed
    
    Returns:
    --------
    pd.DataFrame
        Данные эксперимента
    """
    
    np.random.seed(random_state)
    
    print("=" * 60)
    print("GENERATING A/B TEST DATA")
    print("=" * 60)
    
    # Параметры эксперимента
    start_date = datetime(2025, 2, 1)
    end_date = datetime(2025, 2, 28)
    
    data = []
    
    # Генерируем данные для обеих групп
    for variant in ['Control', 'Treatment']:
        
        result_rate = control_result_rate if variant == 'Control' else treatment_result_rate
        
        for i in range(n_calls_per_variant):
            
            # Дата звонка (случайная в пределах эксперимента)
            days_offset = np.random.randint(0, (end_date - start_date).days)
            call_date = start_date + timedelta(days=days_offset)
            
            # Час звонка (больше звонков днём)
            hour = np.random.choice(range(9, 21), p=[0.05, 0.08, 0.10, 0.12, 0.15, 
                                                     0.12, 0.10, 0.08, 0.08, 0.06, 
                                                     0.04, 0.02])
            
            # Contact (вероятность дозвона)
            # Treatment скрипт не влияет на дозвон
            contact_prob = 0.45
            is_contact = np.random.random() < contact_prob
            
            # Result (если был контакт)
            if is_contact:
                is_result = np.random.random() < result_rate
            else:
                is_result = False
            
            # Agreement (если был результат)
            if is_result:
                is_agreement = np.random.random() < 0.7  # 70% результатов с согласием
            else:
                is_agreement = False
            
            # Duration (секунды)
            # Treatment скрипт короче (меньше "воды")
            if variant == 'Treatment':
                avg_duration = 120  # 2 минуты
            else:
                avg_duration = 150  # 2.5 минуты
            
            call_duration = max(10, np.random.normal(avg_duration, 30))
            
            # Клиент
            client_id = f"C{i:05d}"
            
            data.append({
                'call_id': f"{variant[0]}{i:05d}",
                'client_id': client_id,
                'variant': variant,
                'call_date': call_date.date(),
                'call_hour': hour,
                'is_contact': int(is_contact),
                'is_result': int(is_result),
                'is_agreement': int(is_agreement),
                'call_duration_sec': int(call_duration)
            })
    
    df = pd.DataFrame(data)
    
    print(f"\n✓ Generated {len(df):,} calls")
    print(f"  Control: {len(df[df['variant'] == 'Control']):,}")
    print(f"  Treatment: {len(df[df['variant'] == 'Treatment']):,}")
    
    # Статистика
    print(f"\n📊 Summary Statistics:")
    for variant in ['Control', 'Treatment']:
        variant_df = df[df['variant'] == variant]
        
        contact_rate = variant_df['is_contact'].mean()
        result_rate = variant_df['is_result'].mean()
        agreement_rate = variant_df['is_agreement'].mean()
        avg_duration = variant_df['call_duration_sec'].mean()
        
        print(f"\n  {variant}:")
        print(f"    Contact Rate: {contact_rate:.2%}")
        print(f"    Result Rate: {result_rate:.2%}")
        print(f"    Agreement Rate: {agreement_rate:.2%}")
        print(f"    Avg Duration: {avg_duration:.0f} sec")
    
    return df


def save_test_config(filepath='data/test_config.yaml'):
    """
    Сохраняет конфигурацию теста.
    """
    
    config = """
# A/B Test Configuration
experiment:
  name: "Conversation Script Optimization"
  segment: "3-6 НБ"
  start_date: "2025-02-01"
  end_date: "2025-02-28"
  
variants:
  control:
    name: "Control (Current Script)"
    description: "Existing conversation script with standard flow"
    
  treatment:
    name: "Treatment (Optimized Script)"
    description: "New script with shorter intro, direct value proposition"
    changes:
      - "Reduced greeting from 15s to 5s"
      - "Added urgency cue in first 10 seconds"
      - "Simplified payment options explanation"
      - "Added social proof element"

metrics:
  primary:
    name: "Result Rate"
    description: "% of calls resulting in payment promise"
    
  secondary:
    - name: "Contact Rate"
      description: "% of calls where client answered"
    - name: "Agreement Rate"
      description: "% of results with formal agreement"
    - name: "Call Duration"
      description: "Average call length in seconds"

statistical_params:
  alpha: 0.05
  power: 0.8
  minimum_detectable_effect: 0.02
"""
    
    Path(filepath).parent.mkdir(exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(config)
    
    print(f"\n💾 Test config saved to: {filepath}")


if __name__ == '__main__':
    
    # Генерация данных
    df = generate_ab_test_data(
        n_calls_per_variant=5000,
        control_result_rate=0.08,
        treatment_result_rate=0.12,
        random_state=42
    )
    
    # Сохранение
    Path('data').mkdir(exist_ok=True)
    
    output_path = 'data/ab_test_data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n💾 Data saved to: {output_path}")
    
    # Сохранение конфигурации
    save_test_config()
    
    print("\n" + "=" * 60)
    print("✓ DATA GENERATION COMPLETE")
    print("=" * 60)