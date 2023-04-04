# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 16:28:29 2023

@author: thomas
"""

from haystack.utils import launch_es
launch_es()

from haystack.document_stores import InMemoryDocumentStore

document_store = InMemoryDocumentStore()

# It's a good idea to flush Elasticsearch with each notebook restart
if len(document_store.get_all_documents()) or len(document_store.get_all_labels()) > 0:
    document_store.delete_documents(index="document")
    document_store.delete_documents(index="label")

import json
  
from haystack.nodes import EmbeddingRetriever

f = open('sample.json', encoding='cp1252')
data = json.load(f)
docs = []
    
answers = data['Answers']
question = data['Questions']

f = open('emb.json', encoding='cp1252')
emb = json.load(f)
emb = emb["emb"]

for i in range(len(question)):
  doc = {"content" : question[i], "answer" : answers[i],'embedding' : emb[i]}
  docs.append(doc)    
  
document_store.write_documents(docs)

retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="dangvantuan/sentence-camembert-base",
    use_gpu=True,
    scale_score=False,
)
    
print(f"Loaded {document_store.get_document_count()} documents")

from haystack.nodes.retriever import BM25Retriever

bm25_retriever = BM25Retriever(document_store=document_store)

from haystack.nodes import FARMReader

from haystack.pipelines import ExtractiveQAPipeline

from haystack.pipelines import FAQPipeline

pipe = FAQPipeline(retriever=retriever)

import streamlit as st

query = "Comment me faire rembourser ?"

result = pipe.run(query=query, params={"Retriever": {"top_k": 5}})
print()

for i in result['answers']:
    print(i.answer)
    print()

query = st.text_input("Ecrivez votre questions")

if query:
    
    k = 5
    
    result = pipe.run(query=query, params={"Retriever": {"top_k": k}})
    print(result)
    
    if result['answers']:
    
        
        for ind,r in enumerate(result['answers']):
          st.markdown("Réponse " + str(ind + 1) + ":")
          st.markdown(r.answer)
          
    else:
        st.markdown("Aucune réponse trouvé pour cette question.")