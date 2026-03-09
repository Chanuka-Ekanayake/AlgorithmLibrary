"""
Newton's Method for Optimization & Root Finding.
"""

from .newtons_method import newtons_method, newtons_method_root, newtons_method_optimization
from .newtons_method_multivariate import newtons_method_multivariate, \
    compute_jacobian, compute_hessian

__all__ = [
    'newtons_method',
    'newtons_method_root',
    'newtons_method_optimization',
    'newtons_method_multivariate',
    'compute_jacobian',
    'compute_hessian'
]
