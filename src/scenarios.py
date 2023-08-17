
# Get hardcoded values from config file
k_net_income = get_config('k_net_income')
r_net_income = get_config('r_net_income')

k_crop_yield = get_config('k_crop_yield')
r_crop_yield = get_config('r_crop_yield')
k_crc = get_config('k_crc')
r_crc = get_config('r_crc')

no_hh = get_config('no_hh')
no_cattle_perhh = get_config('no_cattle_perhh')
profit_per_cattle = get_config('profit_per_cattle')
wr_cattle_day = get_config('wr_cattle_day')
fr_cattle_day = get_config('fr_cattle_day')
fraction_residue_fodder = get_config('fraction_residue_fodder')
fraction_produce_fodder = get_config('fraction_produce_fodder')
mass_manure_per_cattle_per_year = get_config('mass_manure_per_cattle_per_year') #tonnes

k_cwr_mm = get_config('k_cwr_mm')
r_cwr_mm = get_config('r_cwr_mm')

soil_density = get_config('soil_density')
height_topsoil = get_config('height_topsoil')
perc_OM_target = get_config('perc_OM_target')
perc_OM_depleted = get_config('perc_OM_depleted')


total_water_available = get_config('total_water_available')


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
    return (wr_cattle_day*365/(1e3*1e6)) #mcm

def fr_cattle_year(fr_cattle_day):
    return (fr_cattle_day*365/(1e3)) #tonnes

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

# Calculate dynamic values
k_area = fcall()
r_area = fcall()
netsownarea = k_area
fodder_deficit = fodder_deficit(total_fodder_available,fr_all_cattle)
