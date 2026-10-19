# Stage report: q3_describe

**What:** Q3: summary statistics, histograms, ECDF, distribution fits, QQ plots, KS tests.

**Status:** failed: ": fit_and_ks(vol)},
                                ~~~~~~~~~~^^^^^^
  File "/home/taeklim01/cs6330_polymarket/code/q3_describe.py", line 37, in fit_and_ks
    ks_norm = stats.kstest(x, "norm", args=(mu, sd))
  File "/home/taeklim01/myEnvs/cs6330/lib/python3.13/site-packages/scipy/stats/_axis_nan_policy.py", line 601, in axis_nan_policy_wrapper
    res = hypotest_fun_out(*samples, **kwds)
  File "/home/taeklim01/myEnvs/cs6330/lib/python3.13/site-packages/scipy/_lib/_util.py", line 882, in wrapper
    return fun(*args, **kwargs)
  File "/home/taeklim01/myEnvs/cs6330/lib/python3.13/site-packages/scipy/stats/_stats_py.py", line 8413, in kstest
    return ks_1samp(xvals, cdf, args=args, alternative=alternative,
                    method=method, axis=axis, _no_deco=True)
  File "/home/taeklim01/myEnvs/cs6330/lib/python3.13/site-packages/scipy/stats/_axis_nan_policy.py", line 431, in axis_nan_policy_wrapper
    return hypotest_fun_in(*args, **kwds)
  File "/home/taeklim01/myEnvs/cs6330/lib/python3.13/site-packages/scipy/_lib/_util.py", line 882, in wrapper
    return fun(*args, **kwargs)
  File "/home/taeklim01/myEnvs/cs6330/lib/python3.13/site-packages/scipy/stats/_stats_py.py", line 7660, in ks_1samp
    cdfvals = _masked_apply(cdf, args=(x, *args), xp=xp)
  File "/home/taeklim01/myEnvs/cs6330/lib/python3.13/site-packages/scipy/_lib/_array_api.py", line 699, in _masked_apply
    return f(*args, **kwargs)
TypeError: ndtr() takes from 1 to 2 positional arguments but 3 were given

