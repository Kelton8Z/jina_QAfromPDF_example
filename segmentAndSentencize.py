from jina.hub.segmenters.nlp.PDFExtractorSegmenter import PDFExtractorSegmenter
from jina.hub.segmenters.nlp.Sentencizer import Sentencizer
from jina.hub.encoders.nlp.TransformerTFEncoder import TransformerTFEncoder

segmenter = PDFExtractorSegmenter()
segmentedPDFChunks = segmenter.segment(uri="/Users/kel/Downloads/LongTail.pdf",buffer=None)
#print(segmentedPDFChunks)
#img = segmentedPDFChunks[0]

txt = segmentedPDFChunks[-1]
#print(txt)
#print(segmentedPDFChunks)

sentencizer = Sentencizer()
sentencized = sentencizer.segment(txt)
print(sentencized)

transformerTFEncoder = TransformerTFEncoder()

for sentences in sentencized:
    transformed = transformerTFEncoder.encode(sentences)
    print(transformed)

'''
query = "question"
transformedQuery = transformerTFEncoder.encode(query)
'''
