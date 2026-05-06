/**
 * mockData.ts
 *
 * Drop-in mock data for testing the frontend without a running backend.
 * Swap out by setting NEXT_PUBLIC_API_URL to your real backend URL.
 *
 * Images use Unsplash source URLs — no API key needed, loads instantly.
 * Coordinates are real Sri Lankan locations.
 */

import type { PropertySummary } from "./page"

// ---------------------------------------------------------------------------
// Summary list  (used by /featured and /search)
// ---------------------------------------------------------------------------

export const MOCK_PROPERTIES: PropertySummary[] = [
  {
    id: 1,
    title: "Modern Penthouse with Ocean View",
    location: "Colombo 03, Western Province",
    price: 95000000,
    bedrooms: 3,
    bathrooms: 3,
    sqft: 2400,
    type: "Apartment",
    image: "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&q=80",
    insight: "Premium Colombo 3 location commands 18% higher resale value than nearby districts. High rental yield potential.",
    lat: 6.9100,
    lng: 79.8550,
  },
  {
    id: 2,
    title: "Spacious Family Villa in Battaramulla",
    location: "Battaramulla, Western Province",
    price: 68000000,
    bedrooms: 4,
    bathrooms: 3,
    sqft: 3100,
    type: "Villa",
    image: "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80",
    insight: "Rapidly growing suburb with new highway access. Strong school catchment area drives family demand.",
    lat: 6.9022,
    lng: 79.9147,
  },
  {
    id: 3,
    title: "Colonial Heritage Home",
    location: "Kandy, Central Province",
    price: 42000000,
    bedrooms: 5,
    bathrooms: 4,
    sqft: 4200,
    type: "House",
    image: "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80",
    insight: "Heritage designation protects architectural value. Tourist rental potential in UNESCO buffer zone.",
    lat: 7.2906,
    lng: 80.6337,
  },
  {
    id: 4,
    title: "Beachfront Boutique Villa",
    location: "Mirissa, Southern Province",
    price: 78000000,
    bedrooms: 3,
    bathrooms: 3,
    sqft: 2800,
    type: "Villa",
    image: "https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?w=800&q=80",
    insight: "Direct beach access is rare in Mirissa. Comparable Airbnb listings earn LKR 80k+ per night in peak season.",
    lat: 5.9483,
    lng: 80.4716,
  },
  {
    id: 5,
    title: "City Centre Studio Apartment",
    location: "Colombo 01, Western Province",
    price: 18500000,
    bedrooms: 1,
    bathrooms: 1,
    sqft: 620,
    type: "Apartment",
    image: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&q=80",
    insight: "Walking distance to Fort business district. Ideal for young professionals — rental vacancy under 3%.",
    lat: 6.9344,
    lng: 79.8428,
  },
  {
    id: 6,
    title: "Highland Tea Country Estate",
    location: "Nuwara Eliya, Central Province",
    price: 135000000,
    bedrooms: 6,
    bathrooms: 5,
    sqft: 6500,
    type: "House",
    image: "https://images.unsplash.com/photo-1464146072230-91cabc968266?w=800&q=80",
    insight: "Working tea garden included. Eco-tourism and boutique hotel conversion potential with existing planning consent.",
    lat: 6.9497,
    lng: 80.7891,
  },
  {
    id: 7,
    title: "Luxury Apartment — World Trade Centre Views",
    location: "Colombo 02, Western Province",
    price: 55000000,
    bedrooms: 2,
    bathrooms: 2,
    sqft: 1450,
    type: "Apartment",
    image: "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&q=80",
    insight: "Floor-to-ceiling glass with WTC skyline views. Building has 5-star hotel management and concierge.",
    lat: 6.9214,
    lng: 79.8452,
  },
  {
    id: 8,
    title: "Commercial Land — High Street Frontage",
    location: "Negombo, Western Province",
    price: 29000000,
    bedrooms: 0,
    bathrooms: 0,
    sqft: 5400,
    type: "Land",
    image: "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800&q=80",
    insight: "15 perches with 60ft road frontage on the main Negombo high street. Zoned for commercial development.",
    lat: 7.2111,
    lng: 79.8386,
  },
  {
    id: 9,
    title: "Serene River-View Bungalow",
    location: "Galle, Southern Province",
    price: 38500000,
    bedrooms: 3,
    bathrooms: 2,
    sqft: 1900,
    type: "House",
    image: "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800&q=80",
    insight: "Galle Fort buffer zone location. Expat demand keeps vacancy extremely low year-round.",
    lat: 6.0535,
    lng: 80.2210,
  },
  {
    id: 10,
    title: "New-Build Semi-Detached",
    location: "Malabe, Western Province",
    price: 32000000,
    bedrooms: 3,
    bathrooms: 2,
    sqft: 1750,
    type: "House",
    image: "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800&q=80",
    insight: "Adjacent to SLIIT university campus — strong student and academic rental market.",
    lat: 6.9063,
    lng: 79.9653,
  },
  {
    id: 11,
    title: "Investor-Grade Commercial Unit",
    location: "Rajagiriya, Western Province",
    price: 48000000,
    bedrooms: 0,
    bathrooms: 2,
    sqft: 2200,
    type: "Commercial",
    image: "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&q=80",
    insight: "Ground-floor retail space on a 50,000 VPD arterial road. Current tenant on 5-year NNN lease.",
    lat: 6.9055,
    lng: 79.8988,
  },
  {
    id: 12,
    title: "Eco-Friendly Jungle Retreat",
    location: "Sigiriya, Central Province",
    price: 62000000,
    bedrooms: 4,
    bathrooms: 4,
    sqft: 3600,
    type: "Villa",
    image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80",
    insight: "3km from Sigiriya Rock — Sri Lanka's #1 tourist destination. Boutique glamping conversion ready.",
    lat: 7.9570,
    lng: 80.7603,
  },
]

// ---------------------------------------------------------------------------
// Full detail objects  (used by /properties/:id)
// ---------------------------------------------------------------------------

export const MOCK_PROPERTY_DETAILS: Record<number, object> = {
  1: {
    ...MOCK_PROPERTIES[0],
    images: [
      "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=1200&q=85",
      "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=1200&q=85",
      "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=1200&q=85",
      "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=1200&q=85",
    ],
    fullDescription:
      "Perched on the 28th floor with uninterrupted views of the Indian Ocean and Colombo skyline, this contemporary penthouse sets a new standard for luxury living. The expansive open-plan living area flows onto a wraparound terrace, creating an indoor-outdoor lifestyle rarely found in the city. The chef's kitchen features Gaggenau appliances, Italian marble countertops, and a butler's pantry. All three bedrooms are en-suite with walk-in wardrobes, while the master suite includes a private study and spa bathroom with a freestanding soaking tub.",
    features: [
      "Wraparound terrace with ocean views",
      "Gaggenau kitchen appliances",
      "Italian marble throughout",
      "Smart home automation system",
      "Private lift lobby",
      "24/7 concierge and security",
      "Infinity-edge rooftop pool access",
      "Two dedicated parking bays",
      "Generator backup",
      "Solar water heating",
    ],
    yearBuilt: 2022,
    parking: "2 dedicated bays",
    heating: "N/A",
    cooling: "Central VRF A/C",
  },
  2: {
    ...MOCK_PROPERTIES[1],
    images: [
      "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1200&q=85",
      "https://images.unsplash.com/photo-1560184897-ae75f418493e?w=1200&q=85",
      "https://images.unsplash.com/photo-1584738766473-61c083514bf4?w=1200&q=85",
    ],
    fullDescription:
      "A beautifully designed family villa on a quiet lane in Battaramulla, one of Colombo's most sought-after residential suburbs. Set on 15 perches, the property features a large landscaped garden with a 40ft private pool, a covered entertaining pavilion, and a children's play area. Inside, the house is bright and airy with high ceilings, imported porcelain tile floors, and a layout that keeps family living and formal reception areas thoughtfully separate.",
    features: [
      "40ft private swimming pool",
      "Landscaped garden — 15 perches",
      "Covered entertaining pavilion",
      "Separate maid's quarters",
      "Double garage",
      "Backup generator",
      "Bore well and municipal water supply",
      "CCTV and alarm system",
      "Study / home office",
    ],
    yearBuilt: 2018,
    parking: "Double garage + 2 open bays",
    heating: "N/A",
    cooling: "Split A/C in all rooms",
  },
  3: {
    ...MOCK_PROPERTIES[2],
    images: [
      "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1200&q=85",
      "https://images.unsplash.com/photo-1464146072230-91cabc968266?w=1200&q=85",
      "https://images.unsplash.com/photo-1449844908441-8829872d2607?w=1200&q=85",
    ],
    fullDescription:
      "A rare opportunity to own a significant colonial-era estate in Kandy, lovingly restored to preserve its original architectural character while introducing modern comforts. The property features original hardwood floors, ornate plasterwork ceilings, and deep verandas overlooking a mature tropical garden. Five bedrooms have been individually styled to reflect different periods of the home's history, making this equally suited as a private residence or boutique guesthouse.",
    features: [
      "Original hardwood floors and ceilings",
      "Period fireplaces in main rooms",
      "Deep wraparound veranda",
      "Mature tropical garden — 30 perches",
      "Separate guest cottage",
      "Heritage council registered",
      "Recently rewired and replumbed",
      "Three-car motor house",
    ],
    yearBuilt: 1924,
    parking: "Motor house (3 cars)",
    heating: "Fireplaces",
    cooling: "Ceiling fans + natural ventilation",
  },
  4: {
    ...MOCK_PROPERTIES[3],
    images: [
      "https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?w=1200&q=85",
      "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=1200&q=85",
      "https://images.unsplash.com/photo-1502005229762-cf1b2da7c5d6?w=1200&q=85",
    ],
    fullDescription:
      "Step directly from your garden onto one of Mirissa's quietest stretches of golden sand. This three-bedroom beachfront villa was custom-built for both high-end rental income and private enjoyment. The architecture draws on Balinese and Sri Lankan vernacular influences — open-sided living pavilion, natural timber and stone, cathedral ceiling in the main sala — while delivering all the modern amenities guests expect.",
    features: [
      "Direct beach access — zero road crossing",
      "Private infinity pool",
      "Open-sided living sala",
      "Fully equipped Bali-style kitchen",
      "All bedrooms with sea view",
      "Outdoor rain shower",
      "Established rental history (95% peak occupancy)",
      "Security guard accommodation",
    ],
    yearBuilt: 2019,
    parking: "2 open bays",
    heating: "N/A",
    cooling: "Split A/C + ceiling fans",
  },
}

// ---------------------------------------------------------------------------
// Mock explain stream  (simulates SSE text arriving in chunks)
// ---------------------------------------------------------------------------

/**
 * Call this from the mock explain endpoint to simulate streaming.
 * Returns a ReadableStream of text chunks with realistic delays.
 */
export const MOCK_EXPLANATIONS: Record<number, string> = {
  1: "This Colombo 03 penthouse sits in Sri Lanka's most liquid real estate market. The beachfront corridor between Kollupitiya and Bambalapitiya has seen consistent 12–15% YoY appreciation over the past five years, driven by limited new supply and strong expatriate and corporate tenant demand. At LKR 95M the per-sqft price of ~39,600 is below comparable new launches in the same precinct, suggesting room for value growth. The ocean-view premium typically adds 20–30% to rental yields versus interior units in the same building. Recommend prioritising this if short-term rental income is a goal — platforms like Airbnb show Colombo 3 oceanview properties commanding LKR 40,000–65,000 per night.",
  2: "Battaramulla's residential market has undergone structural repricing since the outer ring road completion in 2021, cutting commute times to the Fort CBD to under 25 minutes. Family villa stock here is absorbed quickly — average days on market is 18, well below the Colombo district average of 41. The 15-perch plot is the key asset: land in this pocket rarely comes to market below LKR 5M per perch, implying meaningful land value alone of LKR 75M+. The asking price of LKR 68M includes the built structure, making this competitively priced. The school catchment (within 1km of three international schools) sustains strong tenant demand from diplomatic and corporate families.",
  3: "Heritage properties in Kandy represent a micro-market with almost no comparables — supply is structurally constrained and authenticity commands a premium that only increases over time. The Heritage Council registration acts as a double-edged sword: restrictions on exterior alteration protect value but limit redevelopment. The 30-perch garden is the standout asset; Kandy land of this quality rarely transacts publicly. At LKR 42M for a property of this scale and history, the pricing reflects motivated seller circumstances rather than fair market value. Boutique hotel conversion with 8–10 rooms could generate LKR 3–4M per month at current Kandy tourism occupancy rates.",
  4: "Mirissa beachfront is arguably Sri Lanka's most internationalised short-term rental market, with Airbnb Superhost properties generating USD 800–1,200 per night in peak whale-watching season (November–April). The established rental history attached to this villa de-risks the investment materially — you are acquiring a proven income stream, not a speculative one. At LKR 78M (~USD 240K at current rates), the yield on peak-season occupancy alone covers the acquisition cost in under 8 years without factoring appreciation. Direct beach access without a road crossing is genuinely rare in Mirissa; most beachfront properties require crossing the coastal road.",
}