# DocumentGPT

### What is document GPT?
#### Document GPT lets you to upload a PDF or TEXT file and ask any questions related to it and the LLM model answers the questions for you.
![image](https://github.com/PraghadeeshLife/documentGPT1311/assets/102030901/92cd7fcb-3b92-47c4-bd22-e48aeeee4efc)

Document GPT was build with the following tech stack
- Reflex (Used for the UI)
- Supabase (Postgres as Vector Database using pgvector extension)
- Langchain Framework
- OpenAI API for embeddings and as LLM (WIP: Using open source LLM Models)

## Guide to self host
##### Step 1
Git clone the repository and replace the API Keys with your own API Keys (for OpenAI and Supabase) in the .env file
```
OPENAI_API_KEY=YOUR_KEY
SUPABASE_URL=YOUR_KEY
SUPABASE_KEY=YOUR_KEY
```

##### Step 2
Once the Supabase Project has been created, enable pgvector extension and run the following SQL Query in the Supabase's SQL Editor
```
       -- Enable the pgvector extension to work with embedding vectors
       create extension vector;

       -- Create a table to store your documents
       create table documents (
       id uuid primary key,
       content text, -- corresponds to Document.pageContent
       metadata jsonb, -- corresponds to Document.metadata
       embedding vector(1536) -- 1536 works for OpenAI embeddings, change if needed
       );

       CREATE FUNCTION match_documents(query_embedding vector(1536), match_count int)
           RETURNS TABLE(
               id uuid,
               content text,
               metadata jsonb,
               -- we return matched vectors to enable maximal marginal relevance searches
               embedding vector(1536),
               similarity float)
           LANGUAGE plpgsql
           AS $$
           # variable_conflict use_column
       BEGIN
           RETURN query
           SELECT
               id,
               content,
               metadata,
               embedding,
               1 -(documents.embedding <=> query_embedding) AS similarity
           FROM
               documents
           ORDER BY
               documents.embedding <=> query_embedding
           LIMIT match_count;
       END;
       $$;
```

##### Step 3
Install the requirements mentioned in the requirements.txt file, apart from the requirements mentioned in the text file. We also need NodeJS for the frontend with a v19.4.0 or greater.

##### Step 4
After the above steps, we'll have to initialize reflex
```
cd documentGPT1311
reflex init
reflex run
```

##### Now the program should be up and live at http://localhost:3000, try it out!

You can upload the files by clicking the Avatar on the top right, and click upload files with the PDF or TEXT file of your choice and the program will ingest the data as vector.
