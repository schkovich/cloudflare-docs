import json

class ContextPersister:
    def __init__(self, sqlite_persister):
        self.sqlite_persister = sqlite_persister

    def get_relationships(self, relationships):
        return {
               'source': vars(relationships['1']) if "1" in relationships else "{}",
               'previous': vars(relationships['2']) if "2" in relationships else "{}",
               'next': vars(relationships['3']) if "3" in relationships else "{}"
           }

    def get_content(self, chunk):
        return [
               chunk.id_,
               json.dumps(chunk.embedding),
               json.dumps(chunk.metadata),
               json.dumps(chunk.excluded_embed_metadata_keys),
               json.dumps(chunk.excluded_llm_metadata_keys),
               json.dumps(self.get_relationships(chunk.relationships),
               chunk.hash,
               chunk.text,
               chunk.start_char_idx,
               chunk.end_char_idx,
               chunk.text_template,
               chunk.metadata_template,
               chunk.metadata_seperator
           ]
    def get_sql(self):
        return '''INSERT INTO LLamaNodes (idx, embedding, metadata, excluded_embed_metadata_keys, excluded_llm_metadata_keys, relationships, hash,
                               text, start_char_idx, end_char_idx, text_template, metadata_template, metadata_seperator)
                             VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) '''

    def persist_context(self, context):
        self.sqlite_persister.connect()
        for chunk in context:
            self.sqlite_persister.persist_data(self.get_sql(), self.get_content(chunk)
        self.sqlite_persister.disconnect()
