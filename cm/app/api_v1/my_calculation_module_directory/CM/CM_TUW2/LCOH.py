import os
import sys
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.
                                                       abspath(__file__))))
if path not in sys.path:
    sys.path.append(path)


def levelized_costs_of_heat(energy_demand, heat_load, energy_price,
                            specific_investment_cost, fix_o_and_m, var_o_and_m,
                            efficiency_heatingsystem, r, lt):
    '''
    This function calculates the levelized costs of heat (LCOH) in EUR/MWh for
    a residential building.
    TAX: Due to wide range of taxation methods and tax refunds in different
    countries, it is not considered here.
    Emissions: are not considered separately for the households. Depending on
    the country, it is sometimes indirectly included in the fuel costs.
    '''
    annuity = (r*(1+r)**lt)/((1+r)**lt - 1)
    # final energy demand
    fed = energy_demand / efficiency_heatingsystem
    # OPEX: Operational Expenditure
    OPEX = fix_o_and_m * heat_load + var_o_and_m * fed
    # CAPEX: Capital Expenditure
    CAPEX = heat_load * specific_investment_cost * annuity
    # energy costs
    energy_costs = fed * energy_price
    # total costs heat supply
    total_costs = OPEX + CAPEX + energy_costs
    # LCOH [EUR/MWh]
    lcoh = total_costs / energy_demand
    '''
    # costs per capita [€/capita]
    lcohcapita = total_costs / population
    '''
    output = {'Final energy demand': round(float(fed), 2),
              'Capital Expenditure (CAPEX)': round(float(CAPEX), 2),
              'Operational Expenditure (OPEX)': round(float(OPEX), 2),
              'Energy costs': round(float(energy_costs), 2),
              'Total costs': round(float(total_costs), 2),
              'Levelized costs of heat': round(float(lcoh), 2)}
    return output
