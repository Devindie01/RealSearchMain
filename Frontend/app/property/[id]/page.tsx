"use client"

import { useParams, useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { MapPin, Bed, Bath, Square, Calendar, Phone, Mail } from "lucide-react"
import Link from "next/link"
import { Header } from "@/components/header"

// Mock property data (same as in the main page)
const mockProperties = [
  {
    id: 1,
    title: "Modern Downtown Loft",
    location: "Colombo 03, Sri Lanka",
    price: 45000000,
    bedrooms: 2,
    bathrooms: 2,
    sqft: 1200,
    image: "/modern-loft-interior.jpg",
    type: "Apartment",
    description: "Stunning modern loft with city views, hardwood floors, and premium finishes",
    fullDescription:
      "This exceptional modern loft offers the perfect blend of urban sophistication and comfortable living. Located in the heart of Colombo, this property features floor-to-ceiling windows that flood the space with natural light and provide breathtaking city views. The open-concept layout includes a gourmet kitchen with stainless steel appliances, quartz countertops, and custom cabinetry. Beautiful hardwood floors throughout, high ceilings, and premium finishes make this loft truly special.",
    yearBuilt: 2020,
    parking: "2 spaces",
    heating: "Central heating",
    cooling: "Central A/C",
    lat: 6.9271,
    lng: 79.8612,
    features: [
      "Floor-to-ceiling windows",
      "Hardwood floors",
      "Stainless steel appliances",
      "Quartz countertops",
      "In-unit washer/dryer",
      "Walk-in closets",
      "Balcony",
      "Gym access",
      "24/7 security",
    ],
  },
  {
    id: 2,
    title: "Suburban Family Home",
    location: "Bellevue, WA",
    price: 1200000,
    bedrooms: 4,
    bathrooms: 3,
    sqft: 2800,
    image: "/placeholder.svg?key=ytxto",
    type: "House",
    description: "Spacious family home with large backyard, updated kitchen, and excellent schools nearby",
    fullDescription:
      "Welcome to this beautiful family home in one of Bellevue's most sought-after neighborhoods. This spacious 4-bedroom, 3-bathroom house offers everything a growing family needs. The recently updated kitchen features modern appliances, granite countertops, and plenty of storage. The large backyard is perfect for children to play and for hosting summer barbecues. Located near top-rated schools and parks, this home combines comfort with convenience.",
    yearBuilt: 2015,
    parking: "2-car garage",
    heating: "Gas furnace",
    cooling: "Central A/C",
    features: [
      "Updated kitchen",
      "Large backyard",
      "Master suite with ensuite",
      "Hardwood and carpet flooring",
      "Two-car garage",
      "Laundry room",
      "Fireplace",
      "Near excellent schools",
      "Quiet neighborhood",
    ],
  },
  {
    id: 3,
    title: "Waterfront Condo",
    location: "Lake Union, Seattle",
    price: 950000,
    bedrooms: 2,
    bathrooms: 2,
    sqft: 1400,
    image: "/placeholder.svg?key=uu3qp",
    type: "Condo",
    description: "Luxurious waterfront living with panoramic lake views and resort-style amenities",
    fullDescription:
      "Experience luxury waterfront living in this stunning Lake Union condo. Wake up to panoramic lake views from your private balcony and enjoy resort-style amenities including a rooftop deck, fitness center, and concierge service. The open floor plan features high-end finishes, a chef's kitchen with premium appliances, and spa-like bathrooms. This is urban living at its finest, with easy access to restaurants, shops, and the vibrant Seattle waterfront.",
    yearBuilt: 2018,
    parking: "1 space + storage",
    heating: "Radiant floor heating",
    cooling: "Central A/C",
    features: [
      "Panoramic lake views",
      "Private balcony",
      "Chef's kitchen",
      "Spa-like bathrooms",
      "Rooftop deck",
      "Fitness center",
      "Concierge service",
      "Secure parking",
      "Pet-friendly",
    ],
  },
  {
    id: 4,
    title: "Cozy Craftsman Bungalow",
    location: "Capitol Hill, Seattle",
    price: 725000,
    bedrooms: 3,
    bathrooms: 2,
    sqft: 1600,
    image: "/placeholder.svg?key=v1mzz",
    type: "House",
    description: "Charming craftsman with original details, updated systems, and walkable neighborhood",
    fullDescription:
      "Fall in love with this charming craftsman bungalow in the heart of Capitol Hill. This home beautifully preserves its original character with built-in cabinetry, crown molding, and hardwood floors, while offering modern updates including a renovated kitchen and updated electrical and plumbing systems. The covered front porch is perfect for morning coffee, and the fenced backyard provides a private retreat. Walk to cafes, restaurants, and parks in one of Seattle's most vibrant neighborhoods.",
    yearBuilt: 1925,
    parking: "Street parking",
    heating: "Gas furnace",
    cooling: "Window units",
    features: [
      "Original craftsman details",
      "Renovated kitchen",
      "Hardwood floors",
      "Built-in cabinetry",
      "Covered front porch",
      "Fenced backyard",
      "Updated systems",
      "Walkable neighborhood",
      "Near public transit",
    ],
  },
  {
    id: 5,
    title: "Luxury Penthouse",
    location: "Downtown, Seattle",
    price: 2500000,
    bedrooms: 3,
    bathrooms: 3,
    sqft: 3200,
    image: "/placeholder.svg?key=73kd4",
    type: "Penthouse",
    description: "Exclusive penthouse with private rooftop terrace, floor-to-ceiling windows, and premium appliances",
    fullDescription:
      "This exclusive penthouse represents the pinnacle of luxury urban living. Occupying the entire top floor, this residence features soaring ceilings, floor-to-ceiling windows, and a private rooftop terrace with 360-degree city views. The gourmet kitchen is equipped with top-of-the-line appliances, and the master suite includes a spa-like bathroom and expansive walk-in closet. Smart home technology, custom lighting, and premium finishes throughout make this penthouse truly exceptional.",
    yearBuilt: 2021,
    parking: "3 spaces",
    heating: "Radiant floor heating",
    cooling: "Central A/C",
    features: [
      "Private rooftop terrace",
      "360-degree city views",
      "Smart home technology",
      "Gourmet kitchen",
      "Spa-like master bath",
      "Custom lighting",
      "Wine storage",
      "Concierge service",
      "Private elevator access",
    ],
  },
  {
    id: 6,
    title: "Garden View Townhouse",
    location: "Fremont, Seattle",
    price: 680000,
    bedrooms: 3,
    bathrooms: 2.5,
    sqft: 1800,
    image: "/placeholder.svg?key=1emu3",
    type: "Townhouse",
    description: "Beautiful townhouse with private garden, modern kitchen, and close to parks",
    fullDescription:
      "This beautiful townhouse in Fremont offers the perfect combination of indoor and outdoor living. The main level features an open-concept living and dining area that flows seamlessly to a private garden patio. The modern kitchen includes stainless steel appliances and plenty of counter space. Upstairs, you'll find three bedrooms including a master suite with ensuite bathroom. The location is ideal, with easy access to parks, the Burke-Gilman Trail, and Fremont's eclectic shops and restaurants.",
    yearBuilt: 2017,
    parking: "1-car garage",
    heating: "Gas furnace",
    cooling: "Central A/C",
    features: [
      "Private garden patio",
      "Modern kitchen",
      "Open-concept living",
      "Master suite",
      "One-car garage",
      "Near Burke-Gilman Trail",
      "Close to parks",
      "Fremont neighborhood",
      "Low HOA fees",
    ],
  },
]

export default function PropertyDetailPage() {
  const params = useParams()
  const router = useRouter()
  const propertyId = Number.parseInt(params.id as string)

  const property = mockProperties.find((p) => p.id === propertyId)

  if (!property) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="max-w-md w-full text-center">
          <CardContent className="pt-12 pb-12">
            <h2 className="text-2xl font-bold mb-4">Property Not Found</h2>
            <p className="text-muted-foreground mb-6">The property you're looking for doesn't exist.</p>
            <Link href="/">
              <Button>Back to Search</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <Header />

      {/* Hero Image */}
      <div className="w-full aspect-[21/9] relative overflow-hidden bg-muted">
        <img src={property.image || "/placeholder.svg"} alt={property.title} className="object-cover w-full h-full" />
        <Badge className="absolute top-6 right-6 text-base px-4 py-2">{property.type}</Badge>
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Title and Price */}
            <div>
              <h1 className="text-4xl font-bold mb-4 text-balance">{property.title}</h1>
              <div className="flex items-center text-muted-foreground mb-4">
                <MapPin className="h-5 w-5 mr-2" />
                <span className="text-lg">{property.location}</span>
              </div>
              <p className="text-4xl font-bold text-primary">{property.price.toLocaleString()} LKR</p>
            </div>

            <Separator />

            {/* Key Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <div className="flex flex-col items-center p-4 bg-muted rounded-lg">
                <Bed className="h-8 w-8 mb-2 text-primary" />
                <span className="text-2xl font-bold">{property.bedrooms}</span>
                <span className="text-sm text-muted-foreground">Bedrooms</span>
              </div>
              <div className="flex flex-col items-center p-4 bg-muted rounded-lg">
                <Bath className="h-8 w-8 mb-2 text-primary" />
                <span className="text-2xl font-bold">{property.bathrooms}</span>
                <span className="text-sm text-muted-foreground">Bathrooms</span>
              </div>
              <div className="flex flex-col items-center p-4 bg-muted rounded-lg">
                <Square className="h-8 w-8 mb-2 text-primary" />
                <span className="text-2xl font-bold">{property.sqft}</span>
                <span className="text-sm text-muted-foreground">Sq Ft</span>
              </div>
              <div className="flex flex-col items-center p-4 bg-muted rounded-lg">
                <Calendar className="h-8 w-8 mb-2 text-primary" />
                <span className="text-2xl font-bold">{property.yearBuilt}</span>
                <span className="text-sm text-muted-foreground">Year Built</span>
              </div>
            </div>

            <Separator />

            {/* Location */}
            <div>
              <h2 className="text-2xl font-bold mb-4">Location</h2>
              <div className="aspect-video rounded-lg overflow-hidden border">
                <iframe
                  width="100%"
                  height="100%"
                  frameBorder="0"
                  style={{ border: 0 }}
                  src={`https://www.google.com/maps/embed/v1/place?key=AIzaSyBFw0Qbyq9zTFTd-tUY6dZWTgaQzuU17R8&q=${property.lat},${property.lng}&zoom=15`}
                  allowFullScreen
                />
              </div>
            </div>

            <Separator />

            {/* Description */}
            <div>
              <h2 className="text-2xl font-bold mb-4">About This Property</h2>
              <p className="text-muted-foreground leading-relaxed">{property.fullDescription}</p>
            </div>

            <Separator />

            {/* Features */}
            <div>
              <h2 className="text-2xl font-bold mb-4">Features & Amenities</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {property.features.map((feature, index) => (
                  <div key={index} className="flex items-center gap-2">
                    <div className="h-2 w-2 rounded-full bg-primary" />
                    <span className="text-muted-foreground">{feature}</span>
                  </div>
                ))}
              </div>
            </div>

            <Separator />

            {/* Additional Details */}
            <div>
              <h2 className="text-2xl font-bold mb-4">Property Details</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex justify-between p-3 bg-muted rounded-lg">
                  <span className="text-muted-foreground">Parking</span>
                  <span className="font-semibold">{property.parking}</span>
                </div>
                <div className="flex justify-between p-3 bg-muted rounded-lg">
                  <span className="text-muted-foreground">Heating</span>
                  <span className="font-semibold">{property.heating}</span>
                </div>
                <div className="flex justify-between p-3 bg-muted rounded-lg">
                  <span className="text-muted-foreground">Cooling</span>
                  <span className="font-semibold">{property.cooling}</span>
                </div>
                <div className="flex justify-between p-3 bg-muted rounded-lg">
                  <span className="text-muted-foreground">Year Built</span>
                  <span className="font-semibold">{property.yearBuilt}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <Card className="sticky top-24">
              <CardContent className="p-6 space-y-6">
                <div>
                  <h3 className="text-xl font-bold mb-2">Interested in this property?</h3>
                  <p className="text-sm text-muted-foreground">
                    Contact us to schedule a viewing or get more information
                  </p>
                </div>

                <Separator />

                <div className="space-y-3">
                  <Button className="w-full" size="lg">
                    <Phone className="h-5 w-5 mr-2" />
                    Call Agent
                  </Button>
                  <Button variant="outline" className="w-full bg-transparent" size="lg">
                    <Mail className="h-5 w-5 mr-2" />
                    Send Message
                  </Button>
                </div>

                <Separator />

                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Property ID</span>
                    <span className="font-semibold">#{property.id.toString().padStart(6, "0")}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Listed</span>
                    <span className="font-semibold">2 weeks ago</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Views</span>
                    <span className="font-semibold">1,234</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
