class ManyModelsView(object):
    def build_filter(self, title, name, values):
        return {
            'title': title,
            'id': name,
            'values': values
        }

    def create_key_value_dict(self, key, value):
        return {
            'key': key,
            'value': value
        }
