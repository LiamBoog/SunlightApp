import colour
import numpy as np
from numpy.typing import NDArray
from scipy.constants import h, c, k


SOLAR_BLACKBODY_TEMPERATURE = 5800


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


def get_blackbody(wavelength: NDArray[int]) -> colour.SpectralDistribution:
    wavelength_meters = wavelength * 1e-9
    exponent = h * c / (k * wavelength_meters * SOLAR_BLACKBODY_TEMPERATURE)
    denominator = wavelength_meters ** 5 * (np.exp(exponent) - 1)
    spectral_radiance = (2 * h * c * c) / denominator
    scattering_coefficient = get_total_scattering_coefficient(0, wavelength_meters)
    spectral_radiance = scattering_coefficient * spectral_radiance
    return colour.SpectralDistribution(spectral_radiance, wavelength)


def get_air_mass(zenith_angle: float) -> float:
    r = 6371 / 9
    a = 2 * r + 1
    cosine = np.cos(np.radians(zenith_angle))
    square_root = np.sqrt((r * cosine) ** 2 + a)
    denominator = square_root + r * cosine
    return a / denominator


def get_total_scattering_coefficient(zenith_angle: float, wavelength: NDArray[float]) -> float:
    scattering_coefficient = 1e-26
    x = -(get_air_mass(zenith_angle) * scattering_coefficient / wavelength ** 4)
    co = np.exp(x)
    return co


def spectral_radiance_to_srgb() -> str:
    blackbody_spectrum = get_blackbody(np.array([i for i in range(380, 781, 5)]))
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


print(spectral_radiance_to_srgb())
