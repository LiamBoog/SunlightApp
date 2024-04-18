import colour
import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import h, c, k


# spectral_distribution = colour.sd_blackbody(4000) * 1e9
# with colour.domain_range_scale("1"):
#     xyz = colour.sd_to_XYZ(spectral_distribution)
#     xyz /= np.sum(xyz)
#     xy = colour.XYZ_to_xy(xyz)
#     xy = colour.CCT_to_xy(1000)
#     xyz = colour.xy_to_XYZ(xy)
#     rgb = colour.XYZ_to_sRGB(xyz)
#     print(rgb)
#     # colour.plotting.plot_single_colour_swatch(rgb)
# xy = colour.CCT_to_xy(1500)
# xyz = colour.xy_to_XYZ(xy)
# rgb = colour.XYZ_to_sRGB(xyz)
# colour.plotting.plot_single_colour_swatch(rgb)
# colour.plotting.plot_sds_in_chromaticity_diagram_CIE1931(colour.sd_blackbody(1000))
# print(xyz, rgb)


def xyz_from_xy(x, y):
    """Return the vector (x, y, 1-x-y)."""
    return np.array((x, y, 1 - x - y))


class ColourSystem:
    """A class representing a colour system.

    A colour system defined by the CIE x, y and z=1-x-y coordinates of
    its three primary illuminants and its "white point".

    TODO: Implement gamma correction

    """

    # The CIE colour matching function for 380 - 780 nm in 5 nm intervals
    cmf = np.loadtxt('cie-cmf.txt', usecols=(1, 2, 3))

    def __init__(self, red, green, blue, white):
        """Initialise the ColourSystem object.

        Pass vectors (ie NumPy arrays of shape (3,)) for each of the
        red, green, blue  chromaticities and the white illuminant
        defining the colour system.

        """

        # Chromaticities
        self.red, self.green, self.blue = red, green, blue
        self.white = white
        # The chromaticity matrix (rgb -> xyz) and its inverse
        self.M = np.vstack((self.red, self.green, self.blue)).T
        self.MI = np.linalg.inv(self.M)
        # White scaling array
        self.wscale = self.MI.dot(self.white)
        # xyz -> rgb transformation matrix
        self.T = self.MI / self.wscale[:, np.newaxis]

    def xyz_to_rgb(self, xyz):
        """Transform from xyz to rgb representation of colour.

        The output rgb components are normalized on their maximum
        value. If xyz is out the rgb gamut, it is desaturated until it
        comes into gamut.

        By default, fractional rgb components are returned; if
        out_fmt='html', the HTML hex string '#rrggbb' is returned.

        """

        rgb = self.T.dot(xyz)
        if np.any(rgb < 0):
            # We're not in the RGB gamut: approximate by desaturating
            w = - np.min(rgb)
            rgb += w
        if not np.all(rgb == 0):
            # Normalize the rgb vector
            rgb /= np.max(rgb)

        print(rgb)
        return self.rgb_to_hex(rgb)

    def rgb_to_hex(self, rgb):
        """Convert from fractional rgb values to HTML-style hex string."""

        hex_rgb = (255 * rgb).astype(int)
        return '#{:02x}{:02x}{:02x}'.format(*hex_rgb)

    def spec_to_xyz(self, spec):
        """Convert a spectrum to an xyz point.

        The spectrum must be on the same grid of points as the colour-matching
        function, self.cmf: 380-780 nm in 5 nm steps.

        """

        XYZ = np.sum(spec[:, np.newaxis] * self.cmf, axis=0)
        den = np.sum(XYZ)
        if den == 0.:
            return XYZ
        return XYZ / den

    def spectral_radiance_to_rgb(self, spec):
        """Convert a spectrum to an rgb value."""

        xyz = self.spec_to_xyz(spec)
        return self.xyz_to_rgb(xyz)


def planck(lam, T):
    """ Returns the spectral radiance of a black body at temperature T.

    Returns the spectral radiance, B(lam, T), in W.sr-1.m-2 of a black body
    at temperature T (in K) at a wavelength lam (in nm), using Planck's law.

    """

    lam_m = lam / 1.e9
    fac = h * c / lam_m / k / T
    B = 2 * h * c ** 2 / lam_m ** 5 / (np.exp(fac) - 1)
    return B


def custom_sd_to_srgb(t: float) -> str:
    blackbody_spectrum = colour.sd_blackbody(t, colour.SpectralShape(380, 780, 5)) * 1e9
    xyz = colour.sd_to_XYZ(
        colour.SpectralDistribution(blackbody_spectrum),
        cmfs=colour.MSDS_CMFS["CIE 2015 10 Degree Standard Observer"],
        illuminant=colour.SDS_ILLUMINANTS["D65"])
    xyz /= np.sum(xyz)
    srgb = colour.XYZ_to_sRGB(xyz)
    # srgb -= min if (min := np.min(srgb)) < 0 else 0
    srgb /= np.max(srgb)
    srgb = np.clip(srgb, 0, 1)
    srgb_hex = colour.notation.RGB_to_HEX(srgb)
    print(xyz, srgb, srgb_hex)
    return srgb_hex, tuple(srgb)


def stolen_sd_to_rgb(t: float) -> str:
    blackbody_spectrum = colour.sd_blackbody(t, colour.SpectralShape(380, 780, 5)) * 1e9
    srgb = colour_system.spectral_radiance_to_rgb(blackbody_spectrum.values)
    xyz = colour_system.spec_to_xyz(blackbody_spectrum.values)
    print(xyz, srgb)
    return srgb


def plot_gradients(a_colours: list[tuple[float, float, float]], b_colours: list[tuple[float, float, float]]) -> None:
    figure, (ax1, ax2) = matplotlib.pyplot.subplots(2, 1, sharex=True)
    for i in range(min(len(a_colours), len(b_colours))):
        ax1.bar(i, 1, color=a_colours[i], edgecolor="none")
        ax2.bar(i, 1, color=b_colours[i], edgecolor="none")
    plt.tight_layout()
    plt.show()


T = 1500
blackbody_spectrum = colour.sd_blackbody(T, colour.SpectralShape(380, 780, 5)) * 1e9

colour_system = ColourSystem(
    red=xyz_from_xy(0.67, 0.33),
    green=xyz_from_xy(0.21, 0.71),
    blue=xyz_from_xy(0.15, 0.06),
    white=xyz_from_xy(0.3127, 0.3290))

temp_range = range(100, 10000, 250)
plot_gradients(
    [custom_sd_to_srgb(T)[1] for T in temp_range],
    [tuple(int(stolen_sd_to_rgb(T).lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)) for T in temp_range])
