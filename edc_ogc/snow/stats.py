
import numpy as np
import matplotlib.pyplot as plt
import edc_ogc.snow.dem_utils as du
from moby_report.manager import PdfManager
import moby_report.element as el
import xarray as xr
import xrspatial as xrs
from rasterio.plot import show
import io


def reclass_aspect(x, n_class=4):
    dg = 360 // n_class
    return ((x + dg/2) // dg) - (x // (360 - dg/2)) * n_class


def format_altitude_range(z, dz):
    return f"{z:.0f} - {z + dz:.0f}"


def format_aspect(a):
    asp_zones = {0: 'Flat areas', 1: 'North slopes', 2: 'East slopes', 3: 'South slopes', 4: "West slopes"}
    return asp_zones[a // 100]


def format_df(df, dz):
    df = df.rename(columns={0: 'Flat areas', 1: 'North slopes', 2: 'East slopes', 3: 'South slopes', 4: "West slopes"})
    df.columns.name = None
    df.index = df.index.map(lambda z: f"{z:.0f}-{z + dz:.0f}")
    return df


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
    stats_df = xrs.zonal_stats(zones=zones, values=values, stats_funcs=['mean', 'sum', 'count'])
    stats_df['altitude'] = stats_df['zone'] % 100 * dz
    stats_df['aspect'] = stats_df['zone'] // 100
    stats_df = stats_df.set_index(['aspect', 'altitude'])

    df_mean = format_df(stats_df['mean'].unstack('aspect'), dz)
    df_count = format_df(stats_df['count'].unstack('aspect'), dz)

    return df_mean, df_count


def generate_report(var, date, img, df_mean, df_vol, tot_vol):
    manager = PdfManager()

    # Header
    manager.with_header(header_images=[
        el.ImageUrl("https://snow-app-gte2s.1faa6041-02f5-4205-ae26-48fc3bc3b966.hub.eox.at/static/esalogo_white.svg"),
        el.ImageUrl("https://snow-app-gte2s.1faa6041-02f5-4205-ae26-48fc3bc3b966.hub.eox.at/static/mobygis_white.svg"),
        el.ImageUrl("https://snow-app-gte2s.1faa6041-02f5-4205-ae26-48fc3bc3b966.hub.eox.at/static/SinergiseLogo_white.svg"),
        el.ImageUrl("https://snow-app-gte2s.1faa6041-02f5-4205-ae26-48fc3bc3b966.hub.eox.at/static/eurac-logo_white.svg"),
    ])

    manager.with_element(el.Heading1(f"EO4ALps - Snow Report"))

    date_box = el.Box([el.Paragraph(date)],
        title="Date",
        with_padding=True
    )
    manager.with_element(date_box)

    map_box = el.Box([el.ImageBytes(img)],
        title=f"{var} Map",
        with_padding=True
    )
    manager.with_element(map_box)

    manager.with_element(el.PageInterruption())

    unit = '[mm]' if var == 'SWE' else '[cm]'
    manager.with_element(el.Heading2(f"Mean {var} {unit}"))
    manager.with_element(el.Table(df_mean))
    if var == 'SWE':
        manager.with_element(el.Heading2(f"{var} volume [Mmc]"))
        manager.with_element(el.Table(df_vol))
        manager.with_element(el.Paragraph(f"The total amount of SWE in selected area is: {tot_vol/1000000:.0f} Mmc."))
    # manager.create_pdf(result_file=f"file.pdf")

    manager.with_footer("ESA Contract No. 4000133468/20/I-BG - EO4ALPS REGIONAL INITIATIVE - EXPRO+")

    # "Waterjade by MobyGIS Srl - Viale Dante 300, I - 38057 Pergine Valsugana (TN)<br>" +
    # "Tel. +39 0461 425806 | email: info@waterjade.com<br>" +

    return manager.get_bytes()


def compose_map(dem: np.array, snow: np.array, dtr, str) -> bytes:
    da_z = xr.DataArray(dem, dims=['y', 'x'], name='Z')
    da_hillshade = xrs.hillshade(da_z)

    # write rendered plot to memory
    buf = io.BytesIO()
    # plt.imshow(da_hillshade, cmap='gray');
    # plt.imshow(test_dem, cmap='terrain', alpha=0.1)
    # plt.imshow(snow, cmap='Blues', alpha=0.6)
    # plt.contourf(snow, cmap='Blues', alpha=0.5)
    fig, ax = plt.subplots()
    show(da_hillshade.values, ax=ax, cmap='gray', transform=dtr)
    show(snow, ax=ax, cmap='viridis', alpha=0.3, transform=str)
    # plt.contourf(snow, cmap='Blues', alpha=0.5)
    plt.savefig(buf, dpi=200.0)
    return buf.getvalue()


if __name__ == '__main__':
    import edc_ogc.snow.stats as sst

    test_dem = np.load('/home/ste/dem.obj.npy')
    test_snow = np.load('/home/ste/snow.obj.npy')

    img = compose_map(test_dem, test_snow)

    df = sst.compute_snow_stats(test_dem, test_snow)
    pdf_raw = generate_report(df)

    # print(pdf_raw)
    # from matplotlib.colors import ListedColormap, LinearSegmentedColormap
    # cmap = ListedColormap(["darkorange", "gold", "lawngreen", "lightseagreen"])
    # plt.imshow(da_hillshade, cmap='gray'); plt.imshow(test_dem, cmap=cmap, alpha=0.1)

