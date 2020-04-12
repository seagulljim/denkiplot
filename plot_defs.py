import os
import gdxpds
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
import plotting_tools as ptools

# Set the style
plt.style.use(ptools.seaborn_style)


def plot_price_duration_curve(folder, case, outputs_folder):
    """Plots the price duration curve for case ans savesit to outputs folder"""

    gdx_dispatch_location = os.path.join(folder, case, 'output_dispatch.gdx')
    dispatch_df = gdxpds.to_dataframes(gdx_dispatch_location)

    price = dispatch_df['post_energy_price']
    price = price.filter(items=['hours', 'Value'])
    price['hours'] = price['hours'].astype(int)

    price = price.fillna(value=0)
    y_sort = price.sort_values(by=['Value'], ascending=False)
    x = range(0, len(y_sort))
    l_y = y_sort['Value']

    f, (ax1, ax2) = plt.subplots(ncols=1, nrows=2, sharex=True)
    sns.lineplot(x=x, y=l_y, ax=ax1, color=ptools.lineplot_colour)
    sns.lineplot(x=x, y=l_y, ax=ax2, color=ptools.lineplot_colour)

    ax1.set_ylim(13000, 15000)
    ax2.set_ylim(-275, 275)
    ax1.set_xlim(0, 8760)
    ax2.set_xlim(0, 8760)
    # ax1.set_xticks([])  # Turns off xticks on the upper plot

#   Add '$' to the yaxis
    fmt = '${x:,.0f}'
    tick = ticker.StrMethodFormatter(fmt)
    ax1.yaxis.set_major_formatter(tick)
    ax2.yaxis.set_major_formatter(tick)

    ax1.set(ylabel='Energy Price ($/MWh)                                    ')
    ax2.set(ylabel='')
    plt.xlabel('Hours')
    plt.subplots_adjust(wspace=0, hspace=0.03)

    filename = 'price_duration_curve_' + case + '.png'
    save_loc = os.path.join(outputs_folder, filename)
    plt.savefig(save_loc, bbox_inches="tight")
    plt.clf()
    print("Plotted price duration curve for", case)


def plot_average_price(folder, outputs_folder, cases_in_scenario, name):
    """Plots the average price for the cases in cases_in_scenario"""

    y = []
    x = [1, 2, 3, 4]

    for case in cases_in_scenario:
        gdx_results_location = os.path.join(folder, case, 'output_results.gdx')

        dataframes = gdxpds.to_dataframes(gdx_results_location)

        av_price_df = dataframes['volume_weighted_energy_price']
        av_price_df = av_price_df.filter(items=['Value'])
        y.append(av_price_df['Value'][0])

    plt.figure(figsize=(5, 5))
    ax = sns.barplot(x=x, y=y, color=ptools.barplot_colour)
    plt.xlabel('Volume Weighted Average Price ($/MWh)')

#   Add '$' to the yaxis
    ax = plt.gca()
    fmt = '${x:,.0f}'
    tick = ticker.StrMethodFormatter(fmt)
    ax.yaxis.set_major_formatter(tick)

    save_loc = os.path.join(outputs_folder, 'average_price_' + name + '.png')
    plt.savefig(save_loc)
    plt.clf()
    print("Plotted average price")


def plot_unserved_hours(folder, outputs_folder, cases_in_scenario, name):
    """Plots the hours of unserved (LOR) for the cases in cases_in_scenario"""

    y = []
    x = [1, 2, 3, 4]

    for case in cases_in_scenario:
        gdx_results_location = os.path.join(folder, case, 'output_results.gdx')

        dataframes = gdxpds.to_dataframes(gdx_results_location)

        unserved_df = dataframes['hours_of_unserved']
        unserved_df = unserved_df.filter(items=['Value'])
        y.append(unserved_df['Value'][0])

    plt.figure(figsize=(5, 5))
    sns.barplot(x=x, y=y, color=ptools.barplot_colour)
    plt.ylabel('Hours of LOR')

    save_loc = os.path.join(outputs_folder, 'unserved_' + name + '.png')
    plt.savefig(save_loc)
    plt.clf()
    print("Plotted hours of LOR")


def plot_irr(outputs_folder, case, generator_df):
    """Plots the IRR for case"""

    irrfig = sns.barplot(x="Name", y="IRR", data=generator_df,
                         palette=generator_df['colour2'].tolist())
    plt.ylabel('Internal Rate of Return')
    plt.xlabel('')

    irrfig.set_xticklabels(irrfig.get_xticklabels(), rotation=90)
    irrfig.axhline(0, color='black')

    irrfig.axhline(10, color='black', linestyle='--')

    ax = plt.gca()
    ax.set_ylim(-20, 20)

    filename = 'irr_' + case + '.png'
    save_loc = os.path.join(outputs_folder, filename)
    plt.savefig(save_loc, bbox_inches="tight")
    plt.clf()
    print("Plotted IRR for", case)


def plot_operating_profit(outputs_folder, case, generator_df):
    """Plots the operating profit"""

    opfig = sns.barplot(x="Name", y="operating_profit_per_MW",
                        data=generator_df,
                        palette=generator_df['colour2'].tolist())
    plt.ylabel('Operating Profit (per MW)')
    plt.xlabel('')
    opfig.set_xticklabels(opfig.get_xticklabels(), rotation=90)

    opfig.axhline(0, color='black')

#   Add '$' to the yaxis
    fmt = '${x:,.0f}'
    tick = ticker.StrMethodFormatter(fmt)
    opfig.yaxis.set_major_formatter(tick)

    filename = 'operating_profit_' + case + '.png'
    save_loc = os.path.join(outputs_folder, filename)
    plt.savefig(save_loc, bbox_inches="tight")
    plt.clf()
    print("Plotted operating profit per MW for", case)


def plot_capacity_factor(outputs_folder, case, generator_df):
    """Plots the capacity factor"""

    cffig = sns.barplot(x="Name", y="capacity_factor",
                        data=generator_df,
                        palette=generator_df['colour2'].tolist())
    plt.ylabel('Capacity Factor (%)')
    plt.xlabel('')
    cffig.set_xticklabels(cffig.get_xticklabels(), rotation=90)

    filename = 'capacity_factor_' + case + '.png'
    save_loc = os.path.join(outputs_folder, filename)
    plt.savefig(save_loc, bbox_inches="tight")
    plt.clf()
    print("Plotted capacity factor for", case)


def plot_energy_percentage(outputs_folder, case, generator_df):
    """Plots the capacity factor"""

    cffig = sns.barplot(x="Name", y="energy_provided_by_technology_percentage",
                        data=generator_df,
                        palette=generator_df['colour2'].tolist())
    plt.ylabel('Energy (%)')
    plt.xlabel('')
    cffig.set_xticklabels(cffig.get_xticklabels(), rotation=90)

    filename = 'energy_percentage_' + case + '.png'
    save_loc = os.path.join(outputs_folder, filename)
    plt.savefig(save_loc, bbox_inches="tight")
    plt.clf()
    print("Plotted energy percentage for", case)


def plot_dispatch_and_price(hours, case, gdx_dispatch_location,
                            outputs_folder, generator_df):
    """Plots the price and dispatch for case for the start and stop hours
    contained in hours
    """

    dispatch_df = gdxpds.to_dataframes(gdx_dispatch_location)

    power = dispatch_df['post_power_from_technology']
    power = power.filter(items=['hours', 'technologies', 'Value'])
    power['hours'] = power['hours'].astype(int)

    power = power[power['hours'] >= hours[0]]
    power = power[power['hours'] <= hours[1]]
    t = power.pivot(index='hours', columns='technologies', values='Value')
    t = t.fillna(0)

    # Arranges the technologies based on Rank in generator_df
    cols = t.columns.tolist()
    col_order = []
    for col in cols:
        rank = generator_df['Rank'][col]
        col_order.append(rank)

    colsnew = [x for _, x in sorted(zip(col_order, cols),
               key=lambda pair: pair[0])]
    t = t[colsnew]

    # Get the colour and name
    cols = t.columns.tolist()
    colour = []
    name = []
    for col in cols:
        colour.append(generator_df['colour1'][col])
        name.append(generator_df['Name'][col])

    price = dispatch_df['post_energy_price']
    price = price.filter(items=['hours', 'Value'])
    price['hours'] = price['hours'].astype(int)
    price = price[price['hours'] >= hours[0]]
    price = price[price['hours'] <= hours[1]]

    plt.figure(figsize=(15, 5))
    ax = plt.gca()
    t.plot(kind='area', stacked=True, ax=ax, color=colour, label=name)
    plt.ylabel('Dispatch (MW)')
    plt.xlabel('Hours')

    price.plot(x='hours', y='Value', secondary_y=True, ax=ax,
               label='Energy Price', color='black')
    ax.set_xlim(hours[0], hours[1])
    plt.ylabel('Energy Price ($/MWh)')
    plt.xlabel('Hours')

    print("$s on ytick label and xlabel (Hours) are not working")
    print("ALso can't get legend to work")

    # Not sure how to get $s on the secondary axis
    # fmt = '${x:,.0f}'
    # tick = ticker.StrMethodFormatter(fmt)
    # ax.set_major_formatter(tick)

    filename = 'dispatch_' + case + '.png'
    save_loc = os.path.join(outputs_folder, filename)
    plt.savefig(save_loc)
    plt.clf()

    print("Plotted dispatch and energy price for", case)


def plot_committed_capacity(hours, case, gdx_dispatch_location,
                            outputs_folder, generator_df):
    """Plots the price and dispatch for case for the start and stop hours
    contained in hours
    """

    dispatch_df = gdxpds.to_dataframes(gdx_dispatch_location)

    power = dispatch_df['post_committed_capacity_in_scenario']
    power = power.filter(items=['hours', 'technologies', 'Value'])
    power['hours'] = power['hours'].astype(int)

    power = power[power['hours'] >= hours[0]]
    power = power[power['hours'] <= hours[1]]
    t = power.pivot(index='hours', columns='technologies', values='Value')
    t = t.fillna(0)

    # Arranges the technologies based on Rank in generator_df
    cols = t.columns.tolist()
    col_order = []
    for col in cols:
        rank = generator_df['Rank'][col]
        col_order.append(rank)

    colsnew = [x for _, x in sorted(zip(col_order, cols),
               key=lambda pair: pair[0])]
    t = t[colsnew]

    # Get the colour and name
    cols = t.columns.tolist()
    colour = []
    name = []
    for col in cols:
        colour.append(generator_df['colour1'][col])
        name.append(generator_df['Name'][col])

    price = dispatch_df['post_energy_price']
    price = price.filter(items=['hours', 'Value'])
    price['hours'] = price['hours'].astype(int)
    price = price[price['hours'] >= hours[0]]
    price = price[price['hours'] <= hours[1]]

    plt.figure(figsize=(15, 5))
    ax = plt.gca()
    t.plot(kind='area', stacked=True, ax=ax, color=colour, label=name)
    plt.ylabel('Committed Capacity (MW)')
    plt.xlabel('Hours')

    price.plot(x='hours', y='Value', secondary_y=True, ax=ax,
               label='Energy Price', color='black')
    ax.set_xlim(hours[0], hours[1])
    plt.ylabel('Energy Price ($/MWh)')
    plt.xlabel('Hours')

    print("$s on ytick label and xlabel (Hours) are not working")
    print("ALso can't get legend to work")

    # Not sure how to get $s on the secondary axis
    # fmt = '${x:,.0f}'
    # tick = ticker.StrMethodFormatter(fmt)
    # ax.set_major_formatter(tick)

    filename = 'units_committed_' + case + '.png'
    save_loc = os.path.join(outputs_folder, filename)
    plt.savefig(save_loc)
    plt.clf()

    print("Plotted committed capacity for", case)
