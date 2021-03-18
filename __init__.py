from jina.executors.crafters import BaseCrafter

class Crafter(BaseCrafter):
    """
    :class:`Crafter` use TikaExtractor.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # your customized __init__ below
        raise NotImplementedError

    

    def craft(self, *args, **kwargs):
        raise NotImplementedError

    
