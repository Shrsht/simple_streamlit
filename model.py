from keybert import KeyBERT


kb = KeyBERT()
keywords = kb.extract_keywords(resume_text, stop_words = 'english',
                               keyphrase_ngram_range = (1,3),
                               nr_candidates= 0.2*len(resume_text),
                               use_mmr = True,
                               top_n = 20,
                               diversity = 0.8,)

