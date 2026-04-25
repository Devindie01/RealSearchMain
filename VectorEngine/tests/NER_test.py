import spacy
import torch
import numpy as np
# This import is CRITICAL to register 'trf_data'
try:
    import spacy_transformers
except ImportError:
    print("❌ spacy_transformers not found. Run: pip install spacy-transformers")

# Point this to your model-best folder
MODEL_PATH = r"D:\FYP\RealSearch\VectorEngine\models\Best Model\output\model-best"

try:
    nlp_ner = spacy.load(MODEL_PATH)
    print("🚀 Model Loaded Successfully!")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    exit()

def get_slot_confidences(text):
    doc = nlp_ner(text)
    
    # 1. Double check if trf_data exists now
    if not hasattr(doc._, "trf_data") or doc._.trf_data is None:
        raise AttributeError("The model did not produce transformer data. Check if 'transformer' is in nlp.pipe_names")

    trf_data = doc._.trf_data
    
    # 2. Extract Logits and Apply Softmax
    # trf_data.model_outputs.logits is a list of tensors (usually length 1 for one sentence)
    logits = torch.from_numpy(trf_data.model_outputs.logits[-1]) 
    probs = torch.nn.functional.softmax(logits, dim=-1).numpy()
    
    # 3. Get NER Label Mapping
    ner_pipe = nlp_ner.get_pipe("ner")
    labels = ner_pipe.labels
    label_to_idx = {label: i for i, label in enumerate(labels)}
    
    results = []
    
    for ent in doc.ents:
        label_idx = label_to_idx.get(ent.label_)
        confidences = []
        
        for token in ent:
            # Get alignment between spaCy tokens and Transformer wordpieces
            # doc._.trf_data.align is a RaggedArray mapping spaCy tokens to trf tokens
            trf_indices = trf_data.align[token.i].data.flatten()
            
            for idx in trf_indices:
                # Get probability for the predicted label at this wordpiece index
                wordpiece_prob = probs[idx][label_idx]
                confidences.append(wordpiece_prob)
        
        # Calculate mean confidence for the slot (c_i)
        c_i = np.mean(confidences) if confidences else 0.0
        
        results.append({
            "slot": ent.label_,
            "value": ent.text,
            "confidence": round(float(c_i), 4)
        })
        
    return results

# Final Test
query = "I'm looking for a 2 bedroom apartment for rent in Colombo 03 below 150,000 LKR"

try:
    analysis = get_slot_confidences(query)
    print(f"\nAnalysis for: '{query}'")
    print("-" * 65)
    for r in analysis:
        print(f"Slot: {r['slot']:15} | c_i: {r['confidence']:.4f} | Value: {r['value']}")
except Exception as e:
    print(f"Detailed Error: {e}")