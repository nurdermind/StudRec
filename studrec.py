import pickle

import numpy as np
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.neighbors import NearestNeighbors


class StudRec:

    def __init__(self, dataset: pd.DataFrame, n_neighbors=5, algorithm='brute'):
        self.dataset = dataset
        self._dataset = None
        self._vec = DictVectorizer()
        self._nbrs = NearestNeighbors(
            n_neighbors=n_neighbors,
            algorithm=algorithm
        )

    def fit(self):
        df = self.dataset.drop(['name', 'rank'], axis=1)
        data = self._prepare_fit_data(df.to_dict(orient='records'))
        self._nbrs.fit(data)

    def find(self, students: list[dict]) -> list[dict]:
        data = self._prepare_data(students)
        founded_indexes = self._find_indexes(data)
        found_data = []

        for indexes in founded_indexes:
            tmp_df = self.dataset.iloc[indexes]
            tmp_df['student_id'] = tmp_df.index
            found_data.append(tmp_df.to_dict(orient='records'))
        return found_data

    def find_indexes(self, students: list[dict]) -> list[list[int]]:
        data = self._prepare_data(students)
        founded_indexes = self._find_indexes(data)
        found_data = []

        for indexes in founded_indexes:
            found_data.append(list(self.dataset.iloc[indexes].index))
        return found_data

    def _find_indexes(self, data):
        distances, indexes = self._nbrs.kneighbors(data)
        return indexes

    def _prepare_fit_data(self, data) -> np.array:
        return self._vec.fit_transform(data).toarray()

    def _prepare_data(self, data) -> np.array:
        return self._vec.transform(data).toarray()

    def save_vec_nbrs_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self._vec, self._nbrs), file)

    def load_vec_nbrs_from_file(self, filename, *args, **kwargs):
        with open(filename, 'rb') as file:
            vec, nbrs = pickle.load(file)
            self._vec = vec
            self._nbrs = nbrs
