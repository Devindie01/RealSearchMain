// "use client"

// import { useEffect, useState } from "react"
// import { Search, MapPin, Bed, Bath, Square, Lightbulb } from "lucide-react"
// import { Button } from "@/components/ui/button"
// import { Input } from "@/components/ui/input"
// import { Card, CardContent } from "@/components/ui/card"
// import { Badge } from "@/components/ui/badge"
// import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
// import Link from "next/link"
// import { Header } from "@/components/header"
// import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
// import { set } from "date-fns"

// // Mock property data with coordinates for map
// // const mockProperties = [
// //   {
// //     id: 1,
// //     title: "Modern Downtown Loft",
// //     location: "Colombo 03, Sri Lanka",
// //     price: 45000000,
// //     bedrooms: 2,
// //     bathrooms: 2,
// //     sqft: 1200,
// //     image: "/modern-loft-interior.jpg",
// //     type: "Apartment",
// //     description: "Stunning modern loft with city views, hardwood floors, and premium finishes",
// //     lat: 6.9271,
// //     lng: 79.8612,
// //     insight: "Prime business district location with high rental yields",
// //   },....
// // ]

// export default function PropertySearchPage() {
//   const [searchQuery, setSearchQuery] = useState("")
//   const [location, setLocation] = useState("")
//   const [bedrooms, setBedrooms] = useState("")
//   const [minPrice, setMinPrice] = useState("")
//   const [maxPrice, setMaxPrice] = useState("")
//   const [propertyType, setPropertyType] = useState("")
//   const [filteredProperties, setFilteredProperties] = useState([])
//   const [isLoading, setIsLoading] = useState(true)
//   const [currentPage, setCurrentPage] = useState(1)
//   const itemsPerPage = 20
//   const [totalCount, setTotalCount] = useState(0)
//   const [featuredProperties, setFeaturedProperties] = useState([])
//   const [isSearchMode, setIsSearchMode] = useState(false)

//   useEffect(() => {
//     const fetchHomeProperties = async () => {
//       try {
//         setIsLoading(true);
//         const response = await fetch("http://localhost:8000/api/v1/featured");
//         const data = await response.json();
//         console.log("Featured properties data:", data);
//         setFeaturedProperties(data.results || []);
//         setTotalCount(data.totalCount || 0);
//       } catch (error) {
//         console.error("Home page fetch error:", error);
//       } finally {
//         setIsLoading(false);
//       }
//     };
//     fetchHomeProperties();
//   }, []);

//   const handleSearch = async (pageNumber = 1) => {
//     setIsLoading(true);
//     setCurrentPage(pageNumber);
//     setIsSearchMode(true);
//     try {
//       const params = new URLSearchParams({
//         query: searchQuery,
//         location: location,
//         min_price: minPrice,
//         max_price: maxPrice,
//         bedrooms: bedrooms,
//         type: propertyType !== "any" ? propertyType : "",
//         page: pageNumber.toString(),
//         limit: itemsPerPage.toString()
//       });

//       const response = await fetch("http://localhost:8000/api/v1/search", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({
//           query: searchQuery,
//           location: location,
//           min_price: minPrice ? parseFloat(minPrice) : null,
//           max_price: maxPrice ? parseFloat(maxPrice) : null,
//           property_type: propertyType !== "any" ? propertyType : null,
//           no_bedrooms: bedrooms && bedrooms !== "0" ? parseInt(bedrooms) : null,
//           // page: pageNumber, // SearchRequest model might not have page/limit yet, check backend model
//           // limit: itemsPerPage
//         }),
//       });
//       if (!response.ok) throw new Error("Failed to fetch");

//       const data = await response.json();

//       // Assuming backend returns { results: [], totalCount: 100 }
//       setFilteredProperties(data.results || []);
//       setTotalCount(data.totalCount || 0);
//     } catch (error) {
//       console.error("Error fetching properties:", error);
//       setFilteredProperties([]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleReset = () => {
//     setSearchQuery("")
//     setLocation("")
//     setBedrooms("")
//     setMinPrice("")
//     setMaxPrice("")
//     setPropertyType("")
//     setIsSearchMode(false)
//     setCurrentPage(1)
//   }

//   return (
//     <div className="min-h-screen bg-background">
//       <Header />

//       <div className="bg-card border-b">
//         <div className="container mx-auto px-4 py-8">
//           <div className="max-w-5xl mx-auto space-y-6">
//             <div className="text-center space-y-2">
//               <h2 className="text-4xl font-bold text-balance">Find Your Perfect Home</h2>
//               <p className="text-lg text-muted-foreground">Search from thousands of properties</p>
//             </div>

//             {/* Main Search Bar */}
//             <div className="flex gap-2">
//               <div className="relative flex-1">
//                 <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
//                 <Input
//                   placeholder="Search by keyword, location, or property name..."
//                   value={searchQuery}
//                   onChange={(e) => setSearchQuery(e.target.value)}
//                   onKeyDown={(e) => e.key === "Enter" && handleSearch()}
//                   className="pl-10 h-14 text-lg"
//                 />
//               </div>
//               <Button onClick={handleSearch} size="lg" className="h-14 px-8">
//                 Search
//               </Button>
//             </div>

//             {/* Filter Fields */}
//             <Card>
//               <CardContent className="p-6">
//                 <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
//                   {/* Location Filter */}
//                   <div className="space-y-2">
//                     <label className="text-sm font-medium">Location</label>
//                     <Input
//                       placeholder="e.g., Colombo, Kandy"
//                       value={location}
//                       onChange={(e) => setLocation(e.target.value)}
//                     />
//                   </div>

//                   {/* Property Type Filter */}
//                   <div className="space-y-2">
//                     <label className="text-sm font-medium">Property Type</label>
//                     <Select value={propertyType} onValueChange={setPropertyType}>
//                       <SelectTrigger>
//                         <SelectValue placeholder="Any" />
//                       </SelectTrigger>
//                       <SelectContent>
//                         <SelectItem value="any">Any</SelectItem>
//                         <SelectItem value="house">House</SelectItem>
//                         <SelectItem value="apartment">Apartment</SelectItem>
//                         <SelectItem value="villa">Villa</SelectItem>
//                         <SelectItem value="land">Land</SelectItem>
//                         <SelectItem value="commercial">Commercial</SelectItem>
//                       </SelectContent>
//                     </Select>
//                   </div>

//                   {/* Min Price Filter */}
//                   <div className="space-y-2">
//                     <label className="text-sm font-medium">Min Price</label>
//                     <Input
//                       type="number"
//                       placeholder="0"
//                       value={minPrice}
//                       onChange={(e) => setMinPrice(e.target.value)}
//                     />
//                   </div>

//                   {/* Max Price Filter */}
//                   <div className="space-y-2">
//                     <label className="text-sm font-medium">Max Price</label>
//                     <Input
//                       type="number"
//                       placeholder="Any"
//                       value={maxPrice}
//                       onChange={(e) => setMaxPrice(e.target.value)}
//                     />
//                   </div>

//                   {/* Bedrooms Filter */}
//                   <div className="space-y-2">
//                     <label className="text-sm font-medium">Bedrooms</label>
//                     <Select value={bedrooms} onValueChange={setBedrooms}>
//                       <SelectTrigger>
//                         <SelectValue placeholder="Any" />
//                       </SelectTrigger>
//                       <SelectContent>
//                         <SelectItem value="0">Any</SelectItem>
//                         <SelectItem value="1">1+</SelectItem>
//                         <SelectItem value="2">2+</SelectItem>
//                         <SelectItem value="3">3+</SelectItem>
//                         <SelectItem value="4">4+</SelectItem>
//                       </SelectContent>
//                     </Select>
//                   </div>


//                 </div>

//                 <div className="flex gap-2 mt-4">
//                   <Button onClick={handleSearch} className="flex-1">
//                     Apply Filters
//                   </Button>
//                   <Button onClick={handleReset} variant="outline">
//                     Reset
//                   </Button>
//                 </div>
//               </CardContent>
//             </Card>
//           </div>
//         </div>
//       </div>

//       {/* Results Section */}
//       <div className="container mx-auto px-4 py-12">
//         <div className="mb-8">
//           <h2 className="text-2xl font-bold mb-2">
//             {isSearchMode && isLoading
//               ? "Searching..."
//               : isSearchMode
//                 ? `${totalCount} Search Results`
//                 : isLoading
//                   ? "Loading featured properties..."
//                   : "Featured Properties"
//             }
//           </h2>
//           <p className="text-muted-foreground">
//             {isSearchMode ? "Results based on your search" : "Hand-picked properties for you"}

//           </p>
//         </div>

//         {isLoading ? (
//           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
//             {[...Array(6)].map((_, i) => (
//               <Card key={i} className="h-[400px] animate-pulse bg-muted/50" />
//             ))}
//           </div>
//         ) : (
//           <>
//             <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
//               {(isSearchMode ? filteredProperties : featuredProperties).map((property) => (
//                 <Link key={property.id} href={`/property/${property.id}`}>
//                   <Card className="overflow-hidden hover:shadow-lg transition-shadow cursor-pointer h-full">
//                     <div className="aspect-[4/3] relative overflow-hidden">
//                       <img
//                         src={property.image || "/placeholder.svg"}
//                         alt={property.title}
//                         className="object-cover w-full h-full hover:scale-105 transition-transform duration-300"
//                       />
//                       <Badge className="absolute top-4 right-4">{property.type}</Badge>
//                       {!isSearchMode && (
//                         <Badge variant="secondary" className="absolute top-4 left-4 bg-yellow-500 text-white border-none">
//                           Featured
//                         </Badge>
//                       )}
//                       {property.insight && (
//                         <TooltipProvider>
//                           <Tooltip delayDuration={200}>
//                             <TooltipTrigger asChild onClick={(e) => e.preventDefault()}>
//                               <div className="absolute top-12 right-4 bg-primary text-primary-foreground p-2 rounded-full cursor-help z-20 shadow-md hover:bg-primary/90 transition-colors">
//                                 <Lightbulb className="h-4 w-4" />
//                               </div>
//                             </TooltipTrigger>
                            
//                             <TooltipContent side="left" align="start" className="max-w-[200px] p-3">
//                               {/* Tooltip content with text on the next line */}
//                               <div className="flex flex-col space-y-1">
//                                 <span className="font-bold text-[10px] uppercase tracking-wider opacity-70">
//                                   Property Insight
//                                 </span>
//                                 <p className="text-sm leading-tight font-medium">
//                                   {property.insight}
//                                 </p>
//                               </div>
//                             </TooltipContent>
//                           </Tooltip>
//                         </TooltipProvider>
//                       )}
//                     </div>
//                     <CardContent className="p-6 space-y-4">
//                       <div>
//                         <h3 className="font-bold text-xl mb-2 line-clamp-1">{property.title}</h3>
//                         <div className="flex items-center text-muted-foreground mb-3">
//                           <MapPin className="h-4 w-4 mr-1" />
//                           <span className="text-sm">{property.location}</span>
//                         </div>
//                         <p className="text-2xl font-bold text-primary">{property.price.toLocaleString()} LKR</p>
//                       </div>

//                       <div className="aspect-video rounded-lg overflow-hidden border">
//                         <iframe
//                           width="100%"
//                           height="100%"
//                           frameBorder="0"
//                           style={{ border: 0 }}
//                           src={`https://www.google.com/maps?q=${property.lat},${property.lng}&output=embed`}                          allowFullScreen
//                         />
//                       </div>

//                       <div className="flex items-center gap-4 text-sm text-muted-foreground border-t pt-4">
//                         <div className="flex items-center gap-1">
//                           <Bed className="h-4 w-4" />
//                           <span>{property.bedrooms} bed</span>
//                         </div>
//                         <div className="flex items-center gap-1">
//                           <Bath className="h-4 w-4" />
//                           <span>{property.bathrooms} bath</span>
//                         </div>
//                         <div className="flex items-center gap-1">
//                           <Square className="h-4 w-4" />
//                           <span>{property.sqft} sqft</span>
//                         </div>
//                       </div>
//                     </CardContent>
//                   </Card>
//                 </Link>
//               ))}
//             </div>

//             {isSearchMode && filteredProperties.length === 0 && (
//               <div className="text-center py-16">
//                 <p className="text-xl text-muted-foreground">No properties found matching your search.</p>
//                 <Button onClick={handleReset} variant="link" className="mt-2">
//                   Return to Featured Properties
//                 </Button>
//               </div>
//             )}

//             {/* Pagination Controls */}
//             {/* [ADDED]: Check to hide pagination when viewing Featured properties */}
//             {isSearchMode && totalCount > itemsPerPage && (
//               <div className="flex justify-center items-center gap-4 mt-12 pb-12">
//                 <Button
//                   variant="outline"
//                   disabled={currentPage === 1 || isLoading}
//                   onClick={() => handleSearch(currentPage - 1)}
//                 >
//                   Previous
//                 </Button>
//                 <span className="text-sm font-medium">Page {currentPage}</span>
//                 <Button
//                   variant="outline"
//                   disabled={currentPage * itemsPerPage >= totalCount || isLoading}
//                   onClick={() => handleSearch(currentPage + 1)}
//                 >
//                   Next
//                 </Button>
//               </div>
//             )}
//           </>
//         )}
//       </div>
//     </div>
//   )
// }
// __________________________________














"use client"

import { useEffect, useRef, useState } from "react"
import { Search, MapPin, Bed, Bath, Square, Lightbulb } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import Link from "next/link"
import { Header } from "@/components/header"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

// ---------------------------------------------------------------------------
// Mock data — active when NEXT_PUBLIC_USE_MOCK_DATA=true OR when the API
// is unreachable. Remove this block (and the fallbacks below) once the
// backend is stable.
// ---------------------------------------------------------------------------
import { MOCK_PROPERTIES } from "./mockData"

const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK_DATA === "true"

/** Client-side search filter applied to mock data — mirrors backend logic */
function filterMock(
  props: PropertySummary[],
  {
    query, location, minPrice, maxPrice, propertyType, bedrooms,
  }: {
    query: string; location: string; minPrice: string; maxPrice: string
    propertyType: string; bedrooms: string
  }
): PropertySummary[] {
  const q = query.toLowerCase()
  return props.filter((p) => {
    if (q && !p.title.toLowerCase().includes(q) && !p.location.toLowerCase().includes(q)) return false
    if (location && !p.location.toLowerCase().includes(location.toLowerCase())) return false
    if (minPrice && p.price < parseFloat(minPrice)) return false
    if (maxPrice && p.price > parseFloat(maxPrice)) return false
    if (propertyType && propertyType !== "any" && p.type.toLowerCase() !== propertyType.toLowerCase()) return false
    if (bedrooms && bedrooms !== "0" && p.bedrooms < parseInt(bedrooms)) return false
    return true
  })
}

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

/**
 * Shape the backend must return for every property in list / search responses.
 *
 * REQUIRED — card cannot render without these:
 *   id        – unique identifier used in the detail-page URL  /property/:id
 *   title     – property name shown as the card heading
 *   location  – human-readable address / area string
 *   price     – numeric price in LKR (no currency symbol)
 *   bedrooms  – integer bedroom count
 *   bathrooms – integer bathroom count
 *   sqft      – floor area in square feet (integer)
 *   type      – one of: "House" | "Apartment" | "Villa" | "Land" | "Commercial"
 *   image     – URL of the primary listing image (absolute, or relative to /public)
 *
 * OPTIONAL — rendered only when present:
 *   insight   – short AI-generated insight string shown in the lightbulb tooltip
 *   lat       – latitude  (used on the detail page map, not the card)
 *   lng       – longitude (same)
 */
export interface PropertySummary {
  id: string | number
  title: string
  location: string
  price: number
  bedrooms: number
  bathrooms: number
  sqft: number
  type: string
  image: string
  insight?: string
  lat?: number
  lng?: number
}

interface PropertyListResponse {
  results: PropertySummary[]
  totalCount: number
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function SkeletonCard() {
  return (
    <Card className="overflow-hidden h-full">
      <div className="aspect-[4/3] bg-muted animate-pulse" />
      <CardContent className="p-6 space-y-3">
        <div className="h-5 bg-muted animate-pulse rounded w-3/4" />
        <div className="h-4 bg-muted animate-pulse rounded w-1/2" />
        <div className="h-6 bg-muted animate-pulse rounded w-1/3" />
        <div className="flex gap-4 pt-4 border-t">
          {[1, 2, 3].map((n) => (
            <div key={n} className="h-4 bg-muted animate-pulse rounded w-16" />
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

function PropertyCard({
  property,
  index,
  isFeatured,
}: {
  property: PropertySummary
  index: number
  isFeatured: boolean
}) {
  return (
    <Link href={`/property/${property.id}`} className="block h-full">
      <Card
        className="overflow-hidden hover:shadow-lg transition-shadow cursor-pointer h-full"
        style={{
          // Staggered fade-up: each card is delayed by 55 ms × its grid position.
          animation: `cardReveal 0.35s ease-out ${index * 55}ms both`,
        }}
      >
        <div className="aspect-[4/3] relative overflow-hidden bg-muted">
          <img
            src={property.image || "/placeholder.svg"}
            alt={property.title}
            className="object-cover w-full h-full hover:scale-105 transition-transform duration-300"
            loading="lazy"
            onError={(e) => {
              ;(e.currentTarget as HTMLImageElement).src = "/placeholder.svg"
            }}
          />
          <Badge className="absolute top-4 right-4">{property.type}</Badge>
          {isFeatured && (
            <Badge
              variant="secondary"
              className="absolute top-4 left-4 bg-yellow-500 text-white border-none"
            >
              Featured
            </Badge>
          )}
          {property.insight && (
            <TooltipProvider>
              <Tooltip delayDuration={200}>
                <TooltipTrigger
                  asChild
                  onClick={(e) => e.preventDefault()}
                >
                  <div className="absolute top-12 right-4 bg-primary text-primary-foreground p-2 rounded-full cursor-help z-20 shadow-md hover:bg-primary/90 transition-colors">
                    <Lightbulb className="h-4 w-4" />
                  </div>
                </TooltipTrigger>
                <TooltipContent side="left" align="start" className="max-w-[200px] p-3">
                  <div className="flex flex-col space-y-1">
                    <span className="font-bold text-[10px] uppercase tracking-wider opacity-70">
                      Property Insight
                    </span>
                    <p className="text-sm leading-tight font-medium">{property.insight}</p>
                  </div>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          )}
        </div>

        <CardContent className="p-6 space-y-4">
          <div>
            <h3 className="font-bold text-xl mb-2 line-clamp-1">{property.title}</h3>
            <div className="flex items-center text-muted-foreground mb-3">
              <MapPin className="h-4 w-4 mr-1 shrink-0" />
              <span className="text-sm line-clamp-1">{property.location}</span>
            </div>
            <p className="text-2xl font-bold text-primary">
              {property.price.toLocaleString()} LKR
            </p>
          </div>
          <div className="flex items-center gap-4 text-sm text-muted-foreground border-t pt-4">
            <span className="flex items-center gap-1"><Bed className="h-4 w-4" />{property.bedrooms} bed</span>
            <span className="flex items-center gap-1"><Bath className="h-4 w-4" />{property.bathrooms} bath</span>
            <span className="flex items-center gap-1"><Square className="h-4 w-4" />{property.sqft} sqft</span>
          </div>
        </CardContent>
      </Card>
    </Link>
  )
}

// ---------------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------------

export default function PropertySearchPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [location, setLocation] = useState("")
  const [bedrooms, setBedrooms] = useState("")
  const [minPrice, setMinPrice] = useState("")
  const [maxPrice, setMaxPrice] = useState("")
  const [propertyType, setPropertyType] = useState("")

  const [featuredProperties, setFeaturedProperties] = useState<PropertySummary[]>([])
  const [searchResults, setSearchResults] = useState<PropertySummary[]>([])
  const [isSearchMode, setIsSearchMode] = useState(false)

  const [featuredLoading, setFeaturedLoading] = useState(true)
  const [searchLoading, setSearchLoading] = useState(false)

  const [totalCount, setTotalCount] = useState(0)
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 20

  // Cancels in-flight requests when a new search starts
  const abortRef = useRef<AbortController | null>(null)

  // -- Featured on mount ---------------------------------------------------
  useEffect(() => {
    ;(async () => {
      if (USE_MOCK) {
        // Simulate a brief network delay so skeletons are visible
        await new Promise((r) => setTimeout(r, 600))
        setFeaturedProperties(MOCK_PROPERTIES)
        setFeaturedLoading(false)
        return
      }
      try {
        const res = await fetch(`${API_BASE}/api/v1/featured`)
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data: PropertyListResponse = await res.json()
        setFeaturedProperties(data.results ?? [])
      } catch (err) {
        console.error("Featured fetch error — falling back to mock data:", err)
        setFeaturedProperties(MOCK_PROPERTIES)
      } finally {
        setFeaturedLoading(false)
      }
    })()
  }, [])

  // -- Search --------------------------------------------------------------
  const handleSearch = async (pageNumber = 1) => {
    abortRef.current?.abort()
    abortRef.current = new AbortController()

    setSearchLoading(true)
    setIsSearchMode(true)
    setCurrentPage(pageNumber)

    try {
      if (USE_MOCK) {
        await new Promise((r) => setTimeout(r, 500))
        const filtered = filterMock(MOCK_PROPERTIES, {
          query: searchQuery, location, minPrice, maxPrice, propertyType, bedrooms,
        })
        const start = (pageNumber - 1) * itemsPerPage
        setSearchResults(filtered.slice(start, start + itemsPerPage))
        setTotalCount(filtered.length)
        return
      }
      const res = await fetch(`${API_BASE}/api/v1/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        signal: abortRef.current.signal,
        body: JSON.stringify({
          query: searchQuery,
          location: location || null,
          min_price: minPrice ? parseFloat(minPrice) : null,
          max_price: maxPrice ? parseFloat(maxPrice) : null,
          property_type: propertyType && propertyType !== "any" ? propertyType : null,
          no_bedrooms: bedrooms && bedrooms !== "0" ? parseInt(bedrooms) : null,
          page: pageNumber,
          limit: itemsPerPage,
        }),
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data: PropertyListResponse = await res.json()
      setSearchResults(data.results ?? [])
      setTotalCount(data.totalCount ?? 0)
    } catch (err: any) {
      if (err.name !== "AbortError") {
        console.error("Search error — falling back to mock data:", err)
        const filtered = filterMock(MOCK_PROPERTIES, {
          query: searchQuery, location, minPrice, maxPrice, propertyType, bedrooms,
        })
        setSearchResults(filtered)
        setTotalCount(filtered.length)
      }
    } finally {
      setSearchLoading(false)
    }
  }

  const handleReset = () => {
    abortRef.current?.abort()
    setSearchQuery("")
    setLocation("")
    setBedrooms("")
    setMinPrice("")
    setMaxPrice("")
    setPropertyType("")
    setIsSearchMode(false)
    setSearchResults([])
    setCurrentPage(1)
  }

  const displayProperties = isSearchMode ? searchResults : featuredProperties
  const isLoading = isSearchMode ? searchLoading : featuredLoading

  return (
    <>
      <style>{`
        @keyframes cardReveal {
          from { opacity: 0; transform: translateY(14px); }
          to   { opacity: 1; transform: translateY(0);    }
        }
      `}</style>

      <div className="min-h-screen bg-background">
        <Header />

        {/* Search bar + filters */}
        <div className="bg-card border-b">
          <div className="container mx-auto px-4 py-8">
            <div className="max-w-5xl mx-auto space-y-6">
              <div className="text-center space-y-2">
                <h2 className="text-4xl font-bold text-balance">Find Your Perfect Home</h2>
                <p className="text-lg text-muted-foreground">Search from thousands of properties</p>
              </div>

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
                <Button
                  onClick={() => handleSearch()}
                  size="lg"
                  className="h-14 px-8"
                  disabled={searchLoading}
                >
                  {searchLoading ? "Searching…" : "Search"}
                </Button>
              </div>

              <Card>
                <CardContent className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
                    <div className="space-y-2">
                      <label className="text-sm font-medium">Location</label>
                      <Input
                        placeholder="e.g., Colombo, Kandy"
                        value={location}
                        onChange={(e) => setLocation(e.target.value)}
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium">Property Type</label>
                      <Select value={propertyType} onValueChange={setPropertyType}>
                        <SelectTrigger><SelectValue placeholder="Any" /></SelectTrigger>
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
                    <div className="space-y-2">
                      <label className="text-sm font-medium">Min Price</label>
                      <Input type="number" placeholder="0" value={minPrice} onChange={(e) => setMinPrice(e.target.value)} />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium">Max Price</label>
                      <Input type="number" placeholder="Any" value={maxPrice} onChange={(e) => setMaxPrice(e.target.value)} />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium">Bedrooms</label>
                      <Select value={bedrooms} onValueChange={setBedrooms}>
                        <SelectTrigger><SelectValue placeholder="Any" /></SelectTrigger>
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
                    <Button onClick={() => handleSearch()} className="flex-1" disabled={searchLoading}>
                      Apply Filters
                    </Button>
                    <Button onClick={handleReset} variant="outline">Reset</Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>

        {/* Results */}
        <div className="container mx-auto px-4 py-12">
          <div className="mb-8">
            <h2 className="text-2xl font-bold mb-2">
              {isSearchMode
                ? searchLoading
                  ? "Searching…"
                  : `${totalCount} Search Result${totalCount !== 1 ? "s" : ""}`
                : featuredLoading
                  ? "Loading featured properties…"
                  : "Featured Properties"}
            </h2>
            <p className="text-muted-foreground">
              {isSearchMode ? "Results based on your search" : "Hand-picked properties for you"}
            </p>
          </div>

          {/* Only show full skeleton on very first load; after that keep stale cards */}
          {isLoading && displayProperties.length === 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => <SkeletonCard key={i} />)}
            </div>
          ) : (
            <>
              {/*
                key resets CSS animations on every new result set so cards
                always play the staggered entrance from scratch.
              */}
              <div
                key={`${isSearchMode ? "search" : "featured"}-${currentPage}-${displayProperties.length}`}
                className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
              >
                {displayProperties.map((property, index) => (
                  <PropertyCard
                    key={property.id}
                    property={property}
                    index={index}
                    isFeatured={!isSearchMode}
                  />
                ))}
              </div>

              {isSearchMode && !searchLoading && searchResults.length === 0 && (
                <div className="text-center py-16">
                  <p className="text-xl text-muted-foreground">No properties found matching your search.</p>
                  <Button onClick={handleReset} variant="link" className="mt-2">
                    Return to Featured Properties
                  </Button>
                </div>
              )}

              {isSearchMode && totalCount > itemsPerPage && (
                <div className="flex justify-center items-center gap-4 mt-12 pb-12">
                  <Button
                    variant="outline"
                    disabled={currentPage === 1 || searchLoading}
                    onClick={() => handleSearch(currentPage - 1)}
                  >
                    Previous
                  </Button>
                  <span className="text-sm font-medium">
                    Page {currentPage} of {Math.ceil(totalCount / itemsPerPage)}
                  </span>
                  <Button
                    variant="outline"
                    disabled={currentPage * itemsPerPage >= totalCount || searchLoading}
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
    </>
  )
}
