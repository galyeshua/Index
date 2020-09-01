from wtforms import FieldList
from wtforms.utils import unset_value


# override process func of FieldList to make it unordered
class UnorderedFieldList(FieldList):
    def process(self, formdata, data=unset_value, extra_filters=None):
        if extra_filters:
            raise TypeError(
                "FieldList does not accept any filters. Instead, define"
                " them on the enclosed field."
            )

        self.entries = []
        if not data:
            try:
                data = self.default()
            except TypeError:
                data = self.default

        self.object_data = data

        if formdata:

            indices = self._remove_duplicates(self._extract_indices(self.name, formdata))
            if self.max_entries:
                indices = indices[: self.max_entries]

            idata = iter(data)
            for index in indices:
                try:
                    obj_data = next(idata)
                except StopIteration:
                    obj_data = unset_value
                self._add_entry(formdata, obj_data, index=index)
        else:
            for obj_data in data:
                self._add_entry(formdata, obj_data)

        while len(self.entries) < self.min_entries:
            self._add_entry(formdata)

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive, but case preserving manner"""
        d = {}
        for item in seq:
            if item not in d:
                d[item] = True
                yield item
