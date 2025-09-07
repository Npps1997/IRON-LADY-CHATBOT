from langchain_cohere import CohereEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

# Example Iron Lady program content (later, scrape from website)
ironlady_text = """
Welcome to Iron Lady - Empower Your Leadership Journey!
Program: Iron Lady offers the Leadership Essentials Program.
Duration: 4 weeks with 1 year community membership.
Mode: Online with live interactive sessions.
Certificate: Yes, provided on successful completion.
Mentors: Experienced leadership coaches and industry experts : Rajesh Bhat (Founder and Director of Iron Lady), Suvarna Hegde (Founder aand CEO),
Simon Newman (Cofounder and Chairman) and many other.
Payment: Could be online via credit/debit cards, UPI, net banking and EMI Option is also possible.
Price: 35,000 INR + GST.
Scholarships: Yes, available based on merit and need.
"""

# Convert to docs
docs = [Document(page_content=ironlady_text)]

# Split text into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# Create embeddings
embeddings = CohereEmbeddings(model="embed-english-v3.0")

# Store in FAISS
vectorstore = FAISS.from_documents(chunks, embeddings)

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
# for doc in retriever.invoke("What is the duration of the Leadership Essentials Program?"):
#     print(doc.page_content)