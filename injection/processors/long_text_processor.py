from llama_index.schema import TransformComponent, NodeRelationship, RelatedNodeInfo, TextNode
from llama_index.node_parser import SentenceSplitter
from transformers import BertTokenizerFast


class LongTextProcessor(TransformComponent):
    """
    Class to process long texts by tokenizing and splitting them into chunks while maintaining relationships between chunks.
    """


    class Config:
        """
        Configuration settings for LongTextProcessor.
        """
        allow_mutation = False  # Ensure the model is immutable

    MAX_TOKENS_DEFAULT: int = 512
    CHUNK_SIZE_DEFAULT: int = 233
    CHUNK_OVERLAP_DEFAULT: int = 36


    def __init__(self, max_tokens=MAX_TOKENS_DEFAULT, chunk_size=CHUNK_SIZE_DEFAULT, chunk_overlap=CHUNK_OVERLAP_DEFAULT):
        """
        Initializes LongTextProcessor with specified parameters.

        Args:
            max_tokens (int): Maximum number of tokens allowed per chunk.
            chunk_size (int): Size of each chunk.
            chunk_overlap (int): Overlap between consecutive chunks.
        """
        self.max_tokens = max_tokens
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap


    def __call__(self, nodes, **kwargs):
        """
        Process a list of text nodes by tokenizing and splitting long texts into chunks.

        Args:
            nodes (list of TextNode): List of input text nodes to be processed.
            **kwargs: Additional keyword arguments.

        Returns:
            list of TextNode: Processed text nodes.
        """
        new_nodes = []
        tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")

        for node in nodes:
            if len(node.get_content()) == 0 or node.text == "('text'='')":
                print("empty node")
                pass
            elif len(tokenizer.encode(node.text)) > self.max_tokens:
                new_nodes.extend(self._split_long_text(node))
            else:
                new_nodes.append(node)

        iterator = iter(new_nodes)
        updated_nodes = self._update_relationships(iterator)
        return list(updated_nodes)

    def _split_long_text(self, node):
        """
        Splits a long word into chunks of size CHUNK_SIZE.

        Args:
            node (TextNode): The node to be split.

        Yields:
            TextNode: Chunks of the node.
        """
        sentence_splitter = SentenceSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        content = sentence_splitter.split_text(node.text)
        chunks = []
        for text in content:
            yield TextNode(
                metadata=node.metadata,
                excluded_embed_metadata_keys=node.excluded_embed_metadata_keys,
                excluded_llm_metadata_keys=node.excluded_llm_metadata_keys,
                relationships=node.relationships,
                text=text,
                metadata_seperator=node.metadata_seperator,
                metadata_template=node.metadata_template,
                text_template=node.text_template,
            )

    def _update_relationships(self, iterator):
        """
        Generates a double linked list item from an iterator.

        Args:
            iterator: An iterator containing words.

        Yields:
            dict: A double-linked list item having previous, data and next attributes.
        """
        try:
            previous = next(iterator)
            current = next(iterator)
            previous.relationships= {
                NodeRelationship.SOURCE: current.relationships[NodeRelationship.SOURCE],
                NodeRelationship.NEXT: current.as_related_node_info()
            }

            previous.relationships[NodeRelationship.PREVIOUS] = current.as_related_node_info()
            yield previous

            while True:
                next_item = next(iterator)
                current.relationships = {
                    NodeRelationship.SOURCE: current.relationships[NodeRelationship.SOURCE],
                    NodeRelationship.PREVIOUS: previous.as_related_node_info(),
                    NodeRelationship.NEXT: next_item.as_related_node_info()
                }
                yield current
                previous, current = current, next_item

        except StopIteration:
            current.relationships = {
                NodeRelationship.SOURCE: current.relationships[NodeRelationship.SOURCE],
                NodeRelationship.PREVIOUS: previous.as_related_node_info()
            }
            yield current
