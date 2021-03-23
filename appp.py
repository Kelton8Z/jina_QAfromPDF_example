import os
import click
from jina.flow import Flow
from jina import Document
MAX_DOCS = int(os.environ.get("JINA_MAX_DOCS", 50))

def config():
    os.environ["JINA_DATA_FILE"] = os.environ.get(
        "JINA_DATA_FILE", "/Users/candice/Downloads/cats_are_awesome_text.pdf"
    )
    os.environ["JINA_WORKSPACE"] = os.environ.get("JINA_WORKSPACE", "workspace")
    os.environ["JINA_PORT"] = os.environ.get("JINA_PORT", str(45678))

def print_topk(resp, sentence):
    for d in resp.search.docs:
        print(f"Ta-Dah🔮, here are what we found for: {sentence}")
        for idx, match in enumerate(d.matches):
            score = match.score.value
            if score < 0.0:
                continue
            print(f'> {idx:>2d}({score:.2f}). {match.text}')

def search_generator(path: str, buffer: bytes):
    d = Document()
    d.mime_type = 'text/plain'
    if buffer:
        d.buffer = buffer
    if path:
        d.content = path
    yield d

def index():
    f = Flow().load_config("flows/index.yml")
    with f:
        data_path = os.path.join(os.path.dirname(__file__), os.environ.get('JINA_DATA_FILE', None))
        f.index(inputs=search_generator(path=data_path, buffer=None), read_mode='r')

def query(top_k):
    f = Flow().load_config("flows/query.yml")
    with f:
        while True:
            text = input("please type a sentence: ")
            if not text:
                break
            def ppr(x):
                print_topk(x, text)
            f.search_lines(lines=[text, ], line_format='text', on_done=ppr, top_k=top_k)

def query_restful():
    f = Flow().load_config("flows/query.yml")
    f.use_rest_gateway("45678")
    with f:
        f.block()

def dryrun():
    f = Flow().load_config("flows/index.yml")
    with f:
        f.dry_run()

@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(
        ["index", "query", "query_restful", "dryrun"], case_sensitive=False
    ),
)
#@click.option("--num_docs", "-n", default=MAX_DOCS)
@click.option("--top_k", "-k", default=5)
def main(task, top_k):
    config()
    workspace = os.environ["JINA_WORKSPACE"]
    if task == "index":
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
        query(top_k)
    if task == "query_restful":
        if not os.path.exists(workspace):
            print(f"The directory {workspace} does not exist. Please index first via `python app.py -t index`")
        query_restful()
    if task == "dryrun":
        dryrun()

if __name__ == "__main__":
    main()
