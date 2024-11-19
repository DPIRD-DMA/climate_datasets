# Climate datasets
A one-stop-shop for climate data

We have explored and source several datasets to investigate their suitability for this work but also potentially for other use case/applications that require climate & weather data, soil & landscape data as well as future climate scenarios data. Data format, availability, resolution and methodologies vary and we have added links and references to detailed/technical information of the datasets.

| Dataset | Resolution | Format | Variables | Method | Access Conditions | Temporal Coverage |
|----------|----------|----------|-------------|-----------|----------|----------|
| DPIRD | station observations (\~200 stations) | web, json, csv | Time series data - Evaporation, rainfall, solar radiation, air temperature, and others | *Ad hoc* handling of technical issues and missing values | Some support is provided to patch missing data | Minute to yearly intervals |
| SILO (BOM) | station observations (\~8000 stations) | web, json, csv, apsim | Continuous daily time series Evaporation, rainfall, solar radiation, air temperature, and others | Observational records or interpolated estimates for missing records | Accessible via SILO network | daily, from 1889 to current year |
| SILO Gridded Data | \~5 km² | NetCDF, GeoTiff | Evaporation, rainfall, solar radiation, air temperature, and others | Gridded daily climate surfaces derived either by splining or kriging the observational data | Valid email required | Daily, monthly, yearly |
| ANUClimate 2.0 | \~1 km² | NetCDF | Evaporation, rainfall, solar radiation, air temperature, and others | Derived from observational records, ANUSPLIN Version 4.6 spatial models | NCI account and membership of the research project | At least daily, from 1970 to present |
| AGCD v1.0.1 | \~1 km², \~5 km² | NetCDF | Rainfall, air temperature, vapour pressure | Consistent temporal and spatial analyses across Australia | NCI account and membership of the research project | Daily |
| AGCD v2.0.1 | \~1 km², \~5 km² | NetCDF | Monthly rainfall | Updated version of AGCD v1.0.1 | NCI account and membership of the research project | monthly, from 1900 to 2022 inclusive |
| Chelseaclim | \~1 km² | GeoTIFF | Atmosphere, Air Temperature, Precipitation | Combines mechanistic and statistical downscaling of GCMs | CC BY 4.0, with credit to sources | 1979-01 to 2013-12 |
| NASA POWER | \~111 km², \~55 km² x \~69 km² | NetCDF, AWS Bucket | Solar and meteorological data sets for support of renewable energy, building energy efficiency and agricultural needs | Derived from NASA research for renewable energy, building energy efficiency, and agricultural needs | Free and publicly accessible | Varies, includes near-real time |
| WorldClim | Up to \~1 km² | GeoTiff | Temperature, precipitation, solar radiation, wind speed, water vapour pressure, bioclimatic variables | Historical and future climate scenarios | Free for ecological modelling and GIS | 1970-2000 |
