class TestUtilsClass(object):
    def test_totuple(self):
        from koh.utils import totuple
        import numpy as np

        a = [0, 1, 2, 3]

        a_tuple = totuple(a)

        assert(len(a) == len(a_tuple))
        assert(isinstance(a_tuple, tuple))

        a_np = np.array(a)
        a_tuple = totuple(a_np)

        assert(len(a) == len(a_tuple))
        assert(isinstance(a_tuple, tuple))

    def test_get_bounds_2d(self):
    	from koh.utils import get_bounds_2d
    	import numpy as np

    	pt_a = (0, 20)
    	pt_b = (50, 80)

    	(x, y, right, bottom) = get_bounds_2d([pt_a, pt_b])

    	assert((x, y) == pt_a)
    	assert((right, bottom) == pt_b)

    	pt_c = (40, 70)
    	(x, y, right, bottom) = get_bounds_2d([pt_a, pt_b, pt_c])

    	assert((x, y) == pt_a)
    	assert((right, bottom) == pt_b)


    	pt_d = (-20, 70)

    	(x, y, right, bottom) = get_bounds_2d([pt_a, pt_b, pt_c, pt_d])

    	assert((x, y) == (pt_d[0], pt_a[1]))
    	assert((right, bottom) == pt_b)
