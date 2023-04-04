# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 15:20:15 2023

@author: thomas
"""


from haystack.utils import launch_es
launch_es()

from haystack.document_stores.elasticsearch import ElasticsearchDocumentStore
document_store = ElasticsearchDocumentStore()

# It's a good idea to flush Elasticsearch with each notebook restart
if len(document_store.get_all_documents()) or len(document_store.get_all_labels()) > 0:
    document_store.delete_documents(index="document")
    document_store.delete_documents(index="label")

import json
  
f = open('sample.json', encoding='cp1252')
data = json.load(f)
docs = []    
    
answers = data['Answers']
question = data['Questions']

for i in range(len(answers)):
  doc = {"content" : answers[i], "answer" : question[i]}
  docs.append(doc)    
    
print(len(docs))
    
document_store.write_documents(documents=docs)
    
print(f"Loaded {document_store.get_document_count()} documents")

from haystack.nodes.retriever import BM25Retriever

bm25_retriever = BM25Retriever(document_store=document_store)

from haystack.nodes import FARMReader

model_ckpt = "etalab-ia/camembert-base-squadFR-fquad-piaf" #alternative larger models: deepset/roberta-base-squad2-distilled or deepset/xlm-roberta-large-squad2 or the tiny distilled model: deepset/tinyroberta-squad2
max_seq_length, doc_stride = 384, 128
reader = FARMReader(model_name_or_path=model_ckpt, progress_bar=False,
                    max_seq_len=max_seq_length, doc_stride=doc_stride, 
                    return_no_answer=False)

from haystack.pipelines import ExtractiveQAPipeline

pipe = ExtractiveQAPipeline(reader=reader, retriever=bm25_retriever)

import streamlit as st

query = st.text_input("Ecrivez votre questions")

if query:
    
    k = 5
    
    result = pipe.run(query=query, params={"Retriever": {"top_k": k}, "Reader": {"top_k": k}})
    
    
    if result['answers']:
        
        answers = []
        docs = []
        
        id_answers = []
        id_docs = []
        
        for i in range(k):
          answers.append(result['answers'][i].answer)
          docs.append(result['documents'][i].content)
          id_answers.append(result['answers'][i].document_ids[0])
          id_docs.append(result['documents'][i].id)
        
        buf = []
        for i in range(k):
          for j in range(k):
            if id_answers[j] == id_docs[i]:
              buf.append(answers[j])
        
        answers = buf
        
        for i in range(k):
          st.markdown("Réponse " + str(i + 1) + ":")
          index = docs[i].find(answers[i])
          st.markdown(docs[i][:index] + ":red[" + docs[i][index:index + len(answers[i])] + "]" +  docs[i][index + len(answers[i]):])
              
    else:
        st.markdown("Aucune réponse trouvé pour cette question.")









