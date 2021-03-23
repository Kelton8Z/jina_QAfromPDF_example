from jina import Encoder, Flow, Document, Indexer
import numpy as np
from jina.executors.indexers.keyvalue import BinaryPbIndexer

class MyEncoder(Encoder):
    def encode(self, data, *args, **kwargs):
        print(f'receiving {data}')

class MyIndexer(BinaryPbIndexer):
    def add(
        self, keys: Iterable[str], values: Iterable[bytes], *args, **kwargs
    ) -> None:
        print(f'receiving args = {args}, kwargs = {kwargs}')


f = Flow().add(uses='MyIndexer')

d = Document(text='hello world',
             embedding=np.array([1,2,3]))

with f:
    f.index(d)