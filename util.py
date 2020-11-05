def reverse_slug(slug):
    slug = slug.replace('-', ' ')
    return slug.title()

def remove_bad_words(name):
    bad_words = ['actor', 'brazilian', 'actress', 'presenter']
    name = name.lower()
    
    for word in bad_words:
        if word in name:
            name = name.replace(word, '')

    return name