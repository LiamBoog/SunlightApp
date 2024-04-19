import colour
import numpy as np


def custom_sd_to_srgb(t: float) -> str:
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

