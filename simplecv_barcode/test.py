import os

from nose.tools import assert_equals, assert_almost_equals
from simplecv.factory import Factory
from simplecv.tests.utils import perform_diff
from simplecv.tests import utils
from simplecv import DATA_DIR as SCV_DATA_DIR

from simplecv_barcode import DATA_DIR

utils.standard_path = os.path.join(DATA_DIR, 'test', 'standard')

TEST_IMAGE = os.path.join(SCV_DATA_DIR, 'sampleimages/9dots4lines.png')
BARCODE_IMAGE = os.path.join(DATA_DIR, 'sampleimages/barcode.png')


def test_barcode():
    img = Factory.Image(BARCODE_IMAGE)
    barcode = img.find_barcode()[0]
    repr_str = "%s.%s at (%d,%d), read data: %s" % (
            barcode.__class__.__module__, barcode.__class__.__name__, barcode.x, barcode.y,
        barcode.data)
    assert_equals(barcode.__repr__(), repr_str)
    barcode.draw(color=(255, 0, 0), width=5)
    assert_equals(barcode.length(),[262.0])
    assert_almost_equals(barcode.get_area(), 68644.0)
    perform_diff([img], "test_barcode", 0.0)


def test_barcode_find_barcode():
    img = Factory.Image(BARCODE_IMAGE)
    featureset = img.find_barcode()
    f = featureset[0]
    img_crop = f.crop()
    result = [img_crop]
    name_stem = "test_barcode_find_barcode"
    perform_diff(result, name_stem, 0.0)


def test_detection_barcode():
    img1 = Factory.Image(TEST_IMAGE)
    img2 = Factory.Image(BARCODE_IMAGE)

    nocode = img1.find_barcode()
    if nocode:  # we should find no barcode in our test image
        assert False
    code = img2.find_barcode()
    code.draw()
    result = [img1, img2]
    name_stem = "test_detection_barcode"
    perform_diff(result, name_stem)
