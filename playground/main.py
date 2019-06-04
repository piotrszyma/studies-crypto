import sys
Z = int(sys.argv[1])

elements = set(element % Z for element in range(1, Z))

print('=' * 50)
print(f'Z: {Z} {elements}')

for element in elements:
  elements_generated_by = set()
  for i in range(Z):
    power_result = (element ** i) % Z
    if power_result in elements_generated_by:
      break
    elements_generated_by.add(power_result)

  print(
    f"""
({element}) {elements_generated_by} |{len(elements_generated_by)}|""", end='')

print()
QS = set(element ** 2 % Z for element in elements)

print(f'QS: {QS}')

print(f'Non QS: {elements - QS}')