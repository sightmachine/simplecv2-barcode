from math import sqrt

import numpy as np
from copy import copy
import scipy.spatial.distance as spsd

from simplecv.features.features import Feature


class Barcode(Feature):
    """
    **SUMMARY**

    The Barcode Feature wrappers the object returned by find_barcode(), a zbar
    symbol

    * The x,y coordinate is the center of the code.
    * points represents the four boundary points of the feature.  Note: for QR
     codes, these points are the reference rectangls, and are quadrangular,
     rather than rectangular with other datamatrix types.
    * data is the parsed data of the code.

    **SEE ALSO**

    :py:meth:`ImageClass.findBarcodes()`
    """
    data = ""

    #given a ZXing bar
    def __init__(self, i, zbsymbol):
        self.image = i

        locs = zbsymbol.location
        if len(locs) > 4:
            xs = [l[0] for l in locs]
            ys = [l[1] for l in locs]
            xmax = np.max(xs)
            xmin = np.min(xs)
            ymax = np.max(ys)
            ymin = np.min(ys)
            points = ((xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin))
        else:
            points = copy(locs)  # hopefully this is in tl clockwise order

        super(Barcode, self).__init__(i, 0, 0, points)
        self.data = zbsymbol.data
        self.points = copy(points)
        numpoints = len(self.points)
        self.x = 0
        self.y = 0

        for pnt in self.points:
            self.x += pnt[0]
            self.y += pnt[1]

        if numpoints:
            self.x /= numpoints
            self.y /= numpoints

    def __repr__(self):
        return "%s.%s at (%d,%d), read data: %s" % (
            self.__class__.__module__, self.__class__.__name__, self.x, self.y,
            self.data)

    def draw(self, color=(255, 0, 0), width=1):
        """

        **SUMMARY**

        Draws the bounding area of the barcode, given by points.  Note that for
        QR codes, these points are the reference boxes, and so may "stray" into
        the actual code.


        **PARAMETERS**

        * *color* - An RGB color triplet.
        * *width* - if width is less than zero we draw the feature filled in,
         otherwise we draw the get_contour using the specified width.


        **RETURNS**

        Nothing - this is an inplace operation that modifies the source images
        drawing layer.


        """
        self.image.draw_line(self.points[0], self.points[1], color, width)
        self.image.draw_line(self.points[1], self.points[2], color, width)
        self.image.draw_line(self.points[2], self.points[3], color, width)
        self.image.draw_line(self.points[3], self.points[0], color, width)

    def length(self):
        """
        **SUMMARY**

        Returns the longest side of the quandrangle formed by the boundary
        points.

        **RETURNS**

        A floating point length value.

        **EXAMPLE**

        >>> img = Image("mycode.jpg")
        >>> bc = img.find_barcode()
        >>> print bc[-1].length()

        """
        sqform = spsd.squareform(spsd.pdist(self.points, "euclidean"))
        #get pairwise distances for all points
        #note that the code is a quadrilateral
        return max(sqform[0][1], sqform[1][2], sqform[2][3], sqform[3][0])

    def get_area(self):
        """
        **SUMMARY**

        Returns the area defined by the quandrangle formed by the boundary
        points


        **RETURNS**

        An integer area value.

        **EXAMPLE**

        >>> img = Image("mycode.jpg")
        >>> bc = img.find_barcode()
        >>> print bc[-1].get_area()


        """
        #calc the length of each side in a square distance matrix
        sqform = spsd.squareform(spsd.pdist(self.points, "euclidean"))

        #squareform returns a N by N matrix
        #boundry line lengths
        a = sqform[0][1]
        b = sqform[1][2]
        c = sqform[2][3]
        d = sqform[3][0]

        #diagonals
        p = sqform[0][2]
        q = sqform[1][3]

        #get_perimeter / 2
        s = (a + b + c + d) / 2.0

        #i found the formula to do this on wikihow.  Yes, I am that lame.
        #http://www.wikihow.com/Find-the-Area-of-a-Quadrilateral
        return sqrt(
            (s - a) * (s - b) * (s - c) * (s - d) - (a * c + b * d + p * q) *
            (a * c + b * d - p * q) / 4)
