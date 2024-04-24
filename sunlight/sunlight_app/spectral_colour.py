import colour
import ephem
import datetime
import geocoder
import python_weather
import numpy as np
from numpy.typing import NDArray
from scipy.constants import h, c, k


SOLAR_BLACKBODY_TEMPERATURE = 5777


def blackbody_temperature_to_srgb(t: float) -> str:
    blackbody_spectrum = colour.sd_blackbody(t, colour.SpectralShape(380, 780, 5))
    xyz = colour.sd_to_XYZ(
        colour.SpectralDistribution(blackbody_spectrum),
        cmfs=colour.MSDS_CMFS["CIE 2015 10 Degree Standard Observer"],
        illuminant=colour.SDS_ILLUMINANTS["D65"])
    xyz /= np.sum(xyz)
    srgb = colour.XYZ_to_sRGB(xyz)
    srgb /= np.max(srgb)
    srgb = np.clip(srgb, 0, 1)
    srgb_hex = colour.notation.RGB_to_HEX(srgb)
    return str(srgb_hex)


def solar_spectral_radiance(wavelength: NDArray[int], zenith_angle: float) -> colour.SpectralDistribution:
    wavelength_meters = wavelength * 1e-9
    exponent = h * c / (k * wavelength_meters * SOLAR_BLACKBODY_TEMPERATURE)
    denominator = wavelength_meters ** 5 * (np.exp(exponent) - 1)
    spectral_radiance = (2 * h * c * c) / denominator
    scattering_coefficient = get_total_scattering_coefficient(zenith_angle, wavelength_meters)
    spectral_radiance = scattering_coefficient * spectral_radiance
    return colour.SpectralDistribution(spectral_radiance, wavelength)


def air_mass_coefficient(zenith_angle: float) -> float:
    r = 6371 / 9
    a = 2 * r + 1
    cosine = np.cos(np.radians(zenith_angle))
    square_root = np.sqrt((r * cosine) ** 2 + a)
    denominator = square_root + r * cosine
    return a / denominator


def get_total_scattering_coefficient(zenith_angle: float, wavelength: NDArray[float]) -> float:
    scattering_coefficient = 1e-26
    x = -(air_mass_coefficient(zenith_angle) * scattering_coefficient / wavelength ** 4)
    co = np.exp(x)
    return co


def solar_zenith_to_srgb(zenith_angle: float) -> str:
    blackbody_spectrum = solar_spectral_radiance(np.array([i for i in range(380, 781, 5)]), zenith_angle)
    xyz = colour.sd_to_XYZ(
        colour.SpectralDistribution(blackbody_spectrum),
        cmfs=colour.MSDS_CMFS["CIE 2015 10 Degree Standard Observer"],
        illuminant=colour.SDS_ILLUMINANTS["D65"])
    xyz /= np.sum(xyz)
    srgb = colour.XYZ_to_sRGB(xyz)
    srgb /= np.max(srgb)
    srgb = np.clip(srgb, 0, 1)
    srgb_hex = colour.notation.RGB_to_HEX(srgb)
    return str(srgb_hex)


def solar_zenith_angle() -> float:
    sun: ephem.Body = ephem.Sun()
    latitude, longitude = geocoder.ip("me").latlng
    observer = ephem.Observer()
    observer.lat = latitude
    observer.lon = longitude
    observer.date = ephem.Date(datetime.datetime.now(datetime.UTC))
    observer.temperature = 15
    sun.compute(observer)
    return 90 + np.degrees(sun.alt)


print((zenith := solar_zenith_angle()))
print(solar_zenith_to_srgb(zenith))
