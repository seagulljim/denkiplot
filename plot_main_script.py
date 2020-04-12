import csv
import os
import plot_defs as pdefs
import other_functions as of

folder = '2020-04-12'
outputs_folder = os.path.join(folder, 'outputs')

# Make outputs folder if it doesn't exist
if not os.path.exists(outputs_folder):
    print('no')
    os.mkdir(outputs_folder)

symbols = ['capacity_factor',
           'generator_life',
           'generator_capex',
           'operating_profit_per_MW',
           'energy_provided_by_technology_percentage',
           'cost_vom',
           'units_built',
           ]

cases = []
with open(os.path.join(folder, 'list_of_cases.csv'), newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        cases.append(row[0])

# Graphs where each case is shown in one figure
cases_in_scenario = cases[:4]
name = 'central'
# pdefs.plot_unserved_hours(folder, outputs_folder, cases_in_scenario, name)
# pdefs.plot_average_price(folder, outputs_folder, cases_in_scenario, name)

cases_in_scenario = cases[4:8]
name = 'step_change'
# pdefs.plot_unserved_hours(folder, outputs_folder, cases_in_scenario, name)
# pdefs.plot_average_price(folder, outputs_folder, cases_in_scenario, name)

# Graphs where each case is shown in a separate figure
for case in cases:

    # Path to the GDX files
    gdx_dispatch_location = os.path.join(folder, case, 'output_dispatch.gdx')
    gdx_results_location = os.path.join(folder, case, 'output_results.gdx')

    generator_df = of.combine_gen_data_t(gdx_results_location, symbols)
    generator_df = of.is_tech_existing(generator_df)
    generator_df = of.calc_irr(generator_df)
    generator_df = of.get_generator_properties(generator_df)
    generator_df['capacity_factor'] = 100 * generator_df['capacity_factor']
    generator_df['energy_provided_by_technology_percentage'] \
        = 100 * generator_df['energy_provided_by_technology_percentage']
    generator_df = generator_df.sort_values(by=['Rank'], ascending=True)
    generator_df = generator_df.set_index("technologies")

    generator_df.to_csv(os.path.join(folder, 'generator_df_' + case + '.csv'))
    # dispatch schedule: power and price
    hours = [1, 120]
    # pdefs.plot_dispatch_and_price(hours, case, gdx_dispatch_location,
                                  # outputs_folder, generator_df)
    # pdefs.plot_committed_capacity(hours, case, gdx_dispatch_location,
                                  # outputs_folder, generator_df)

    # Plot price duration curve
    pdefs.plot_price_duration_curve(folder, case, outputs_folder)

    # profit and IRR
    pdefs.plot_operating_profit(outputs_folder, case, generator_df)
    pdefs.plot_irr(outputs_folder, case, generator_df)

    # Capacity Factor
    pdefs.plot_capacity_factor(outputs_folder, case, generator_df)
    pdefs.plot_energy_percentage(outputs_folder, case, generator_df)
