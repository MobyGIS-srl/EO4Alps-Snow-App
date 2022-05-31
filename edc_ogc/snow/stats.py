
import numpy as np
import matplotlib.pyplot as plt
import snow.dem_utils as du
from moby_report.manager import PdfManager
from moby_report.element import *
import xarray as xr
from xrspatial import aspect, slope, zonal_stats, zonal_crosstab


def reclass_aspect(x, n_class=4):
    dg = 360 // n_class
    return ((x + dg/2) // dg) - (x // (360 -dg/2)) * n_class


def format_altitude_range(z, dz):
    z_min = z % 100 * dz
    return f"{z_min:.0f} - {z_min + dz:.0f}"


def format_aspect(a):
    asp_zones = {0: 'Flat areas', 1: 'North slopes', 2: 'East slopes', 3: 'South slopes', 4: "West slopes"}
    return asp_zones[a // 100]


def compute_snow_stats(dem, snow, dz=500, flat=3):

    slope, aspect = du.horneslope(dem, 250)
    elev_class = dem // dz
    slope_class = np.where(slope > flat, 1, 0)
    aspect_class = reclass_aspect(aspect, 4)
    aspect_class = slope_class * (aspect_class + 1)

    # TODO: decomment aspect class
    snow_class = elev_class + (aspect_class * 100)



    # da_dem = xr.DataArray(dem, dims=['y', 'x'], name='raster')
    # aspect_agg = aspect(da_dem)
    # aspect_class = reclass_aspect(aspect_agg, 4)
    # slope_agg = slope(da_dem)

    zones = xr.DataArray(snow_class, dims=['y', 'x'], name='Z')
    values = xr.DataArray(snow, dims=['y', 'x'], name='SWE')

    # Calculate Stats with dask backed xarray DataArrays
    stats_df = zonal_stats(zones=zones, values=values, stats_funcs=['mean', 'sum', 'count'])
    stats_df['aspect'] = stats_df['zone'].apply(format_aspect)
    stats_df['altitude'] = stats_df['zone'].apply(format_altitude_range, args=[dz])

    stats_df = stats_df[['aspect', 'altitude', 'mean', 'sum', 'count']]

    print(stats_df)

    # df_mean = stats_df.set_index(['aspect', 'altitude'])['mean']
    # df_mean.unstack('aspect')

    # crosstab_df = zonal_crosstab(zones, zones2)
    # print(crosstab_df)

    # fig, axs = plt.subplots(2, 2)
    # axs[0, 0].imshow(elev_class)
    # axs[0, 1].imshow(aspect_class)
    # axs[1, 0].imshow(snow_class, cmap='Blues')
    # axs[1, 1].imshow(snow, cmap='Blues')
    # plt.show()

    return stats_df


def generate_report(df):
    manager = PdfManager()
    manager.with_element(Heading1(f"PDF Title"))
    manager.with_element(Paragraph(f"PDF description"))

    manager.with_element(Table(df))

    manager.create_pdf(result_file=f"file.pdf")

    return manager.get_bytes()


if __name__ == '__main__':
    test_dem = np.load('/home/stw/dem.obj.npy')
    test_snow = np.load('/home/stw/snow.obj.npy')
    # df = compute_snow_stats(test_dem, test_snow)
    # df.to_csv('test_stats.csv')
    df = pd.read_csv('test_stats.csv')
    pdf_raw = generate_report(df)

    print(pdf_raw)