class PartitionedAxis(object):

  def __init__(self, partition_sizes):
    if isinstance(partition_sizes, int): partition_sizes = (partition_sizes,)
    self._dim              = sum(partition_sizes)
    self._npartitions      = len(partition_sizes)
    self._partition_keys   = range(self._npartitions)
    self._partition_sizes  = partition_sizes
    self._partition_starts = [sum(partition_sizes[:i]) for i in self._partition_keys]
    self._partition_stops  = self._partition_starts[1:] + [self._dim]
    self._partitions       = [range(start, stop) for start, stop in zip(self._partition_starts, self._partition_stops)]

  def __repr__(self): return 'PartitionedAxis: {:d} -> {:s}'.format(self.get_dim(), str(self.get_partition_sizes()))

  def get_dim             (self): return self._dim
  def get_npartitions     (self): return self._npartitions
  def get_partition_keys  (self): return self._partition_keys
  def get_partition_sizes (self): return self._partition_sizes
  def get_partition_starts(self): return self._partition_starts
  def get_partition_size (self, partition_key): return self._partition_sizes [partition_key]
  def get_partition_start(self, partition_key): return self._partition_starts[partition_key]

  def get_partition_key(self, index):
    partition_key = next((key for key, partition in zip(self._partition_keys, self._partitions)
                                                 if fits_in(index, partition)), None)
    if not isinstance(partition_key, int):
      raise Exception("Invalid key {:s} used for {:s}-partitioned axis.".format(str(index), str(self._partition_sizes)))
    else:
      return partition_key

  def get_subkey(self, index):
    partition_start = self.get_partition_start(self.get_partition_key(index))
    if   isinstance(index,   int): return index - partition_start
    elif isinstance(index, slice): return slice(index.start - partition_start, index.edn - partition_end)
    

def fits_in(index, arange):
  if   isinstance(index,   int): return index in arange
  elif isinstance(index, slice): return index.start in arange and index.stop - 1 in arange

