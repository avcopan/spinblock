import pandas as pd

def prettyprint(blockedarray):
  return "Axes:\n"                + get_axes_descriptor_string           (blockedarray) + \
         "\n\nBlock Structure:\n" + get_block_structure_descriptor_string(blockedarray) + \
         "\n\nActive Blocks:\n"   + get_active_blocks_string             (blockedarray)
  
def get_block_string(blockedarray, block_keys):
  key    = str(block_keys)
  offset = str(blockedarray.get_block_offset(block_keys))
  shape  = str(blockedarray.get_block_shape (block_keys))
  block  = str(blockedarray.get_block       (block_keys).round(4))
  fillstr = "  Block # {:s}:\n    {:8s} = {:s}\n    {:8s} = {:s}\n{:s}"
  return fillstr.format(key, "offset", offset, "shape", shape, block)

def get_axes_descriptor_string(blockedarray):
  col_labels = ['shape'     , 'block shapes'     , 'block offsets'      , 'block keys'       ]
  data_rows = [[ax.get_dim(), ax.get_block_dims(), ax.get_block_starts(), ax.get_block_keys()] for ax in blockedarray.iter_axes()]
  return pd.DataFrame(data_rows, columns=col_labels).__repr__()

def get_block_structure_descriptor_string(blockedarray):
  col_keys  = list((key,) for key in blockedarray.get_axis(-1).get_block_keys())
  row_keys  = (reversed_key[::-1] for reversed_key in blockedarray.iter_block_keys(slc = slice(-2,None,-1)))
  data_rows = []
  for row_key in row_keys:
    row_label = str(row_key)[:-1] + (',' if len(row_key) > 1 else '')
    row = [not isinstance(blockedarray.get_block(row_key + col_key), float) for col_key in col_keys]
    data_rows.append( (row_label, row) )
  col_labels = [str(col_key) + ')' for col_key, in col_keys]
  return pd.DataFrame.from_items(data_rows, orient='index', columns=col_labels).__repr__()

def get_active_blocks_string(blockedarray):
  active_block_keys = (block_key for block_key in blockedarray.iter_block_keys()
                                               if not isinstance(blockedarray.get_block(block_key), float))
  return '\n'.join(get_block_string(blockedarray, active_block_key) for active_block_key in active_block_keys)
