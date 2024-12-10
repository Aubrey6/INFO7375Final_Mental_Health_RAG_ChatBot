import os
import json
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings


load_dotenv()


def embedding_document(path):
    embedding = OpenAIEmbeddings(
        model='text-embedding-3-small',
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    docs = []
    for filename in os.listdir(path):
        if filename != 'embed.json':
            with open('./documents/embed.json', 'r', encoding='utf-8') as f:
                files = json.load(f)
            if filename not in files.keys():
                files[filename] = False
            if not files[filename]:
                with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
                    data = f.read()
                    fields = data.split('\n\n\n')
                    for field in fields:
                        doc = Document(page_content=field, metadata={'file': filename})
                        docs.append(doc)
                    vector_store = FAISS.from_documents(docs, embedding)
                    if not os.path.exists('./vector_store/'):
                        os.makedirs('./vector_store/', exist_ok=True)
                        vector_store.save_local('./vector_store/')
                    else:
                        load_db = FAISS.load_local(
                            f'./vector_store/',
                            embedding,
                            allow_dangerous_deserialization=True
                        )
                        load_db.merge_from(vector_store)
                        load_db.save_local(f'./vector_store/')
                files[filename] = True
                with open('./documents/embed.json', 'w', encoding='utf-8') as f:
                    json.dump(files, f, ensure_ascii=False, indent=4)
    return {'statu': 'success', 'description': "vector store has been saved"}


if __name__ == '__main__':
    print(embedding_document(path='./documents/'))
