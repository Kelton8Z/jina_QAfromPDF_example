# jina_QAfromPDF_example

Support query based on PDFs with Jina Box frontend @  https://jina.ai/jinabox.js/

Run 'python app.py --task index' to extract images and texts, sentencize text into sentences, encode sentences into embeddings

Then run 'python app.py --task query_restful' and input localhost:port to jina box's custom endpoint field to query on the PDF indexed 
