class FilterHelpersMixin(object):
    def build_filter(self, title, name, values):
        """
        Create dict for filter values
        :param title: view title
        :param name: key for model
        :param values: list values
        :return: dict
        """
        return {
            'title': title,
            'id': name,
            'values': values
        }

    def create_key_value_dict(self, key, value):
        """
        Create dict for model list
        :param key: model key
        :param value: model value
        :return: dict
        """
        return {
            'key': key,
            'value': value
        }
