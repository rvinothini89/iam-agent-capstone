import json
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from dotenv import load_dotenv
import os

load_dotenv()
# Load policies
with open("data/policies.json", "r") as f:
    policies = json.load(f)

docs = []

# Flatten policies → text
for policy in policies.get("policies", []):
    text = f"""
Policy ID: {policy.get('id')}
Resource: {policy.get('resource')}
Allowed Roles: {policy.get('allowed_roles')}
Access Type: {policy.get('access_type')}
Conditions: {policy.get('conditions', {})}
Risk: {policy.get('risk', 'unknown')}
"""
    docs.append(Document(page_content=text.strip()))

print("Total docs created:", len(docs))
print("Sample doc:", docs[0] if docs else "NO DOCS")

# Create embeddings + FAISS index
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(docs, embeddings)

# Save locally
db.save_local("rag/faiss_index")

print("FAISS index created!")
