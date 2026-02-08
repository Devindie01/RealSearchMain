"use client"

import { useEffect, useState } from "react"
import { Search, MapPin, Bed, Bath, Square, Lightbulb } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import Link from "next/link"
import { Header } from "@/components/header"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { set } from "date-fns"

// Mock property data with coordinates for map
// const mockProperties = [
//   {
//     id: 1,
//     title: "Modern Downtown Loft",
//     location: "Colombo 03, Sri Lanka",
//     price: 45000000,
//     bedrooms: 2,
//     bathrooms: 2,
//     sqft: 1200,
//     image: "/modern-loft-interior.jpg",
//     type: "Apartment",
//     description: "Stunning modern loft with city views, hardwood floors, and premium finishes",
//     lat: 6.9271,
//     lng: 79.8612,
//     insight: "Prime business district location with high rental yields",
//   },
//   {
//     id: 2,
//     title: "Suburban Family Home",
//     location: "Nugegoda, Sri Lanka",
//     price: 65000000,
//     bedrooms: 4,
//     bathrooms: 3,
//     sqft: 2800,
//     image: "/suburban-family-house.png",
//     type: "House",
//     description: "Spacious family home with large backyard, updated kitchen, and excellent schools nearby",
//     lat: 6.8649,
//     lng: 79.8997,
//     insight: null,
//   },
//   {
//     id: 3,
//     title: "Waterfront Condo",
//     location: "Mount Lavinia, Sri Lanka",
//     price: 52000000,
//     bedrooms: 2,
//     bathrooms: 2,
//     sqft: 1400,
//     image: "/waterfront-condo-view.png",
//     type: "Apartment",
//     description: "Luxurious waterfront living with panoramic ocean views and resort-style amenities",
//     lat: 6.8382,
//     lng: 79.8636,
//     insight: null,
//   },
//   {
//     id: 4,
//     title: "Cozy Colonial Bungalow",
//     location: "Kandy, Sri Lanka",
//     price: 38000000,
//     bedrooms: 3,
//     bathrooms: 2,
//     sqft: 1600,
//     image: "/craftsman-bungalow-exterior.png",
//     type: "House",
//     description: "Charming colonial home with original details, updated systems, and walkable neighborhood",
//     lat: 7.2906,
//     lng: 80.6337,
//     insight: null,
//   },
//   {
//     id: 5,
//     title: "Luxury Penthouse",
//     location: "Colombo 07, Sri Lanka",
//     price: 135000000,
//     bedrooms: 3,
//     bathrooms: 3,
//     sqft: 3200,
//     image: "/luxury-penthouse-interior.png",
//     type: "Apartment",
//     description: "Exclusive penthouse with private rooftop terrace, floor-to-ceiling windows, and premium appliances",
//     lat: 6.9147,
//     lng: 79.8613,
//     insight: "Luxury market leader with strong appreciation potential",
//   },
//   {
//     id: 6,
//     title: "Garden View Townhouse",
//     location: "Dehiwala, Sri Lanka",
//     price: 36000000,
//     bedrooms: 3,
//     bathrooms: 2.5,
//     sqft: 1800,
//     image: "/townhouse-with-garden.png",
//     type: "House",
//     description: "Beautiful townhouse with private garden, modern kitchen, and close to parks",
//     lat: 6.8562,
//     lng: 79.8742,
//     insight: null,
//   },
// ]

export default function PropertySearchPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [location, setLocation] = useState("")
  const [bedrooms, setBedrooms] = useState("")
  const [minPrice, setMinPrice] = useState("")
  const [maxPrice, setMaxPrice] = useState("")
  const [propertyType, setPropertyType] = useState("")
  const [filteredProperties, setFilteredProperties] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 20
  const [totalCount, setTotalCount] = useState(0)
  const [featuredProperties, setFeaturedProperties] = useState([])
  const [isSearchMode, setIsSearchMode] = useState(false)

  useEffect(() => {
  const fetchHomeProperties = async () => {
    try {
      setIsLoading(true);
      const response = await fetch("http://localhost:8000/api/v1/featured");
      const data = await response.json();
      setFeaturedProperties(data.results);
    } catch (error) {
      console.error("Home page fetch error:", error);
    }finally {
      setIsLoading(false);
    }
  };
  fetchHomeProperties();
}, []);

  const handleSearch = async (pageNumber = 1) => {
    setIsLoading(true);
    setCurrentPage(pageNumber);
    setIsSearchMode(true);
    try {
    const params = new URLSearchParams({
      query: searchQuery,
      location: location,
      min_price: minPrice,
      max_price: maxPrice,
      bedrooms: bedrooms,
      type: propertyType !== "any" ? propertyType : "",
      page: pageNumber.toString(),
      limit: itemsPerPage.toString()
    });

    const response = await fetch(`http://localhost:8000/api/v1/search?${params.toString()}`);
    if (!response.ok) throw new Error("Failed to fetch");
    
    const data = await response.json();
    
    // Assuming backend returns { results: [], totalCount: 100 }
    setFilteredProperties(data.results || []);
    setTotalCount(data.totalCount || 0); 
  } catch (error) {
    console.error("Error fetching properties:", error);
    setFilteredProperties([]);
  } finally {
    setIsLoading(false);
  }
};

const handleReset = () => {
  setSearchQuery("")
  setLocation("")
  setBedrooms("")
  setMinPrice("")
  setMaxPrice("")
  setPropertyType("")
  setIsSearchMode(false)
  setCurrentPage(1)
}

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <div className="bg-card border-b">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-5xl mx-auto space-y-6">
            <div className="text-center space-y-2">
              <h2 className="text-4xl font-bold text-balance">Find Your Perfect Home</h2>
              <p className="text-lg text-muted-foreground">Search from thousands of properties</p>
            </div>

            {/* Main Search Bar */}
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                <Input
                  placeholder="Search by keyword, location, or property name..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                  className="pl-10 h-14 text-lg"
                />
              </div>
              <Button onClick={handleSearch} size="lg" className="h-14 px-8">
                Search
              </Button>
            </div>

            {/* Filter Fields */}
            <Card>
              <CardContent className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
                  {/* Location Filter */}
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Location</label>
                    <Input
                      placeholder="e.g., Colombo, Kandy"
                      value={location}
                      onChange={(e) => setLocation(e.target.value)}
                    />
                  </div>

                  {/* Property Type Filter */}
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Property Type</label>
                    <Select value={propertyType} onValueChange={setPropertyType}>
                      <SelectTrigger>
                        <SelectValue placeholder="Any" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="any">Any</SelectItem>
                        <SelectItem value="house">House</SelectItem>
                        <SelectItem value="apartment">Apartment</SelectItem>
                        <SelectItem value="villa">Villa</SelectItem>
                        <SelectItem value="land">Land</SelectItem>
                        <SelectItem value="commercial">Commercial</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                                    {/* Min Price Filter */}
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Min Price</label>
                    <Input
                      type="number"
                      placeholder="0"
                      value={minPrice}
                      onChange={(e) => setMinPrice(e.target.value)}
                    />
                  </div>

                  {/* Max Price Filter */}
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Max Price</label>
                    <Input
                      type="number"
                      placeholder="Any"
                      value={maxPrice}
                      onChange={(e) => setMaxPrice(e.target.value)}
                    />
                  </div>

                  {/* Bedrooms Filter */}
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Bedrooms</label>
                    <Select value={bedrooms} onValueChange={setBedrooms}>
                      <SelectTrigger>
                        <SelectValue placeholder="Any" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="0">Any</SelectItem>
                        <SelectItem value="1">1+</SelectItem>
                        <SelectItem value="2">2+</SelectItem>
                        <SelectItem value="3">3+</SelectItem>
                        <SelectItem value="4">4+</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>


                </div>

                <div className="flex gap-2 mt-4">
                  <Button onClick={handleSearch} className="flex-1">
                    Apply Filters
                  </Button>
                  <Button onClick={handleReset} variant="outline">
                    Reset
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Results Section */}
      <div className="container mx-auto px-4 py-12">
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-2">
            {isSearchMode && isLoading 
              ? "Searching..." 
              : isSearchMode 
                ? `${totalCount} Search Results` 
              : isLoading
                ? "Loading featured properties..."
                : "Featured Properties"
            }
          </h2>
          <p className="text-muted-foreground">
            {isSearchMode ? "Results based on your search" : "Hand-picked properties for you"}
            
          </p>        
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <Card key={i} className="h-[400px] animate-pulse bg-muted/50" />
            ))}
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {(isSearchMode ? filteredProperties : featuredProperties).map((property) => (
                <Link key={property.id} href={`/property/${property.id}`}>
                  <Card className="overflow-hidden hover:shadow-lg transition-shadow cursor-pointer h-full">
                    <div className="aspect-[4/3] relative overflow-hidden">
                      <img
                        src={property.image || "/placeholder.svg"}
                        alt={property.title}
                        className="object-cover w-full h-full hover:scale-105 transition-transform duration-300"
                      />
                      <Badge className="absolute top-4 right-4">{property.type}</Badge>
                      {!isSearchMode && (
                        <Badge variant="secondary" className="absolute top-4 left-4 bg-yellow-500 text-white border-none">
                          Featured
                        </Badge>
                      )}
                      {property.insight && (
                        <TooltipProvider>
                          <Tooltip>
                            <TooltipTrigger asChild onClick={(e) => e.preventDefault()}>
                              <div className="absolute top-4 right-16 bg-primary text-primary-foreground p-2 rounded-full cursor-help">
                                <Lightbulb className="h-4 w-4" />
                              </div>
                            </TooltipTrigger>
                            <TooltipContent side="left" className="max-w-xs">
                              {property.insight}
                            </TooltipContent>
                          </Tooltip>
                        </TooltipProvider>
                      )}
                    </div>
                    <CardContent className="p-6 space-y-4">
                      <div>
                        <h3 className="font-bold text-xl mb-2 line-clamp-1">{property.title}</h3>
                        <div className="flex items-center text-muted-foreground mb-3">
                          <MapPin className="h-4 w-4 mr-1" />
                          <span className="text-sm">{property.location}</span>
                        </div>
                        <p className="text-2xl font-bold text-primary">{property.price.toLocaleString()} LKR</p>
                      </div>

                      <div className="aspect-video rounded-lg overflow-hidden border">
                        <iframe
                          width="100%"
                          height="100%"
                          frameBorder="0"
                          style={{ border: 0 }}
                          src={`https://www.google.com/maps/embed/v1/place?key=AIzaSyBFw0Qbyq9zTFTd-tUY6dZWTgaQzuU17R8&q=${property.lat},${property.lng}&z=15&output=embed`}
                          allowFullScreen
                        />
                      </div>

                      <div className="flex items-center gap-4 text-sm text-muted-foreground border-t pt-4">
                        <div className="flex items-center gap-1">
                          <Bed className="h-4 w-4" />
                          <span>{property.bedrooms} bed</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Bath className="h-4 w-4" />
                          <span>{property.bathrooms} bath</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Square className="h-4 w-4" />
                          <span>{property.sqft} sqft</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              ))}
            </div>

            {isSearchMode && filteredProperties.length === 0 && (
              <div className="text-center py-16">
                <p className="text-xl text-muted-foreground">No properties found matching your search.</p>
                <Button onClick={handleReset} variant="link" className="mt-2">
                   Return to Featured Properties
                </Button>
              </div>
            )}

{/* Pagination Controls */}
            {/* [ADDED]: Check to hide pagination when viewing Featured properties */}
            {isSearchMode && totalCount > itemsPerPage && (
              <div className="flex justify-center items-center gap-4 mt-12 pb-12">
                <Button 
                  variant="outline" 
                  disabled={currentPage === 1 || isLoading}
                  onClick={() => handleSearch(currentPage - 1)}
                >
                  Previous
                </Button>
                <span className="text-sm font-medium">Page {currentPage}</span>
                <Button 
                  variant="outline" 
                  disabled={currentPage * itemsPerPage >= totalCount || isLoading}
                  onClick={() => handleSearch(currentPage + 1)}
                >
                  Next
                </Button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
