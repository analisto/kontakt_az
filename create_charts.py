#!/usr/bin/env python3
"""
Create focused, meaningful charts from electricity data for README presentation.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Create charts directory
os.makedirs('charts', exist_ok=True)

# Store findings for README
findings = []

print("="*80)
print("CREATING ELECTRICITY DATA VISUALIZATIONS")
print("="*80)

# ==============================================================================
# 1. GLOBAL ELECTRICITY PRODUCTION BY SOURCE
# ==============================================================================
print("\n1. Creating Global Electricity Production Mix chart...")

df_production = pd.read_csv('wikipedia_data/List of countries by electricity production_table_1.csv', skiprows=[0])
world_data = df_production[df_production['Location'] == 'World'].iloc[0]

# Energy sources
sources = ['Coal', 'Gas', 'Hydro', 'Nuclear', 'Wind', 'Solar', 'Oil*', 'Bio.', 'Geo.']
values = [float(world_data[src]) for src in sources]

# Calculate percentages
total = sum(values)
percentages = [(v/total)*100 for v in values]

# Sort by value (descending)
sorted_data = sorted(zip(sources, values, percentages), key=lambda x: x[1], reverse=True)
sources_sorted = [x[0] for x in sorted_data]
values_sorted = [x[1] for x in sorted_data]
pct_sorted = [x[2] for x in sorted_data]

# Create horizontal bar chart
fig, ax = plt.subplots(figsize=(14, 9))
colors_dict = {'Coal': '#8B4513', 'Gas': '#FF6B6B', 'Hydro': '#4ECDC4', 'Nuclear': '#FFE66D',
               'Wind': '#95E1D3', 'Solar': '#FFA07A', 'Oil*': '#696969', 'Bio.': '#90EE90', 'Geo.': '#DDA15E'}
bar_colors = [colors_dict[src] for src in sources_sorted]

bars = ax.barh(sources_sorted, values_sorted, color=bar_colors, alpha=0.85, edgecolor='black', linewidth=0.8)

# Add value labels with both TWh and percentage
for i, (bar, val, pct) in enumerate(zip(bars, values_sorted, pct_sorted)):
    ax.text(val + 150, i, f'{val:,.0f} TWh ({pct:.1f}%)',
            va='center', fontsize=11, weight='bold')

ax.set_xlabel('Production (TWh)', fontsize=13, weight='bold')
ax.set_title('Global Electricity Production by Source (2024)\nTotal: 30,853 TWh',
             fontsize=18, weight='bold', pad=25)
ax.invert_yaxis()
ax.grid(axis='x', alpha=0.3)
ax.tick_params(axis='y', labelsize=12)

plt.tight_layout()
plt.savefig('charts/1_global_energy_mix.png', dpi=300, bbox_inches='tight', pad_inches=0.3)
plt.close()

findings.append({
    'title': 'Global Energy Mix Dominated by Fossil Fuels',
    'insight': f"Coal ({values[0]/sum(values)*100:.1f}%) and Gas ({values[1]/sum(values)*100:.1f}%) account for over half of global electricity production. Renewables (Wind, Solar, Hydro) combined represent {(values[4]+values[5]+values[2])/sum(values)*100:.1f}% of total production."
})

print("  ✓ Saved: charts/1_global_energy_mix.png")

# ==============================================================================
# 2. TOP 15 ELECTRICITY PRODUCERS
# ==============================================================================
print("\n2. Creating Top 15 Electricity Producers chart...")

# Get top 15 countries (excluding World)
top_producers = df_production[df_production['Location'] != 'World'].head(15)

fig, ax = plt.subplots(figsize=(12, 8))
countries = top_producers['Location'].values
total_production = top_producers['Total (TWh)[1]'].astype(float).values

bars = ax.barh(countries, total_production, color='steelblue')
ax.set_xlabel('Total Production (TWh)', fontsize=12, weight='bold')
ax.set_title('Top 15 Electricity Producers (2024)', fontsize=16, weight='bold', pad=20)
ax.invert_yaxis()

# Add value labels
for i, (bar, val) in enumerate(zip(bars, total_production)):
    ax.text(val + 100, i, f'{val:,.0f}', va='center', fontsize=10)

plt.tight_layout()
plt.savefig('charts/2_top_producers.png', dpi=300, bbox_inches='tight')
plt.close()

findings.append({
    'title': 'China Dominates Global Electricity Production',
    'insight': f"China produces {total_production[0]:,.0f} TWh, nearly {total_production[0]/total_production[1]:.1f}x more than the USA ({total_production[1]:,.0f} TWh). The top 3 producers (China, USA, India) account for {(total_production[0]+total_production[1]+total_production[2])/float(world_data['Total (TWh)[1]'])*100:.1f}% of global production."
})

print("  ✓ Saved: charts/2_top_producers.png")

# ==============================================================================
# 3. ENERGY MIX OF TOP 10 PRODUCERS
# ==============================================================================
print("\n3. Creating Energy Mix Comparison for Top 10 Producers...")

top_10 = df_production[df_production['Location'] != 'World'].head(10).copy()
sources_cols = ['Coal', 'Gas', 'Hydro', 'Nuclear', 'Wind', 'Solar']

# Prepare data
energy_mix = []
for idx, row in top_10.iterrows():
    country = row['Location']
    total = float(row['Total (TWh)[1]'])
    mix = {src: float(row[src])/total*100 if total > 0 else 0 for src in sources_cols}
    mix['Country'] = country
    energy_mix.append(mix)

df_mix = pd.DataFrame(energy_mix)
df_mix = df_mix.set_index('Country')

fig, ax = plt.subplots(figsize=(14, 8))
df_mix.plot(kind='bar', stacked=True, ax=ax,
            color=['#8B4513', '#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3', '#FFA07A'])
ax.set_ylabel('Percentage of Total Production (%)', fontsize=12, weight='bold')
ax.set_xlabel('Country', fontsize=12, weight='bold')
ax.set_title('Energy Mix of Top 10 Electricity Producers', fontsize=16, weight='bold', pad=20)
ax.legend(title='Source', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
plt.tight_layout()
plt.savefig('charts/3_top10_energy_mix.png', dpi=300, bbox_inches='tight')
plt.close()

findings.append({
    'title': 'Diverse Energy Strategies Among Top Producers',
    'insight': "China relies heavily on coal, USA has a balanced mix of gas/coal/nuclear/renewables, Brazil is dominated by hydro, and France leads in nuclear energy. Each country's energy mix reflects its natural resources and policy choices."
})

print("  ✓ Saved: charts/3_top10_energy_mix.png")

# ==============================================================================
# 4. RENEWABLE VS NON-RENEWABLE
# ==============================================================================
print("\n4. Creating Renewable vs Non-Renewable Analysis...")

df_renewable = pd.read_csv('wikipedia_data/List of countries by renewable electricity production_table_2.csv')

# Get top 15 by renewable production
top_renewable = df_renewable[df_renewable['Location'] != 'World'].head(15)

# Need to match with production data for percentages
renewable_comparison = []
for idx, row in top_renewable.iterrows():
    country = row['Location']
    renewable_twh = float(row['Renew.'])

    # Find matching production data
    prod_row = df_production[df_production['Location'] == country]
    if not prod_row.empty:
        total_twh = float(prod_row.iloc[0]['Total (TWh)[1]'])
        renewable_comparison.append({
            'Country': country,
            'Renewable': renewable_twh,
            'Percentage': (renewable_twh / total_twh * 100) if total_twh > 0 else 0
        })

df_ren_compare = pd.DataFrame(renewable_comparison)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Chart 1: Top renewable producers
countries_ren = df_ren_compare['Country'].values
renewable_prod = df_ren_compare['Renewable'].values

bars1 = ax1.barh(countries_ren, renewable_prod, color='green', alpha=0.7)
ax1.set_xlabel('Renewable Production (TWh)', fontsize=11, weight='bold')
ax1.set_title('Top 15 Renewable Electricity Producers', fontsize=14, weight='bold')
ax1.invert_yaxis()

for i, (bar, val) in enumerate(zip(bars1, renewable_prod)):
    ax1.text(val + 20, i, f'{val:,.0f}', va='center', fontsize=9)

# Chart 2: Renewable percentage of total
renewable_pct = df_ren_compare['Percentage'].values

bars2 = ax2.barh(countries_ren, renewable_pct, color='darkgreen', alpha=0.7)
ax2.set_xlabel('Renewable % of Total Production', fontsize=11, weight='bold')
ax2.set_title('Renewable Energy Share (%)', fontsize=14, weight='bold')
ax2.invert_yaxis()

for i, (bar, val) in enumerate(zip(bars2, renewable_pct)):
    ax2.text(val + 1, i, f'{val:.1f}%', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('charts/4_renewable_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

findings.append({
    'title': 'Renewable Energy Leaders',
    'insight': f"China leads in absolute renewable production ({renewable_prod[0]:,.0f} TWh), but countries like Brazil, Canada, and Norway have much higher renewable percentages ({renewable_pct[2]:.1f}%, {renewable_pct[3]:.1f}%, {renewable_pct[6]:.1f}% respectively), showing different paths to clean energy."
})

print("  ✓ Saved: charts/4_renewable_analysis.png")

# ==============================================================================
# 5. ELECTRICITY CONSUMPTION VS PRODUCTION
# ==============================================================================
print("\n5. Creating Consumption vs Production Analysis...")

df_consumption = pd.read_csv('wikipedia_data/List of countries by electricity consumption_table_1.csv')

# Merge production and consumption for top 15
top_15_countries = df_production[df_production['Location'] != 'World'].head(15)['Location'].values

comparison_data = []
for country in top_15_countries:
    prod_row = df_production[df_production['Location'] == country]
    cons_row = df_consumption[df_consumption['Location'] == country]

    if not prod_row.empty and not cons_row.empty:
        production = float(prod_row.iloc[0]['Total (TWh)[1]'])
        consumption = float(cons_row.iloc[0]['Consumption (TWh per annum)'])
        comparison_data.append({
            'Country': country,
            'Production': production,
            'Consumption': consumption,
            'Net': production - consumption
        })

df_compare = pd.DataFrame(comparison_data)

fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(df_compare))
width = 0.35

bars1 = ax.bar(x - width/2, df_compare['Production'], width, label='Production', color='steelblue', alpha=0.8)
bars2 = ax.bar(x + width/2, df_compare['Consumption'], width, label='Consumption', color='coral', alpha=0.8)

ax.set_xlabel('Country', fontsize=12, weight='bold')
ax.set_ylabel('Electricity (TWh)', fontsize=12, weight='bold')
ax.set_title('Electricity Production vs Consumption - Top 15 Countries', fontsize=16, weight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(df_compare['Country'], rotation=45, ha='right')
ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig('charts/5_production_vs_consumption.png', dpi=300, bbox_inches='tight')
plt.close()

exporters = df_compare[df_compare['Net'] > 50].sort_values('Net', ascending=False)
importers = df_compare[df_compare['Net'] < -50].sort_values('Net')

findings.append({
    'title': 'Net Exporters vs Importers',
    'insight': f"Top exporters: {', '.join(exporters['Country'].head(3).values)}. Top importers: {', '.join(importers['Country'].head(3).values)}. This reflects energy independence strategies and cross-border electricity trade."
})

print("  ✓ Saved: charts/5_production_vs_consumption.png")

# ==============================================================================
# 6. PER CAPITA ENERGY CONSUMPTION
# ==============================================================================
print("\n6. Creating Per Capita Energy Consumption chart...")

df_per_capita = pd.read_csv('wikipedia_data/List of countries by energy consumption per capita_table_1.csv', skiprows=[0])

# Get 2022 data (column index 7)
df_per_capita_clean = df_per_capita[['Country/Territory', 'kgoe/a']].copy()
df_per_capita_clean.columns = ['Country', 'Consumption_kgoe']
df_per_capita_clean['Consumption_kgoe'] = pd.to_numeric(df_per_capita_clean['Consumption_kgoe'], errors='coerce')
df_per_capita_clean = df_per_capita_clean.dropna()
df_per_capita_clean = df_per_capita_clean.sort_values('Consumption_kgoe', ascending=False).head(20)

fig, ax = plt.subplots(figsize=(12, 10))
countries_pc = df_per_capita_clean['Country'].values
consumption_pc = df_per_capita_clean['Consumption_kgoe'].values

bars = ax.barh(countries_pc, consumption_pc, color='purple', alpha=0.7)
ax.set_xlabel('Energy Consumption Per Capita (kgoe/year)', fontsize=12, weight='bold')
ax.set_title('Top 20 Countries by Per Capita Energy Consumption (2022)', fontsize=16, weight='bold', pad=20)
ax.invert_yaxis()

for i, (bar, val) in enumerate(zip(bars, consumption_pc)):
    ax.text(val + 100, i, f'{val:,.0f}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('charts/6_per_capita_consumption.png', dpi=300, bbox_inches='tight')
plt.close()

findings.append({
    'title': 'Wealth Correlates with Energy Consumption',
    'insight': f"Top per capita consumers are wealthy nations and oil-rich states. {countries_pc[0]} leads with {consumption_pc[0]:,.0f} kgoe/year, vastly exceeding global average. High consumption reflects industrialization, climate, and lifestyle factors."
})

print("  ✓ Saved: charts/6_per_capita_consumption.png")

# ==============================================================================
# 7. ENERGY INTENSITY ANALYSIS
# ==============================================================================
print("\n7. Creating Energy Intensity Analysis...")

df_intensity = pd.read_csv('wikipedia_data/List of countries by energy intensity_table_1.csv')

# Get top 15 most and least efficient
df_intensity['Energy intensity'] = pd.to_numeric(df_intensity['Energy intensity'], errors='coerce')
df_intensity_clean = df_intensity.dropna(subset=['Energy intensity'])

most_intensive = df_intensity_clean.nlargest(15, 'Energy intensity')
least_intensive = df_intensity_clean.nsmallest(15, 'Energy intensity')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Most intensive (less efficient)
ax1.barh(most_intensive['Country'], most_intensive['Energy intensity'], color='red', alpha=0.6)
ax1.set_xlabel('Energy Intensity (MJ/$PPP)', fontsize=11, weight='bold')
ax1.set_title('Least Energy Efficient Economies', fontsize=14, weight='bold')
ax1.invert_yaxis()

# Least intensive (more efficient)
ax2.barh(least_intensive['Country'], least_intensive['Energy intensity'], color='green', alpha=0.6)
ax2.set_xlabel('Energy Intensity (MJ/$PPP)', fontsize=11, weight='bold')
ax2.set_title('Most Energy Efficient Economies', fontsize=14, weight='bold')
ax2.invert_yaxis()

plt.suptitle('Energy Efficiency: Energy Required per Dollar of GDP', fontsize=16, weight='bold', y=1.02)
plt.tight_layout()
plt.savefig('charts/7_energy_intensity.png', dpi=300, bbox_inches='tight')
plt.close()

findings.append({
    'title': 'Energy Efficiency Varies Dramatically',
    'insight': f"Most efficient economies (like {least_intensive.iloc[0]['Country']}) use advanced technology and service-based economies. Least efficient (like {most_intensive.iloc[0]['Country']}) reflect heavy industry, cold climates, or inefficient infrastructure."
})

print("  ✓ Saved: charts/7_energy_intensity.png")

# ==============================================================================
# 8. SOLAR VS WIND GROWTH LEADERS
# ==============================================================================
print("\n8. Creating Solar vs Wind Analysis...")

# Get countries with significant solar and wind
solar_wind_data = []
for idx, row in df_production[df_production['Location'] != 'World'].head(30).iterrows():
    country = row['Location']
    solar = float(row['Solar'])
    wind = float(row['Wind'])
    total = float(row['Total (TWh)[1]'])

    if solar > 1 or wind > 1:  # Only countries with meaningful production
        solar_wind_data.append({
            'Country': country,
            'Solar': solar,
            'Wind': wind,
            'Solar %': solar/total*100,
            'Wind %': wind/total*100
        })

df_sw = pd.DataFrame(solar_wind_data).sort_values('Solar', ascending=False).head(15)

fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(df_sw))
width = 0.35

bars1 = ax.bar(x - width/2, df_sw['Solar'], width, label='Solar', color='#FFA07A', alpha=0.8)
bars2 = ax.bar(x + width/2, df_sw['Wind'], width, label='Wind', color='#87CEEB', alpha=0.8)

ax.set_xlabel('Country', fontsize=12, weight='bold')
ax.set_ylabel('Production (TWh)', fontsize=12, weight='bold')
ax.set_title('Solar vs Wind Energy Production - Top Countries', fontsize=16, weight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(df_sw['Country'], rotation=45, ha='right')
ax.legend(fontsize=12)

plt.tight_layout()
plt.savefig('charts/8_solar_vs_wind.png', dpi=300, bbox_inches='tight')
plt.close()

findings.append({
    'title': 'Renewable Technology Choices Differ by Region',
    'insight': f"China leads in both solar ({df_sw.iloc[0]['Solar']:.0f} TWh) and wind. Solar dominates in sunny regions, wind in coastal/windy areas. This shows geographical and policy factors in renewable deployment."
})

print("  ✓ Saved: charts/8_solar_vs_wind.png")

# ==============================================================================
# SAVE FINDINGS
# ==============================================================================
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Created 8 focused visualization charts")
print(f"Extracted {len(findings)} key findings")
print(f"All charts saved to: charts/")
print("="*80)

# Save findings to JSON for README generation
import json
with open('charts/findings.json', 'w') as f:
    json.dump(findings, f, indent=2)

print("\n✓ Findings saved to: charts/findings.json")
print("\nReady to generate README presentation!")
