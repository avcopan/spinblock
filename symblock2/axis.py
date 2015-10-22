class PartitionedAxis(object):

  def __init__(self, partition_sizes):
    if isinstance(partition_sizes, int): partition_sizes = (partition_sizes,)
    self.dim             = sum  (partition_sizes)
    self.npartitions     = len  (partition_sizes)
    self.partition_sizes = tuple(partition_sizes)
    self.partition_keys  = range(self.npartitions)

  def __repr__(self):
    return 'PartitionedAxis: {:d} -> {:s}'.format(self.dim, str(self.partition_sizes))
