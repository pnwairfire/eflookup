__author__      = "Joel Dubowy"

__version_info__ = (3,2,1)
__version__ = '.'.join([str(n) for n in __version_info__])

__all__ = [
    'Phase'
]

class Phase:
    FLAMING = 'flaming'
    SMOLDERING = 'smoldering'
    RESIDUAL = 'residual'
    ALL = set([FLAMING, SMOLDERING, RESIDUAL])
