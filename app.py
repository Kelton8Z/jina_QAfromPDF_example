#from jina.hub.crafters.nlp.TikaExtractor import TikaExtractor
from jina.hub.segmenters.nlp.PDFExtractorSegmenter import PDFExtractorSegmenter

from jina.flow import Flow
import click
import os

def config():
    os.environ.setdefault('JINA_WORKSPACE', './workspace')
    os.environ.setdefault('JINA_PORT', str(65481))

def input_fn():
    print("file processed")
    segmenter = PDFExtractorSegmenter()
    segmentedPDFChunks = segmenter.segment(uri='/Users/kel/Downloads/Engineer\ Onboarding\ Guide.pdf',buffer=None)
    img = segmentedPDFChunks[0]
    txt = segmentedPDFChunks[1]
    print(type(txt))
    '''with Document() as d:
	d.tags = img
        d.tags = txt
    yield d
    '''

def index():
    print("indexed")
    f = Flow().load_config("flows/index.yml")

    with f:
        f.index(input_Fn)

#def printTopK():

def query():
    f = Flow().load_config("flows/query.yml")
    with f:
        f.block() #printTopK()

def query_restful():
    f = Flow().load_config("flows/query.yml")
    f.use_rest_gateway()
    with f:
        f.block()  

def dryrun():
    f = Flow().load_config("flows/index.yml")
    with f:
        pass

'''
def search_generator(path: str, buffer: bytes):
    d = jina_pb2.Document()
    if buffer:
        d.buffer = buffer
    if path:
        d.uri = path
    yield d

def validate_mix_fn(resp):
    for d in resp.search.docs:
        for chunk in range(len(d.chunks) - 1):
            img = Image.open(os.path.join(cur_dir, f'test_img_{chunk}.jpg'))
            blob = d.chunks[chunk].blob
            assert blob.shape[1], blob.shape[0] == img.size
        assert expected_text == d.chunks[2].text

def test_pdf_flow_mix():
    path = os.path.join(cur_dir, 'cats_are_awesome.pdf')
    f = Flow().add(uses='PDFExtractorSegmenter', array_in_pb=True)
    with f:
        f.search(input_fn=search_generator(path=path, buffer=None), output_fn=validate_mix_fn)

'''

@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(
        ["index", "query", "query_restful", "dryrun"], case_sensitive=False
    ),
)
def main(task):
    config()
    workspace = os.environ["JINA_WORKSPACE"]
    if task == "index":
        print("indexing")
        if os.path.exists(workspace):
            print(f'\n +----------------------------------------------------------------------------------+ \
                    \n |                                   🤖🤖🤖                                         | \
                    \n | The directory {workspace} already exists. Please remove it before indexing again.  | \
                    \n |                                   🤖🤖🤖                                         | \
                    \n +----------------------------------------------------------------------------------+')
        index()
    if task == "query":
        if not os.path.exists(workspace):
            print(f"The directory {workspace} does not exist. Please index first via `python app.py -t index`")
        query()
    
    if task == "query_restful":
        if not os.path.exists(workspace):
            print(f"The directory {workspace} does not exist. Please index first via `python app.py -t index`")
        query_restful()
    
    if task == "dryrun":
        dryrun()

if __name__ == "__main__":
    main()
