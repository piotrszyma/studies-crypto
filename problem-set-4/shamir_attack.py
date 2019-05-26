import math

import merkle_hellman_cryptosystem as mhc



def get_int_prog_solutions(n, g, B):
  """Generates integer program solutions for provided params.

  """
  pass


def gen_superinc_seq(n, g, start=1, prev_sum=0): # TODO: start = 0 or 1 ?
  """Generates superincreasing sequences in increasing order.

  Args:
    g: (int) size of superincreasing sequence.
    n: (int) expected size of superincreasing sequence.

  Returns:
    Generator that yields superincreasing sequences.
  """
  # n = 6
  # g = 3
  # [1, [sum(prev) + 1, n]]
  # []
  if g == 0:
    yield []
    return

  for num in range(prev_sum + 1, n + 1):
    for suffix in gen_superinc_seq(
        n, g - 1, start=start+1, prev_sum=prev_sum+num):
      yield [num, *suffix]

def assert_superinc(sequence):
  for idx, element in enumerate(sequence):
    assert element > sum(sequence[:idx])

def main():
  message = b'test msg'
  message_bits = mhc.bytes_to_bits_array(message)

  priv_key, public_key = mhc.key_gen(msg_len=len(message_bits))

  # Assuming you have only public_key, get priv_key

  a = public_key['a']
  n = len(a)

  M_tilde = max(a)
  d_star = math.floor(1/n * math.log2(n ** 2 * M_tilde))

  g = max(d_star + 2, 5)

  # sequences = list(gen_superinc_seq(n, g))

  for sequence in gen_superinc_seq(n, g):
    assert_superinc(sequence)
  import pdb; pdb.set_trace()
  # for sequence in sequences:
  #   pass
  # assert_superinc([1, 2, 4])
  # import pdb; pdb.set_trace()
  # for sequence in gen_superinc_seq(n, g):
  #   import pdb; pdb.set_trace()


if __name__ == "__main__":
  main()