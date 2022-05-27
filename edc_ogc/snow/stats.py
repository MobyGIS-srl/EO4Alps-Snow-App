
import numpy as np
import matplotlib.pyplot as plt
import snow.dem_utils as du
from moby_report.manager import PdfManager
from moby_report.element import *

def reclass_aspect(x, n_class=4):
    dg = 360 // n_class
    return ((x + dg/2) // dg) - (x // (360 -dg/2)) * n_class


def compute_snow_stats(dem, snow, dz=500, flat=3):

    slope, aspect = du.horneslope(dem, 250)
    elev_class = dem // dz
    slope_class = np.where(slope > flat, 1, 0)
    aspect_class = reclass_aspect(aspect, 4)
    aspect_class = slope_class * (aspect_class + 1)

    # TODO: decomment aspect class
    snow_class = elev_class  # + (aspect_class * 100)

    import xarray as xr
    from xrspatial import aspect, slope, zonal_stats, zonal_crosstab

    # da_dem = xr.DataArray(dem, dims=['y', 'x'], name='raster')
    # aspect_agg = aspect(da_dem)
    # aspect_class = reclass_aspect(aspect_agg, 4)
    # slope_agg = slope(da_dem)

    zones = xr.DataArray(snow_class, dims=['y', 'x'], name='Z')
    values = xr.DataArray(snow, dims=['y', 'x'], name='SWE')

    # Calculate Stats with dask backed xarray DataArrays
    stats_df = zonal_stats(zones=zones, values=values, stats_funcs=['mean', 'sum', 'count'])
    print(stats_df)

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