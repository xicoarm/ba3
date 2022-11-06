import os


result = os.popen('alpr car2.jpeg').read()

start = result.find('- ')
end = result.find('confidence', start)

result = result[start + 2: end]

print(result)
