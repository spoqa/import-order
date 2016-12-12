import collections

__all__ = 'Item',

ImportItem = collections.namedtuple(
    'ImportItem',
    ['original_name', 'resolved_name', 'lineno', 'col_offset', 'relative']
)
