from collections import UserDict, defaultdict

import ngram


class Engine(UserDict):
    """
    This class allows to index and search documents. Result of the search is sorted by the best match.

    Example:
        class Person:
            def __init__(self, name, email):
                self.name = name
                self.email = email

        engine = Engine(["name", "email"])
        engine.add_to_index(Person("John Doe", "findmeinthemorgue@gmail.com"))
        engine.add_to_index(Person("Jane Doe", "findmeinnearjohn@gmail.com"))

        result = engine.search("one")

    :param fields: list of fields to index and search by. Those fields MUST support casting to string
    :param search_threshold: allows to make search more or less strict
    """
    def __init__(self, fields: list, search_threshold: float = 0.2):
        super().__init__()

        self.__fields = fields
        self.__search_threshold = search_threshold

        self.__rebuild_index()

    def add_to_index(self, entity_id, entity):
        """
        :param entity_id: id of the entity
        :param entity: object to be indexed
        :return:
        """
        self.data[entity_id] = entity

        self.__rebuild_index()

    def remove_from_index(self, entity_id):
        del self.data[entity_id]

        self.__rebuild_index()

    def find(self, search_string: str) -> list:
        result = []
        found_items = {}

        keys = []
        for key in self.__index.keys():
            keys.append(str(key))

        ng = ngram.NGram(keys, N=2)
        for value, weight in ng.search(search_string):
            if weight < self.__search_threshold:
                continue

            for entity_id in self.__index[value]:
                if entity_id in found_items:
                    continue

                result.append(self.data[entity_id])
                found_items[entity_id] = True

        return result

    def __rebuild_index(self):
        self.__index = defaultdict(set)

        for entity_id, entity in self.data.items():
            for field in self.__fields:
                field_value = getattr(entity, field)

                self.__index[str(field_value)].add(entity_id)