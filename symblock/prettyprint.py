
def TiledTensor_to_str(tiledtensor):
  rowindex_width = len(str(tiledtensor.get_tile_container_shape()[slice(None,-1)])) + (1 if tiledtensor._ndim is 2 else 2)
  array_title    = "{:{width}s} ".format("Tiles:", width=rowindex_width)
  label_width    = len(array_title)
  column_width   = len(str(tiledtensor.get_tile_container_shape()[slice(-1,None)]))
  label_format   = lambda tup : "{:{width}s}".format(str(tup)[:-1] + ('' if len(tup) is 1 else ','), width = label_width )
  column_format  = lambda tup : "{:{width}s}".format(str(tup[0]) +')'                              , width = column_width)
  element_format = lambda tile: "{:{width}s}".format('-' if tile.is_empty() else '#'               , width = column_width)
  rows           = tiledtensor.iter_tile_keys(slice(-1))
  cols           = [(partition_key,) for partition_key in tiledtensor._axes[-1].get_partition_keys()]
  string         = '  ' + array_title + ''.join(column_format(col) for col in cols) + '\n'
  for row in rows: string += '  ' + label_format(row) + ''.join(element_format(tiledtensor._tiles[row+col]) for col in cols) + '\n'
  for tile_key in tiledtensor.iter_tile_keys():
    if not tiledtensor.get_tile(tile_key).is_empty():
      ranges  = ','.join("{:d}-{:d}".format(offset, offset + size) for offset, size in zip(tiledtensor.get_tile_offset(tile_key),
                                                                                            tiledtensor.get_tile_shape (tile_key)))
      string += "\n  Tile {:s} holds elements ({:s}):\n    ".format(str(tile_key), ranges) + str(tiledtensor.get_tile(tile_key)).replace("\n","\n    ") + "\n"
  return "TiledTensor {{\n{:s}}}".format(string)
