import random

key = [str(random.getrandbits(8)) for _ in range(256)]

print(f"""
static const unsigned int key[] = {{ {', '.join(key)} }};
""")