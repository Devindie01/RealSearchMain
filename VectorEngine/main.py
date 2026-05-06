from app.storage.connections import get_client
from tests.pipeline import run_pipeline_test

queries = [
    "Buy a House in Colombo",
    "I'm looking for a 2 bedroom apartment for rent in Colombo 03 below 150,000 LKR",
    "Hello everyone! I’m looking for a house to buy or land with electricity and water already connected. 📍 Preferred location: Habaraduwa area ➡️ I will also consider properties from Talpe to Ahangama Requirements: • 4–5 bedrooms • 4–5 bathrooms • Maximum 2.5 km from the beach • Clear legal status – I will verify the Title Report with my lawyer.",
    "Looking for a 3+ bedroom villa for long term lease. In Thalpe",
    # "Hi, Im looking for a house to rent in Hiriketya from 1.11.25-1.12.25. I would like a house with a good kitchen, an outside place to sit and a workingplace.",
    # "Looking for a House for Rent 2 Bedrooms Kitchen Living Room Washroom Parking Preferred Areas: Moratuwa, Panadura, Piliyandala 💰 Budget: Rs. 30,000 – 40,000/-",
    # "We are looking for a house to rent in Ahangama starting from 21 February for a duration of 2–3 months. The house should have 3 bedrooms and 2 bathrooms, along with a fully equipped kitchen. Air conditioning is required in all bedrooms, and the property should include a living room with a sofa. Ideally, it should also have a small garden and a terrace space. Our budget is up to 350,000 LKR per month. We are a quiet family and will take good care of the house.",
    # "We are looking for a 3+ bedroom boutique villa for a long-term lease. The preferred location is between Galle Fort and Thalpe. The property should be suitable for long-term living and offer a comfortable and private environment.",
    # "I am looking for a house to rent in Hiriketiya from 1 November 2025 to 1 December 2025. The house should include a good kitchen, an outdoor seating area, and a workspace suitable for working remotely.",
    # "I am looking for a house for rent with 2 bedrooms, a kitchen, living room, washroom, and parking space. Preferred locations are Moratuwa, Panadura, or Piliyandala. My budget is between Rs. 30,000 and 40,000 per month.",
    # "land for sale in Colombo with good access to public transport",
    # "villa in Galle with pool and sea view for sale",
    # "affordable house in Kandy with 3 bedrooms and garden for rent",
]

with get_client() as client:
    for q in queries:
        try:
            run_pipeline_test(q, client)
        except Exception as e:
            print(f"Error processing '{q}': {e}")
