# from slugify import slugify
from util import reverse_slug

# txt = "This is a test ---"
# print(slugify(txt))


array = ['unknown']
new_array = []
for i in array:
    new_array.append(reverse_slug(i))

print(new_array)