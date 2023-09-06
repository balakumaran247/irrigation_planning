from src.gee import get_ag_area, get_fc_area
from src.config import baseline, scenario1

# Define functions
def k_income(k_area,k_net_income):
    return (k_area*k_net_income) #Rs

def r_income(r_area,r_net_income):
    return (r_area*r_net_income) #Rs

def total_crop_produce(k_area,k_crop_yield,r_area,r_crop_yield):
    return (k_area*k_crop_yield+r_area*r_crop_yield) #tonnes

def total_crop_residue(k_area,k_crc,r_area,r_crc):
    return (k_area*k_crc+r_area*r_crc) #tonnes

def no_cattle(no_hh,no_cattle_perhh):
    return (no_hh*no_cattle_perhh) #no

def wr_cattle_year(wr_cattle_day):
    return ((wr_cattle_day*365)/(1e3*1e6)) #mcm

def fr_cattle_year(fr_cattle_day):
    return ((fr_cattle_day*365)/(1e3)) #tonnes

def wr_all_cattle(wr_cattle_year,no_cattle):
    return (wr_cattle_year*no_cattle)  #mcm

def fr_all_cattle(fr_cattle_year,no_cattle):
    return (fr_cattle_year*no_cattle)  #tonnes

def fraction_residue_leaf_manure(fraction_residue_fodder):
    return (1- fraction_residue_fodder) #tonnes

def total_fodder_available(total_crop_produce,fraction_crop_fodder,total_crop_residue,fraction_residue_fodder):
    return (total_crop_produce*fraction_crop_fodder+total_crop_residue*fraction_residue_fodder) #tonnes

def total_fodder_as_cattle_manure(no_cattle,mass_manure_per_cattle_per_year):
    return (no_cattle*mass_manure_per_cattle_per_year) #tonnes

def k_cwr_mcm(k_area,k_cwr_mm):
    return (k_area*1e4*k_cwr_mm*1e-3/1e6) #mcm

def r_cwr_mcm(r_area,r_cwr_mm):
    return (r_area*1e4*r_cwr_mm*1e-3/1e6) #mcm

def cwr_crop_cattle(wr_all_cattle,k_cwr_mcm,r_cwr_mcm):
    return (wr_all_cattle*k_cwr_mcm+r_cwr_mcm) #mcm

def water_deficit(total_water_available,cwr_crop_cattle):
    return (total_water_available-cwr_crop_cattle) #mcm

def fodder_deficit(total_fodder_available,fr_all_cattle):
    return (total_fodder_available-fr_all_cattle) #tonnes

def mass_soil(soil_density,height_topsoil):
    return (soil_density*height_topsoil*1e4) #kg/ha

def mass_OM(mass_soil,perc_OM_target):
    return (mass_soil*perc_OM_target/100) #kg/ha

def mass_OM_depleted(mass_OM,perc_OM_depleted):
    return (mass_OM*perc_OM_depleted/100) #kg/ha

def total_mass_OM_depleted(k_area,r_area,mass_OM_depleted):
    return (k_area*mass_OM_depleted+r_area*mass_OM_depleted) #kg/ha

def total_crop_residue_as_OM(fodder_deficit,fraction_residue_fodder,total_crop_residue):
    return (fodder_deficit+(fraction_residue_fodder*total_crop_residue)) #tonnes

def cattle_income(no_cattle,profit_per_cattle):
    return (no_cattle*profit_per_cattle) #Rs

def kharif_crops(k_area, scenario):
    return [('Paddy', f'{round(k_area, 2)} ha')] if scenario == 'baseline' else [('Cotton', f'{round(k_area, 2)} ha')]

def rabi_crops(r_area, scenario):
    return [('Millet', f'{round(r_area, 2)} ha')] if scenario == 'baseline' else [('Ragi', f'{round(r_area, 2)} ha')]

def kharif_iwr_mm_list(k_cwr_mm, rain_mm, scenario):
    if scenario == 'baseline':
        return [('Paddy', k_cwr_mm), ('Rainfall', rain_mm), ('IWR', k_cwr_mm-rain_mm)]
    else:
        return [('Cotton', k_cwr_mm), ('Rainfall', rain_mm), ('IWR', k_cwr_mm-rain_mm)]

def rabi_iwr_mm_list(r_cwr_mm, rain_mm, scenario):
    if scenario == 'baseline':
        return [('Millet', r_cwr_mm), ('Rainfall', rain_mm), ('IWR', r_cwr_mm-rain_mm)]
    else:
        return [('Ragi', r_cwr_mm), ('Rainfall', rain_mm), ('IWR', r_cwr_mm-rain_mm)]

def scenarios(scenario, name):
    get_config = baseline if scenario == 'baseline' else scenario1
    # Get hardcoded values from config file
    k_net_income = get_config['k_net_income']
    r_net_income = get_config['r_net_income']
    k_crop_yield = get_config['k_crop_yield']
    r_crop_yield = get_config['r_crop_yield']
    k_crc = get_config['k_crc']
    r_crc = get_config['r_crc']
    no_hh = get_config['no_hh']
    no_cattle_perhh = get_config['no_cattle_perhh']
    profit_per_cattle = get_config['profit_per_cattle']
    wr_cattle_day = get_config['wr_cattle_day']
    fr_cattle_day = get_config['fr_cattle_day']
    fraction_residue_fodder = get_config['fraction_residue_fodder']
    fraction_produce_fodder = get_config['fraction_produce_fodder']
    mass_manure_per_cattle_per_year = get_config['mass_manure_per_cattle_per_year'] #tonne]
    k_cwr_mm = get_config['k_cwr_mm']
    r_cwr_mm = get_config['r_cwr_mm']
    soil_density = get_config['soil_density']
    height_topsoil = get_config['height_topsoil']
    perc_OM_target = get_config['perc_OM_target']
    perc_OM_depleted = get_config['perc_OM_depleted']
    total_water_available = get_config['total_water_available']
    # get dynamic values
    geom_area = get_fc_area(name)
    k_area = get_config['k_area'] or get_ag_area('kharif', 'raichurCCA')/1e4
    r_area = get_config['r_area'] or get_ag_area('rabi', 'raichurCCA')/1e4
    k_rain_mm = 300
    r_rain_mm = 100
    # execute the defined functions
    k_crops = kharif_crops(k_area, scenario)
    r_crops = rabi_crops(r_area, scenario)
    k_iwr_list = kharif_iwr_mm_list(k_cwr_mm, k_rain_mm, scenario)
    r_iwr_list = rabi_iwr_mm_list(r_cwr_mm, r_rain_mm, scenario)
    k_incom = k_income(k_area, k_net_income)
    r_incom = r_income(r_area, r_net_income)
    total_cr_produce = total_crop_produce(k_area, k_crop_yield, r_area, r_crop_yield)
    total_cr_residue = total_crop_residue(k_area, k_crc, r_area, r_crc)
    no_cattl = no_cattle(no_hh, no_cattle_perhh)
    wr_cattle_yr = wr_cattle_year(wr_cattle_day)
    fr_cattle_yr = fr_cattle_year(fr_cattle_day)
    wr_all_cattl = wr_all_cattle(wr_cattle_yr, no_cattl)
    fr_all_cattl = fr_all_cattle(fr_cattle_yr, no_cattl)
    fr_res_leaf_manure = fraction_residue_leaf_manure(fraction_residue_fodder)
    tot_fdr_avail = total_fodder_available(total_cr_produce, fraction_produce_fodder, total_cr_residue, fraction_residue_fodder)
    tot_fdr_cat_manur = total_fodder_as_cattle_manure(no_cattl, mass_manure_per_cattle_per_year)
    k_cwr_mcm_var = k_cwr_mcm(k_area, k_cwr_mm)
    r_cwr_mcm_var = r_cwr_mcm(r_area, r_cwr_mm)
    cwr_cr_cat = cwr_crop_cattle(wr_all_cattl, k_cwr_mcm_var, r_cwr_mcm_var)
    wt_def = water_deficit(total_water_available, cwr_cr_cat)
    fdr_def = fodder_deficit(tot_fdr_avail, fr_all_cattl)
    soil_mass = mass_soil(soil_density, height_topsoil)
    om_mass = mass_OM(soil_mass, perc_OM_target)
    mass_om_dep = mass_OM_depleted(om_mass, perc_OM_depleted)
    tot_mass_om_dep = total_mass_OM_depleted(k_area, r_area, mass_om_dep)
    tot_cr_res_as_om = total_crop_residue_as_OM(fdr_def, fraction_residue_fodder, total_cr_residue)
    cat_inc = cattle_income(no_cattl, profit_per_cattle)
    
    return {
        'geom_area': f'{round(geom_area, 2)} ha',
        'k_area': f'{round(k_area, 2)} ha',
        'r_area': f'{round(r_area, 2)} ha',
        'k_crops': k_crops,
        'r_crops': r_crops,
        'k_rain_mm': k_rain_mm,
        'r_rain_mm': r_rain_mm,
        'k_iwr_list': k_iwr_list,
        'r_iwr_list': r_iwr_list,
        'netsownarea': k_area,
        'k_net_income': k_net_income,
        'r_net_income': r_net_income,
        'k_crop_yield': k_crop_yield,
        'r_crop_yield': r_crop_yield,
        'k_crc': k_crc,
        'r_crc': r_crc,
        'no_hh': no_hh,
        'no_cattle_perhh': no_cattle_perhh,
        'profit_per_cattle': profit_per_cattle,
        'wr_cattle_day': wr_cattle_day,
        'fr_cattle_day': fr_cattle_day,
        'fraction_residue_fodder': fraction_residue_fodder,
        'fraction_produce_fodder': fraction_produce_fodder,
        'mass_manure_per_cattle_per_year': mass_manure_per_cattle_per_year,
        'k_cwr_mm': k_cwr_mm,
        'r_cwr_mm': r_cwr_mm,
        'soil_density': soil_density,
        'height_topsoil': height_topsoil,
        'perc_OM_target': perc_OM_target,
        'perc_OM_depleted': perc_OM_depleted,
        'total_water_available': total_water_available,
        'k_income': k_incom,
        'r_income': r_incom,
        'total_crop_residue': total_cr_residue,
        'total_crop_produce': total_cr_produce,
        'no_cattle': no_cattl,
        'wr_cattle_year': wr_cattle_yr,
        'fr_cattle_year': fr_cattle_yr,
        'wr_all_cattle': wr_all_cattl,
        'fr_all_cattle': fr_all_cattl,
        'fraction_residue_leaf_manure': fr_res_leaf_manure,
        'total_fodder_available': tot_fdr_avail,
        'total_fodder_as_cattle_manure': tot_fdr_cat_manur,
        'k_cwr_mcm': k_cwr_mcm_var,
        'r_cwr_mcm': r_cwr_mcm_var,
        'cwr_crop_cattle': cwr_cr_cat,
        'water_deficit': wt_def,
        'fodder_deficit': fdr_def,
        'mass_soil': soil_mass,
        'mass_OM': om_mass,
        'mass_OM_depleted': mass_om_dep,
        'total_mass_OM_depleted': tot_mass_om_dep,
        'total_crop_residue_as_OM': tot_cr_res_as_om,
        'cattle_income': cat_inc,
    }
