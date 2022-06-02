from tkinter.messagebox import NO
import cdsapi
from pathlib import Path
import pandas as pd
import rioxarray
import xarray as xr


class ERA5_Manager(object):
    def __init__(self, folder=None, result_dir='result'):
        '''

        Parameters:
        -----------
        folder : str or pathlib.Path object
            folder to save data
        result : str
            result folder. Could be an absolute path or just a name
        '''
        self.client = cdsapi.Client()
        if folder is None:
            self.folder = Path.cwd()
        else:
            self.folder = Path(folder)

        if Path(result_dir).is_absolute():
            self.result_dir = Path(result_dir)
        else:
            self.result_dir = self.folder / result_dir

    def generate_datetime(self, start=None, end=None, periods=None,
                          freq=None, time=None):
        '''return year, month, day, time in the format of CDS API. the 
        date (year, month, day) for CDS API is generated by using 
        pd.period_range method. Of the four parameters: start, end, 
        periods, and freq, exactly three must be specified to generate 
        date


        Parameters
        ----------
        start : str or period-like
            Left bound for generating periods.
        end : str or period-like
            Right bound for generating periods.
        periods : int, default None
            Number of periods to generate.
        freq : str or DateOffset, optional
            Frequency alias. By default the freq is taken from `start` or `end`
            if those are Period objects. Otherwise, the default is ``"D"`` for
            daily frequency.
        time : a list of str, optional
            time to download for product. Default None, which means all hourly 
            time data will be used. The format of time should be '%H:%M'
        '''
        date = pd.period_range(start, end, periods, freq)
        if time is None:
            time = ['00:00', '01:00', '02:00', '03:00',
                    '04:00', '05:00', '06:00', '07:00',
                    '08:00', '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00', '15:00',
                    '16:00', '17:00', '18:00', '19:00',
                    '20:00', '21:00', '22:00', '23:00']
        year = sorted(set(date.strftime("%Y")))
        month = sorted(set(date.strftime("%m")))
        day = sorted(set(date.strftime("%d")))
        return year, month, day, time

    def get_date_range(self, start, end):
        date_range = {'beg': pd.to_datetime(start),
                      'end': pd.to_datetime(end)}
        return date_range

    def get_area_from_DEM(self, dem_file, buffer=0.25):
        da = rioxarray.open_rasterio(dem_file)
        area = [
            float(da.y.max()) + buffer,  # north
            float(da.x.min()) - buffer,  # west
            float(da.y.min()) - buffer,  # south
            float(da.x.max()) + buffer   # east
        ]
        da.close()
        return area

    def all_pressure_levels(self):
        '''return all pressure levels available'''
        pressure_levels = [
            '1', '2', '3',
            '5', '7', '10',
            '20', '30', '50',
            '70', '100', '125',
            '150', '175', '200',
            '225', '250', '300',
            '350', '400', '450',
            '500', '550', '600',
            '650', '700', '750',
            '775', '800', '825',
            '850', '875', '900',
            '925', '950', '975',
            '1000'
        ]
        return pressure_levels

    def get_pressure_levels(self, min, max):
        '''return all pressure levels than in the interval [min, max]

        Parameters:
        -----------
        min/max : int
            min/max pressure levels
        '''
        all_pressure_levels = self.all_pressure_levels()
        pressure_levels = [
            i for i in all_pressure_levels
            if min <= int(i) <= max
        ]
        return pressure_levels

    def _split_requests(self, year, month, day, time, num_item):
        '''split requests into multipart to make it's number meet the 
        CDS api requirements (<120000)
        '''
        num_y = len(year)
        num_m = len(month)
        num_d = len(day)
        num_t = len(time)

        num_one_month = num_item * num_t * num_d
        # all year small than 12000
        if num_one_month * num_m * num_y < 120000:
            return [(year, month, day)]
        # one year small than 12000
        elif num_one_month * num_m < 120000:
            return [([y], month, day) for y in year]
        # one month (max items for 2 variables in one month is 55056 < 120000)
        else:
            ymd_list = []
            for y in year:
                dr = pd.date_range(f'{y}-01-01', f'{y}-12-31', freq='1D')
                df_dr = pd.Series(dr, index=dr)
                for m in month:
                    dr_m = df_dr[f'{y}-{m}'].index
                    day_new = sorted(
                        set(dr_m.strftime('%d')).intersection(set(day))
                    )
                    ymd_list.append(([y], [m], day_new))
            return ymd_list

    def _retrieve_multiple_date(self, name, year, month, day, time, num_item, request_info):
        ymd_list = self._split_requests(
            year, month, day, time, num_item)

        for year, month, day in ymd_list:
            request_info.update({
                'year': year,
                'month': month,
                'day': day,
            })
            file_name = f'{name}_{year[0]}{month[0]}{day[0]}-{year[-1]}{month[-1]}{day[-1]}.nc'
            target = self.folder / file_name
            if target.is_file():
                print(f'File {target} has been downloaded, Skipping...')
                continue
            else:
                self.client.retrieve(name, request_info, target)

    def _retrieve_single_date(self, name, request_info, file_name):
        target = self.folder / file_name
        if target.is_file():
            print(f'File {target} has been downloaded, Skipping...')
        else:
            self.client.retrieve(name, request_info, target)

    def retrieve_pressure_levels(self, pressure_level, year, month, day, time, area):
        name = 'reanalysis-era5-pressure-levels'

        num_item = len(pressure_level) * 2

        request_info = {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': ['geopotential', 'temperature'],
            'pressure_level': pressure_level,
            'time': time,
            'area': area,
        }
        self._retrieve_multiple_date(
            name, year, month, day, time, num_item, request_info)

    def retrieve_single_levels(self, year, month, day, time, area):
        name = 'reanalysis-era5-single-levels'

        # geopotential data
        request_info = {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': 'geopotential',
            'year': ['1979'],
            'month': ['01'],
            'day': ['01'],
            'time': ['12:00'],
            'area': area,
        }
        self.geop = self.folder / 'surface_geopotential.nc'
        self._retrieve_single_date(name, request_info, self.geop)

        # 2m_temperature
        num_item = 1
        ymd_list = self._split_requests(year, month,
                                        day, time, num_item)
        for year, month, day in ymd_list:
            request_info = {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': '2m_temperature',
                'time': time,
                'area': area,
            }
        self._retrieve_multiple_date(
            name, year, month, day, time, num_item, request_info)

    def _format_dataset(self, ds):
        '''format dataset to make file could be read by redcapp.
        '''
        name_map = {'latitude': 'lat',
                    'longitude': 'lon',
                    't': 'Temperature',
                    'z': 'Geopotential',
                    't2m': '2 metre temperature'}
        rename_map = {}
        for k, v in name_map.items():
            if k in ds:
                rename_map.update({k: v})
        ds = ds.rename(rename_map)

        if 'lat' in ds:
            if ds['lat'][0] > ds['lat'][-1]:
                ds = ds.sortby('lat', ascending=True)
        return ds

    def format_nc(self, file_in, file_out=None):
        '''format nc file to make file could be read by redcapp.

        Parameters:
        -----------
        file_in: str or pathlib.Path object
            The path to the nc file that needs to be formatted.
        file_out: str or pathlib.Path object
            The path to the nc file that has been formatted.
            if file_out is None, will save is to result folder
            with the same name with file_in

        Returns:
        --------
        path of output file  
        '''
        ds = xr.open_dataset(file_in)
        ds = self._format_dataset(ds)

        if file_out is None:
            file_out = self.result_dir / Path(file_in).name
        encode = {}
        if 'time' in ds:
            encode = {'time':
                      {'units': 'seconds since 1970-1-1',
                       'calendar': 'standard'}
                      }
        make_sure_folder(file_out.parent)
        make_sure_file(file_out)

        ds.to_netcdf(file_out, encoding=encode)
        ds.close()
        return file_out

    def merge_nc(self, name, merged_file=None, day_mean=True, format=True):
        '''merge multiple nc files into one file

        Parameters:
        -----------
        name: str, one of ['pl', 'sl']
            which type of data to merge. 'pl' and 'sl' is short for 'reanalysis-era5-pressure-levels' and
            'reanalysis-era5-single-levels' product respectively.
        merged_file: str or pathlib.Path object
            the path to save merged file. could be absolute path
            or just a name of file
        day_mean: bool
            where to get daily mean value after combine all data
        format: bool
            Whether to format nc file to make file could be read by redcapp. 

        Returns:
        --------
        path of output file        
        '''
        names_mapper = {
            'pl': 'reanalysis-era5-pressure-levels',
            'sl': 'reanalysis-era5-single-levels'
        }
        pattern = f'{names_mapper[name]}*.nc'
        files = list(self.folder.glob(pattern))
        mfds = xr.open_mfdataset(files)

        if day_mean:
            mfds = (mfds.groupby('time.date').mean()
                    .rename({'date': 'time'}))
            mfds['time'] = pd.to_datetime(mfds['time'])

        encode = {}
        if format:
            mfds = self._format_dataset(mfds)
            if 'time' in mfds:
                encode = {'time':
                          {'units': 'seconds since 1970-1-1',
                           'calendar': 'standard'}
                          }

        if merged_file is None:
            dt_start = files[0].stem.split('_')[-1][:8]
            dt_end = files[-1].stem.split('_')[-1][9:]
            d_txt = 'daily' if day_mean else ''
            merged_file = f'result/{names_mapper[name]}_{dt_start}-{dt_end}_{d_txt}.nc'
        if not Path(merged_file).is_absolute():
            merged_file = self.folder / merged_file

        make_sure_folder(merged_file.parent)
        make_sure_file(merged_file)

        mfds.to_netcdf(merged_file, encoding=encode)
        mfds.close()
        print(f'Merged files to file: {merged_file}')

        return merged_file

    def get_pl(self, name=None):
        if name is None:
            path = list(self.result_dir.glob(
                'reanalysis-era5-pressure-levels*.nc'))[0]
        else:
            path = self.result_dir / name

        return path

    def get_sa(self, name=None):
        if name is None:
            path = list(self.result_dir.glob(
                'reanalysis-era5-single-levels*.nc'))[0]
        else:
            path = self.result_dir / name

        return path

    def get_geop(self, name=None):
        if name is None:
            path = self.result_dir / 'surface_geopotential.nc'
        else:
            path = self.result_dir / name

        return path


def make_sure_folder(folder):
    if not folder.is_dir():
        folder.mkdir(parents=True)


def make_sure_file(file):
    if file.is_file():
        file.unlink()


def install_CDS_API_key(url, key):
    '''install the CDS API key  in the file $HOME/.cdsapirc'''
    txt = f'url: {url}\nkey: {key}'
    file = Path('~/.cdsapirc').expanduser()
    with open(file, 'w') as f:
        f.write(txt)
    print(f'The file "{file}" has been written as follows api key:')
    with open(file) as f:
        print(f'"{f.read()}"')