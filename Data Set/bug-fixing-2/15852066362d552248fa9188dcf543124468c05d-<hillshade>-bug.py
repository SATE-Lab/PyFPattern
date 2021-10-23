

def hillshade(self, elevation, vert_exag=1, dx=1, dy=1, fraction=1.0):
    '\n        Calculates the illumination intensity for a surface using the defined\n        azimuth and elevation for the light source.\n\n        This computes the normal vectors for the surface, and then passes them\n        on to `shade_normals`\n\n        Parameters\n        ----------\n        elevation : array-like\n            A 2d array (or equivalent) of the height values used to generate an\n            illumination map\n        vert_exag : number, optional\n            The amount to exaggerate the elevation values by when calculating\n            illumination. This can be used either to correct for differences in\n            units between the x-y coordinate system and the elevation\n            coordinate system (e.g. decimal degrees vs. meters) or to\n            exaggerate or de-emphasize topographic effects.\n        dx : number, optional\n            The x-spacing (columns) of the input *elevation* grid.\n        dy : number, optional\n            The y-spacing (rows) of the input *elevation* grid.\n        fraction : number, optional\n            Increases or decreases the contrast of the hillshade.  Values\n            greater than one will cause intermediate values to move closer to\n            full illumination or shadow (and clipping any values that move\n            beyond 0 or 1). Note that this is not visually or mathematically\n            the same as vertical exaggeration.\n        Returns\n        -------\n        intensity : ndarray\n            A 2d array of illumination values between 0-1, where 0 is\n            completely in shadow and 1 is completely illuminated.\n        '
    dy = (- dy)
    (e_dy, e_dx) = np.gradient((vert_exag * elevation), dy, dx)
    normal = np.empty((elevation.shape + (3,))).view(type(elevation))
    normal[(..., 0)] = (- e_dx)
    normal[(..., 1)] = (- e_dy)
    normal[(..., 2)] = 1
    normal /= _vector_magnitude(normal)
    return self.shade_normals(normal, fraction)
