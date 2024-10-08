from app import app
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer 

# Route to retrieve a list of similar images based on text input, each with a score
@app.route("/api/search/text=<search_text>", methods=["GET"])
def get_image(search_text):
    mogodb_uri = "mongodb://localhost:32768/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.1"
    client = MongoClient(mogodb_uri)

    db_name = "image_search_demo"
    db = client.get_database(db_name)

    image_collection_name = "images"
    collection = db.get_collection(image_collection_name)

    model = SentenceTransformer("clip-ViT-L-14")
    embedding = model.encode(search_text)
    cursor = collection.aggregate(
        [
            {
                "$vectorSearch": {
                    "index": "default",
                    "path": "embedding",
                    "queryVector": embedding.tolist(),
                    "numCandidates": 100,
                    "limit": 9,
                }
            },
            {"$project": {"_id": 1, "score": {"$meta": "vectorSearchScore"}}},
        ]
    )

    cursor_list = list(cursor)
    image_list = [cursor["_id"] for cursor in cursor_list]
    image_score = [cursor["score"] for cursor in cursor_list]
    
    return {
        "image": image_list,
        "score": image_score,
    }