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
    This function calculates the levelized costs of heat (LCOH) in EUR/kWh for
    a residential building.
    TAX: Due to wide range of taxation methods and tax refunds in different
    countries, it is not considered here.
    Emissions: are not considered separately for the households. Depending on
    the country, it is sometimes indirectly included in the fuel costs.
    energy_demand [kWh]
    heat_load [kW]
    energy_price [EUR/kWh]
    specific_investment_cost [EUR/kW]
    fix_o_and_m [EUR/kW]
    var_o_and_m [EUR/kWh]
    LCOH [EUR/MWh]
    '''
    r = float(r)
    lt = float(lt)
    q = 1 + r
    assert q != 0 or q != 1 ,"Error in calculation annuity factor ! Please choose an other interest rate."
    annuity_factor = (1-q**lt)/(q**lt*(1-q))

    # final energy demand
    if efficiency_heatingsystem == 0:
        fed = efficiency_heatingsystem
    else:
        fed = float(energy_demand) / float(efficiency_heatingsystem)

    # OPEX: Operational Expenditure (EUR)
    OPEX = float(fix_o_and_m) * float(heat_load) + float(var_o_and_m) * float(fed)

    # CAPEX: Capital Expenditure (EUR)
    CAPEX = float(heat_load) * float(specific_investment_cost) 
    # energy costs (EUR)
    energy_costs = float(fed) * float(energy_price)
    # total costs heat supply (EUR)
    present_value = float(annuity_factor) * (float(OPEX) + float(energy_costs)) + float(CAPEX)
    # LCOH [EUR/MWh]
    if energy_demand == 0:
        lcoh = 0
    else:
        # kWh to MWh
        lcoh = float(present_value) / (float(energy_demand) * float(annuity_factor)) * 1000
    '''
    # costs per capita [€/capita]
    lcohcapita = total_costs / population
    '''

    output = {'Final energy demand': round(float(fed), 2),
              'Capital Expenditure (CAPEX)': round(float(CAPEX), 2),
              'Operational Expenditure (OPEX)': round(float(OPEX), 2),
              'Energy costs': round(float(energy_costs), 2),
              'Present Value': round(float(present_value), 2),
              'Levelized costs of heat': round(float(lcoh), 2)}
    return output
