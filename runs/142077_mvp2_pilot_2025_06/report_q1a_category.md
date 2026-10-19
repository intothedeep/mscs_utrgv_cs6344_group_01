# Stage report: q1a_category

**What:** Q1a: does accuracy depend on the topic?

**Status:** failed: Traceback (most recent call last):
  File "/home/taeklim01/cs6330_polymarket/code/common.py", line 106, in run_stage
    fields = fn()
  File "/home/taeklim01/cs6330_polymarket/code/q1a_category.py", line 163, in work
    draw_calibration_by_category(bins, tab, out)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/taeklim01/cs6330_polymarket/code/q1a_category.py", line 129, in draw_calibration_by_category
    ax.errorbar(b["mean_price"], b["observed_rate"], yerr=err, fmt="o", ms=3.5, capsize=2, color="#222222")
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/taeklim01/myEnvs/cs6330/lib/python3.13/site-packages/matplotlib/_api/deprecation.py", line 477, in wrapper
    return func(*args, **kwargs)
  File "/home/taeklim01/myEnvs/cs6330/lib/python3.13/site-packages/matplotlib/__init__.py", line 1531, in inner
    return func(
        ax,
        *map(cbook.sanitize_sequence, args),
        **{k: cbook.sanitize_sequence(v) for k, v in kwargs.items()})
  File "/home/taeklim01/myEnvs/cs6330/lib/python3.13/site-packages/matplotlib/axes/_axes.py", line 4232, in errorbar
    raise ValueError(
        f"'{dep_axis}err' must not contain negative values")
ValueError: 'yerr' must not contain negative values

