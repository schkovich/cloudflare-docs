import os
import openai
import nest_asyncio
from llama_index.node_parser import MarkdownNodeParser
from llama_index import ServiceContext
from llama_index.llms import OpenAI
from llama_index.extractors import (
    SummaryExtractor,
    TitleExtractor,
    KeywordExtractor,
)
from llama_index.ingestion import IngestionPipeline
from processors.long_text_processor import LongTextProcessor

nest_asyncio.apply()
parser = MarkdownNodeParser.from_defaults()

# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY_HERE"
openai.api_key = os.environ["OPENAI_API_KEY"]
# from llama_index.schema import MetadataMode
llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo", max_tokens=512)
extractors = [
    TitleExtractor(nodes=5, llm=llm),
    SummaryExtractor(summaries=["prev", "self"], llm=llm),
    KeywordExtractor(keywords=10, llm=llm),
]
transformations = [parser, ltp] + extractors


class ContentProcessor:


    def __init__(self, parser, extractors, ltp):
        self.parser = parser
        self.extractors = extractors
        self.ltp = ltp


    def set_transformations(parser, long_text_processor, extractors):
        self.transformations = [parser, ltp] + extractors


    def process_content(self, content):
        pipeline = IngestionPipeline(transformations=self.transformations)
        context = pipeline.run(documents=content)
        pipeline.persist("./d1_cache_639e6b2")
        return context
