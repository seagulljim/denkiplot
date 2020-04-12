import gdxpds
import numpy_financial as npf
import pandas as pd


def combine_gen_data_t(gdx_location, symbols):
    """Extracts the data from the gdx file (gdx_location) and extracts the
    list of symbols.  This currently is designed for generators with no other
    index.  It would be good to expand it to handle any generalised set of
    parameters.
    """

    loc_sym = symbols.copy()  # Make this new version for the local script

    # Create the df with the 0th symbol, as no need to merge at this point
    generator_df = gdxpds.to_dataframe(gdx_location, symbol_name=loc_sym[0])
    generator_df = generator_df[loc_sym[0]]
    generator_df = generator_df.rename(columns={"technologies": "technologies",
                                                "Value": loc_sym[0]})
    loc_sym.pop(0)  # Remove symbol 0 as already extracted

    for symbol in loc_sym:
        temp_df = gdxpds.to_dataframe(gdx_location, symbol_name=symbol)
        temp_df = temp_df[symbol]
        temp_df = temp_df.rename(columns={"technologies": "technologies",
                                          "Value": symbol})
        generator_df = pd.merge(generator_df, temp_df, on='technologies',
                                how='left')

    generator_df = generator_df[generator_df['units_built'].notna()]
    generator_df = generator_df.set_index("technologies")
    return generator_df


def is_tech_existing(generator_df):
    """Quick function to identify if a unit has existing in its name.  """

    t_new = []
    for tech in generator_df.index.values:
        if 'extg' not in tech:
            t_new.append(True)
        else:
            t_new.append(False)
    generator_df['New Build'] = t_new
    return generator_df


def calc_irr(generator_df):
    """Calculates the IRR of each technology based on life, operating profit,
    and capex
    """

    d_irr = []
    generator_df = generator_df.fillna(value=0)
    for tech in generator_df.index.values:
        cfs = [-1 * generator_df.loc[tech, 'generator_capex']] \
              + [generator_df.loc[tech, 'operating_profit_per_MW']] \
              * generator_df.loc[tech, 'generator_life'].astype(int)
        irr = npf.irr(cfs)
        irr = round(irr * 100, 2)
        d_irr.append(irr)
        print(tech, irr)
    generator_df['IRR'] = d_irr
    return generator_df


def get_generator_properties(df=0):
    """Gets a file that has generator properties, i.e. their proper name,
    the colour to be used for plotting them and so on.
    """

    path_to_properties_file = "other_files\\generator_properties.csv"
    generator_properties = pd.read_csv(path_to_properties_file, delimiter=',')
    if type(df) == int:
        return generator_properties
    else:
        new_df = pd.merge(df, generator_properties,
                          on='technologies', how='left')
        return new_df
