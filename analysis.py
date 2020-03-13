import sys
import random

from matplotlib import pyplot as plt
from matplotlib import ticker
import numpy as np
import nrrd

from colorpy import blackbody
from colorpy import colormodels


logging = False
if logging:
    old_stdout = sys.stdout
    log_file = open('log.txt', "w")
    sys.stdout = log_file

plt.style.use('dark_background')

L0 = 3.828e26
f0 = 37 * L0 / (4 * np.pi * (25 * 9460730777119564)**2)


def f(m):
    """Return the flux given a magnitude"""
    return f0 * 10**(-0.4 * m)


def m(f):
    """Return the magnitude given a flux"""
    return -2.5 * np.log10(f / f0)


# Reading an nrrd file from ds9
im = nrrd.read('ds9.nrrd')
im = im[0].T

# flipping, trimming of some useless pixels
im = im[:, 13:]
im = im[13:, :]

shape = im.shape
print(f"Image dimensions: {im.shape}.")
print(f"fov: {0.559 * np.array(shape)} as")

fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
fig2, ax5 = plt.subplots()

# Showing our image
ax1.imshow(im, cmap='bone')

# Showing a cropped image
img_cropped = np.empty(shape)
img_cropped[1800:3300, 1800:3087] = im[1800:3300, 1800:3087]
ax2.imshow(img_cropped, cmap='bone')
ax2.set_ylim((3300, 1800))
ax2.set_xlim((1800, 3087))

# Calibration measurements (some done with ds9) star: GSC 04383-00613
__pixel_delta_cal = 1.21767568e+12  # from ds9
__cal_star_m = 13.810  # from Aladin lite, visual magnitude of GSC 04383-00613
__cal_star_f = f(__cal_star_m)
# With the fluxpixel_ratio, we can convert pixel values to flux values.
fluxpixel_ratio = __cal_star_f / __pixel_delta_cal


# Total flux of the galaxy, first some processing:
galaxy = im[1800:3300, 1800:3087]
min_pix_value = min(galaxy.flatten())
galaxy += min_pix_value  # No photons implies a pixel value of 0
galaxy[np.where(galaxy < 0)] = 0  # should not be neccesary
ax3.hist(galaxy.flatten(), bins=30)


# a quick way to get the total amt of pixels, (faster)
pixels_tot = np.mean(galaxy) * np.product(galaxy.shape)
print("Pixel sum:")
print(pixels_tot)

print("Flux:")
flux = fluxpixel_ratio * pixels_tot
print(f"{flux} W/m2")

print("magnitude:")
print(m(flux))  # Should be around 6-7

print("Total luminocity L_tot:")
d_m = 11.74e6 * 9460730777119564  # 11.8 mln ly from wikipedia
L_tot = 4 * np.pi * d_m**2 * flux
print(f"{L_tot} W")

print("Amount of Stars in M_81:")
N = L_tot / L0  # Assuming each star has a brightness of 1 L0
print(f"{N:e} stars")
N2 = 2.5e14

print('Diameter of M81:')
# astrometry.net gives us a ratio of .559 as / pixel
theta = 0.559 * (3300 - 1800)  # arcseconds
print(f"{theta} arcseconds")
d_pc = d_m * 3.24077929e-17  # from m to pc
diameter_m = d_pc * theta * 149597870700  # au to m
diameter_ly = diameter_m / 9460730777119564
print(f"{diameter_ly} ly")

# error prop on theta
dr = 50 * 149597870700 * d_pc / 2  # m
print(f"dr {dr / 9460730777119564}")


aspect_ratio = 10 / 3  # Aspect ratio milky way from wikipedia somewhere
r_m = diameter_m / 2
volume_m3 = np.pi * r_m**2 * diameter_m / aspect_ratio

volume_pc3 = volume_m3 * 3.24077929e-17**3

# error prop on V
dV = 9 / 5 * np.pi * r_m**2 * dr * 3.24077929e-17**3  # pc
print(f"Error on V: {dV/volume_pc3}")

print(f"Total volume of M81 (Aspect ratio {aspect_ratio} to 1)")
print(f"{volume_pc3:e} pc^3")
print(f"Average star density:")
rho = N / volume_pc3
print(f"{rho} stars / pc^3")

# Error prop on rho
drho = N / volume_pc3**2 * dV
print(f"drho: {drho}")

# What about specifically the center of M81?
# We found the total pixel value of 3.960068e+12, we convert this to a flux.
# We also need to consider the pixel delta.
center_tot_pixels_delta = 3.96e+12
print("Total pixel value center:")
print(center_tot_pixels_delta)

center_f = fluxpixel_ratio * center_tot_pixels_delta
print("Flux of the center of m81:")
print(center_f)

center_L = 4 * np.pi * d_m**2 * center_f
print("luminosity of the center of m81:")
print(center_L)

center_N = center_L / L0
print("Total stars in the center of m81:")
print(center_N)

# The diameter of the center is 38 pixels
center_theta = 38 * 0.559  # arcseconds, .559 from astrometry.net
center_diameter_m = center_theta * d_pc * 149597870700  # from au to m
center_diameter_pc = center_diameter_m * 3.24077929e-17
print("Center diameter:")
print(f"{center_diameter_pc} pc = {center_diameter_pc / 3.26} ly")

center_V = 4 / 3 * np.pi * (center_diameter_pc / 2)**2  # The center as a shere
center_rho = center_N / center_V
print("Star density inside the center of m81:")
print(f"{center_rho} stars / pc^3")


# Calculating the total flux if earth would be in m81:
max_visible_magnitude = 5
d_max_m = 10 ** (max_visible_magnitude / 5) * \
    np.sqrt(L0 / (4 * np.pi * f0)
            )  # Once again assuming every star has luminosity L0
d_max_pc = d_max_m * 3.24077929e-17
print("Max visible distance:")
print(f"{d_max_pc} pc")

# Volume of the domain:
V_tot = 4 / 3 * np.pi * (d_max_pc)**3  # pc^3
V_better = 2 / 3 * np.pi * d_max_pc**3 * (1 - np.cos(np.pi / 6))
print("Volume over which to simulate:")
print(f"{V_tot} pc^3")
# Total amount of stars to simulate:
n = V_tot * rho
print(f"Simulating {n} stars")

# error prop on n
dn = V_tot * drho
print(f"dn: {dn}")

f_m81 = 0
M_region = 0

# print(dir(colorpy))
random.seed('astronomy')
print("Distance (pc), flux (W/m2),   T (K),  M (M0).")
for i in range(int(n - dn)):
    r = random.uniform(3.08567758e16, d_max_pc *
                       3.08567758e16)
    L = random.triangular(0.7, 10, 1)
    f_ = L * L0 / (4 * np.pi * r**2)
    f_m81 += f_

    # Getting an idea of the solar mass/pc3 in near our simulated earth
    # We use the mass-luminosity relation from wikipedia
    mass = L**0.25
    M_region += mass
    # Given the randomly generated distance and luminosity, we want to calculate:
    # A) the colour of the star
    # B) the visual flux of the star (Each star has a radius )
    # We will then plot this in ax4 and ax5

    R = 1.5 * 696340000  # m
    sigma = 5.67e-8  # stefan-boltsmann constant
    T = (L * L0 / (4 * np.pi * R**2 * sigma))**(1 / 4)  # stefan-boltzmann law
    color = np.array(colormodels.irgb_from_xyz(
        blackbody.blackbody_color(T))) / 255

    x, y = (random.random(), random.random())
    ax4.scatter(x, y, s=f_ * 7e7, c=[color])
    ax5.scatter(x, y, s=f_ * 7e7, c=[color])
    dis = f"{(r / 3.08567758e16):.3g}"
    print(f"{''.join([' ' for _ in range(13 - len(dis))])}{(r / 3.08567758e16):.3g},    {f_:.2e},    {T:.0f},    {mass:.2f}.")


print()
ax4.set_aspect('equal')
ax4.xaxis.set_major_locator(ticker.NullLocator())
ax4.xaxis.set_minor_locator(ticker.NullLocator())
ax4.yaxis.set_major_locator(ticker.NullLocator())
ax4.yaxis.set_minor_locator(ticker.NullLocator())

ax5.set_aspect('equal')
ax5.xaxis.set_major_locator(ticker.NullLocator())
ax5.xaxis.set_minor_locator(ticker.NullLocator())
ax5.yaxis.set_major_locator(ticker.NullLocator())
ax5.yaxis.set_minor_locator(ticker.NullLocator())
fig2.savefig(r'pictures/Simulated_sky.png')


print("Simulated m81-earth.")
print(f"Total magnitude: {m(f_m81)}")
print(f"Total mass/pc^3: {M_region / V_tot} M0/pc^3")


if logging:
    sys.stdout = old_stdout
    log_file.close()

plt.show()
# time.sleep(60)
# plt.close()
