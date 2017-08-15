from entry import Entry

def pdf_urlifier(entry):
    return entry.resource_id

def webpage_urlifier(entry):
    return entry.resource_id

urlifiers = {
    'web/pdf' : pdf_urlifier,
    'web': webpage_urlifier,
}

def urlify(entry):
    return urlifiers[entry.resource_type](entry)
