from axis import PartitionedAxis

def test_get_dim______________1():
  assert PartitionedAxis(7).get_dim() == 7

def test_get_nparts___________1():
  assert PartitionedAxis(7).get_nparts() == 1

def test_get_partition_keys___1():
  assert PartitionedAxis(7).get_partition_keys() == [0]

def test_get_partition_sizes__1():
  assert PartitionedAxis(7).get_partition_sizes() == (7,)

def test_get_partition_starts_1():
  assert PartitionedAxis(7).get_partition_starts() == [0]

def test_get_partition_size___1():
  assert PartitionedAxis(7).get_partition_size(0) == 7

def test_get_partition_start__1():
  assert PartitionedAxis(7).get_partition_start(0) == 0

def test_get_partition_key____1():
  assert PartitionedAxis(7).get_partition_key(0) == 0
  assert PartitionedAxis(7).get_partition_key(1) == 0
  assert PartitionedAxis(7).get_partition_key(2) == 0
  assert PartitionedAxis(7).get_partition_key(3) == 0
  assert PartitionedAxis(7).get_partition_key(4) == 0
  assert PartitionedAxis(7).get_partition_key(5) == 0
  assert PartitionedAxis(7).get_partition_key(6) == 0

def test_get_relative_index___1():
  assert PartitionedAxis(7).get_relative_index(0) == 0
  assert PartitionedAxis(7).get_relative_index(1) == 1
  assert PartitionedAxis(7).get_relative_index(2) == 2
  assert PartitionedAxis(7).get_relative_index(3) == 3
  assert PartitionedAxis(7).get_relative_index(4) == 4
  assert PartitionedAxis(7).get_relative_index(5) == 5
  assert PartitionedAxis(7).get_relative_index(6) == 6

def test_get_dim______________2():
  assert PartitionedAxis((4,0,1,2)).get_dim() == 7

def test_get_nparts___________2():
  assert PartitionedAxis((4,0,1,2)).get_nparts() == 4

def test_get_partition_keys___2():
  assert PartitionedAxis((4,0,1,2)).get_partition_keys() == [0,1,2,3]

def test_get_partition_sizes__2():
  assert PartitionedAxis((4,0,1,2)).get_partition_sizes() == (4,0,1,2)

def test_get_partition_starts_2():
  assert PartitionedAxis((4,0,1,2)).get_partition_starts() == [0,4,4,5]

def test_get_partition_size___2():
  assert PartitionedAxis((4,0,1,2)).get_partition_size(0) == 4
  assert PartitionedAxis((4,0,1,2)).get_partition_size(1) == 0
  assert PartitionedAxis((4,0,1,2)).get_partition_size(2) == 1
  assert PartitionedAxis((4,0,1,2)).get_partition_size(3) == 2

def test_get_partition_start__2():
  assert PartitionedAxis((4,0,1,2)).get_partition_start(0) == 0
  assert PartitionedAxis((4,0,1,2)).get_partition_start(1) == 4
  assert PartitionedAxis((4,0,1,2)).get_partition_start(2) == 4
  assert PartitionedAxis((4,0,1,2)).get_partition_start(3) == 5

def test_get_partition_key____2():
  assert PartitionedAxis((4,0,1,2)).get_partition_key(0) == 0
  assert PartitionedAxis((4,0,1,2)).get_partition_key(1) == 0
  assert PartitionedAxis((4,0,1,2)).get_partition_key(2) == 0
  assert PartitionedAxis((4,0,1,2)).get_partition_key(3) == 0
  assert PartitionedAxis((4,0,1,2)).get_partition_key(4) == 2
  assert PartitionedAxis((4,0,1,2)).get_partition_key(5) == 3
  assert PartitionedAxis((4,0,1,2)).get_partition_key(6) == 3

def test_get_relative_index___2():
  assert PartitionedAxis((4,0,1,2)).get_relative_index(0) == 0
  assert PartitionedAxis((4,0,1,2)).get_relative_index(1) == 1
  assert PartitionedAxis((4,0,1,2)).get_relative_index(2) == 2
  assert PartitionedAxis((4,0,1,2)).get_relative_index(3) == 3
  assert PartitionedAxis((4,0,1,2)).get_relative_index(4) == 0
  assert PartitionedAxis((4,0,1,2)).get_relative_index(5) == 0
  assert PartitionedAxis((4,0,1,2)).get_relative_index(6) == 1
