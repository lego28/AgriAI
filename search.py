from pymongo import MongoClient
import json
import re

# ----------------- CONFIG -----------------
client = MongoClient("mongodb://localhost:27017/")
db = client["cocosense"]

searchnames_col = db["searchnames"]
byproducts_col = db["byproducts"]
downstreamproducts_col = db["downstreamproducts"]
products_col = db["products"]
# ------------------------------------------

def normalize_text(text):
    """Normalize double vowels and split into word list."""
    text = text.lower()
    # Replace double vowels with single
    text = re.sub(r"aa", "a", text)
    text = re.sub(r"ee", "e", text)
    text = re.sub(r"ii", "i", text)
    text = re.sub(r"oo", "o", text)
    text = re.sub(r"uu", "u", text)
    text = re.sub("k", "c", text)
    print(text)
    # Split into words
    return text.split()

def search_word_ids(words):
    """
    Find rows in 'searchnames' where 'names' contain ALL words (AND condition).
    Returns a list of matched IDs.
    """
    and_conditions = [{"names": {"$regex": word, "$options": "i"}} for word in words]
    query = {"$and": and_conditions}

    found_ids = set()
    matches = searchnames_col.find(query)
    for m in matches:
        if "id" in m:
            found_ids.add(m["id"])
    return list(found_ids)

import json

def fetch_related_objects(ids):
    final_ids = set()   # store all related product IDs
    final_set = set()   # store final unique JSON objects

    # --------- First Pass: Collect IDs ----------
    for _id in ids:
        if _id.startswith("p"):
            # Direct product ID
            final_ids.add(_id)

        elif _id.startswith("bp") and "-" in _id:
            # For byproduct-dsp type, get products linked via dspid
            prod_matches = products_col.find({"dspid": _id}, {"id": 1})
            for prod in prod_matches:
                final_ids.add(prod["id"])
            

        elif _id.startswith("bp"):
            # Normal byproduct: find related downstream products, then products
            dsp_matches = downstreamproducts_col.find({"bpid": _id}, {"id": 1})
            for dsp in dsp_matches:
                prod_matches = products_col.find({"dspid": dsp["id"]}, {"id": 1})
                for prod in prod_matches:
                    final_ids.add(prod["id"])
    print(final_ids)
    # --------- Second Pass: Fetch Objects ----------
    for fid in final_ids:
        if fid.startswith("p"):
            obj = products_col.find_one({"id": fid})
        elif fid.startswith("bp") and "-dsp" in fid:
            obj = downstreamproducts_col.find_one({"id": fid})
        elif fid.startswith("bp"):
            obj = byproducts_col.find_one({"id": fid})
        else:
            obj = None

        if obj:
            final_set.add(json.dumps(obj, default=str))

    # --------- Convert back to list of dicts ----------
    final_list = [json.loads(item) for item in final_set]
    return final_list

# def fetch_related_objects(ids):
#     final_set = set()

#     for _id in ids:

#         if _id.startswith("bp") and "-dsp" in _id:  # byproduct + downstream id
#             dsp_obj = downstreamproducts_col.find_one({"id": _id})
#             if dsp_obj:wht
#                 final_set.add(json.dumps(dsp_obj, default=str))
#                 prod_matches = list(products_col.find({"dspid": _id}))
#                 for prod in prod_matches:
#                     final_set.add(json.dumps(prod, default=str))
#         elif _id.startswith("bp"):
#             bp_obj = byproducts_col.find_one({"id": _id})
#             if bp_obj:
#                 final_set.add(json.dumps(bp_obj, default=str))

#                 dsp_matches = list(downstreamproducts_col.find({"bpid": _id}))
#                 for dsp in dsp_matches:
#                     final_set.add(json.dumps(dsp, default=str))

#                     prod_matches = list(products_col.find({"dspid": dsp["id"]}))
#                     for prod in prod_matches:
#                         final_set.add(json.dumps(prod, default=str))

#         elif _id.startswith("p"):  # product id
#             prod_obj = products_col.find_one({"id": _id})
#             if prod_obj:
#                 final_set.add(json.dumps(prod_obj, default=str))

#     final_list = [json.loads(item) for item in final_set]
#     return final_list

def searchuse(x):
    words = normalize_text(x)
    matched_ids = search_word_ids(words)
    results = fetch_related_objects(matched_ids)
    
    return results

if __name__ == "__main__":
    searchuse("Aakulu")
