class SearchService:
    @staticmethod
    async def search_nlp(query: str, session_id: str):
        # 1. Here you would log the session_id to track behavior
        print(f"Tracking behavior for session: {session_id}")
        
        # 2. Dummy Vector Engine Logic
        # In a real scenario, you'd call: vector_db.search(query)
        dummy_results = [
            {"id": 1, "title": "Luxury Villa", "description": "Near the beach", "price": 500000, "score": 0.98},
            {"id": 2, "title": "Cozy Apartment", "description": "City center", "price": 200000, "score": 0.85}
        ]
        return dummy_results