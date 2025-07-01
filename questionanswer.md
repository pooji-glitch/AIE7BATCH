#### ❓Question #1:
1. Is there any way to modify this dimension?
2. What technique does OpenAI use to achieve this?
##### ✅ Answer:
1.yes we can change the modify the dimension by using using the optional dimensions parameter.
2.OpenAI uses Reducing embedding dimensions technique to modify the dimensions.


#### ❓Question #2:
What are the benefits of using an `async` approach to collecting our embeddings?
##### ✅ Answer:
Using an async approach allows multiple embedding requests to run concurrently, without waiting for each one to finish before starting the next. This is faster and more efficient, especially when embedding many texts.
Core difference:
sync = waits for each task to finish one-by-one
async = handles multiple tasks at once, improving speed and resource use


#### ❓ Question #3:
When calling the OpenAI API - are there any ways we can achieve more reproducible outputs?
##### ✅ Answer:
To achieve more reproducible outputs when calling the OpenAI API, we can set the seed parameter in our request. This makes the model's behavior deterministic, so the same input will return the same output every time (if other parameters are unchanged).

#### ❓ Question #4:
What prompting strategies could you use to make the LLM have a more thoughtful, detailed response?
What is that strategy called?
##### ✅ Answer:
To encourage more thoughtful and detailed responses from an LLM, we can use Chain-of-Thought Prompting. This strategy asks the model to explain its reasoning step by step, rather than providing an answer immediately.
Other helpful prompting strategies include:
Few-shot prompting: Give examples of detailed responses first.
Explicit instructions: Ask the model directly to "explain in detail" or "reason step by step."


ACTIVITY 

## importing pdf file 
mport pdfplumber

pdf_path = "data/marc.pdf"
all_text = ""
with pdfplumber.open(pdf_path) as pdf:
       for page in pdf.pages:
           all_text += page.extract_text() + "\n"

print(all_text)




## implemeting a new distance metrix 

mport numpy as np

# Example function
def manhattan_distance(v1, v2):
    return np.sum(np.abs(v1 - v2))

# Retrieve closest vectors using the new metric
def get_top_k(query_vector, db_vectors, k=2):
    return sorted(
        db_vectors,
        key=lambda x: manhattan_distance(query_vector, x[1])
    )[:k]

#####diagram
 ┌────────────────────┐
 │   PDF File Input   │
 └────────┬───────────┘
          │
 ┌────────▼───────────┐
 │ Document Loader     │ ← (PyPDFLoader)
 └────────┬───────────┘
          │
 ┌────────▼───────────┐
 │ Text Splitter      │ ← (RecursiveCharacterTextSplitter)
 └────────┬───────────┘
          │
 ┌────────▼───────────┐
 │ Embedder (OpenAI)  │
 └────────┬───────────┘
          │
 ┌────────▼───────────┐
 │ Vector DB + Metadata│
 └────────┬───────────┘
          │
 ┌────────▼───────────┐
 │ Retrieve Top-K Docs │ ← (with custom distance metric)
 └────────┬───────────┘
          │
 ┌────────▼───────────┐
 │ LLM Prompt + Answer │
 └────────────────────┘






