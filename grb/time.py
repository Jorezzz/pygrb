import requests
from bs4 import BeautifulSoup
from astropy.time import Time
from functools import lru_cache

@lru_cache(maxsize = 100)
def parse_datetime_from_response_text(text, time_tag):
    '''
    Parse datetime from response text from heasarc
    Args:
        text: response text
        time_tag: time tag in response text, 'ijd' = 'time_out_ii', 'utc' = 'time_out_i'
    Returns:
        str: datetime in requested format
    '''
    ob = BeautifulSoup(text,'lxml')
    category = ob.find_all("td", {"id" : time_tag})
    return ' '.join(category[0].string.split())

def get_utc_from_ijd(ijd_time: float, loading_method = 'local') -> str:
    '''
    Converts UTC to Integral Julian Date
    Args:
        ijd_time (float): Integral Julian Date in float
        loading_method (str, optional): how to process transformation, 'local' - using astropy, 'web' - using heasarc. Defaults to 'local'
    '''
    if loading_method == 'local':
        return Time(51544 + ijd_time, format='mjd', scale = 'tt').utc.to_value('iso', subfmt='date_hms')
    elif loading_method == 'web':
        url = f'https://heasarc.gsfc.nasa.gov/cgi-bin/Tools/xTime/xTime.pl?time_in_i=&time_in_c=&time_in_d=&time_in_j=&time_in_m=&time_in_sf=&time_in_wf=&time_in_ii={ijd_time}&time_in_sl=&time_in_sni=&time_in_snu=&time_in_s=&time_in_h=&time_in_sz=&time_in_ss=&time_in_sn=&timesys_in=u&timesys_out=u&apply_clock_offset=yes'
        response = requests.get(url)
        return parse_datetime_from_response_text(response.text, "time_out_i")
    else:
        raise NotImplementedError(f'{loading_method=} is not implemented')

def get_ijd_from_utc(utc_time: str, loading_method = 'local') -> float:
    '''
    Converts Integral Julian Date to UTC
    Args:
        utc_time (str): datetime to convert in ISO format
        loading_method (str, optional): how to process transformation, 'local' - using astropy, 'web' - using heasarc. Defaults to 'local'
    '''
    if loading_method == 'local':
        time = utc_time[:10]+'T'+utc_time[11:]
        return Time(time, format='isot', scale='utc').tt.mjd - 51544
    elif loading_method == 'web':
        utc_time = utc_time[:10]+'+'+utc_time[11:13]+'%3A'+utc_time[14:16]+'%3A'+utc_time[17:19]
        url = f'https://heasarc.gsfc.nasa.gov/cgi-bin/Tools/xTime/xTime.pl?time_in_i={utc_time}&time_in_c=&time_in_d=&time_in_j=&time_in_m=&time_in_sf=&time_in_wf=&time_in_ii=&time_in_sl=&time_in_sni=&time_in_snu=&time_in_s=&time_in_h=&time_in_sz=&time_in_ss=&time_in_sn=&timesys_in=u&timesys_out=u&apply_clock_offset=yes'
        response = requests.get(url)
        return float(parse_datetime_from_response_text(response.text, "time_out_ii"))
    else:
        raise NotImplementedError(f'{loading_method=} is not implemented')

def get_utc_from_Fermi_seconds(fermi_seconds):
    url = f'https://heasarc.gsfc.nasa.gov/cgi-bin/Tools/xTime/xTime.pl?time_in_i=&time_in_c=&time_in_d=&time_in_j=&time_in_m=&time_in_sf={fermi_seconds}&time_in_wf=&time_in_ii=&time_in_sl=&time_in_sni=&time_in_snu=&time_in_s=&time_in_h=&time_in_sz=&time_in_ss=&time_in_sn=&timesys_in=u&timesys_out=u&apply_clock_offset=yes'
    response = requests.get(url)
    return parse_datetime_from_response_text(response.text, "time_out_i")

def get_ijd_from_Fermi_seconds(fermi_seconds) -> float:
    url = f'https://heasarc.gsfc.nasa.gov/cgi-bin/Tools/xTime/xTime.pl?time_in_i=&time_in_c=&time_in_d=&time_in_j=&time_in_m=&time_in_sf={fermi_seconds}&time_in_wf=&time_in_ii=&time_in_sl=&time_in_sni=&time_in_snu=&time_in_s=&time_in_h=&time_in_sz=&time_in_ss=&time_in_sn=&timesys_in=u&timesys_out=u&apply_clock_offset=yes'
    response = requests.get(url)
    return float(parse_datetime_from_response_text(response.text, "time_out_ii"))