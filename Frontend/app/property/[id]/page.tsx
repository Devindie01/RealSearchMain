// "use client"

// import { useParams, useRouter } from "next/navigation"
// import { Button } from "@/components/ui/button"
// import { Card, CardContent } from "@/components/ui/card"
// import { Badge } from "@/components/ui/badge"
// import { Separator } from "@/components/ui/separator"
// import { MapPin, Bed, Bath, Square, Calendar, Phone, Mail } from "lucide-react"
// import Link from "next/link"
// import { Header } from "@/components/header"

// // Mock property data (same as in the main page)
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
// //     fullDescription:
// //       "This exceptional modern loft offers the perfect blend of urban sophistication and comfortable living. Located in the heart of Colombo, this property features floor-to-ceiling windows that flood the space with natural light and provide breathtaking city views. The open-concept layout includes a gourmet kitchen with stainless steel appliances, quartz countertops, and custom cabinetry. Beautiful hardwood floors throughout, high ceilings, and premium finishes make this loft truly special.",
// //     yearBuilt: 2020,
// //     parking: "2 spaces",
// //     heating: "Central heating",
// //     cooling: "Central A/C",
// //     lat: 6.9271,
// //     lng: 79.8612,
// //     features: [
// //       "Floor-to-ceiling windows",
// //       "Hardwood floors",
// //       "Stainless steel appliances",
// //       "Quartz countertops",
// //       "In-unit washer/dryer",
// //       "Walk-in closets",
// //       "Balcony",
// //       "Gym access",
// //       "24/7 security",
// //     ],
// //   },
// // ]
// mockProperties = []
// export default function PropertyDetailPage() {
//   const params = useParams()
//   const router = useRouter()
//   const propertyId = Number.parseInt(params.id as string)

//   const property = mockProperties.find((p) => p.id === propertyId)

//   if (!property) {
//     return (
//       <div className="min-h-screen bg-background flex items-center justify-center p-4">
//         <Card className="max-w-md w-full text-center">
//           <CardContent className="pt-12 pb-12">
//             <h2 className="text-2xl font-bold mb-4">Property Not Found</h2>
//             <p className="text-muted-foreground mb-6">The property you're looking for doesn't exist.</p>
//             <Link href="/">
//               <Button>Back to Search</Button>
//             </Link>
//           </CardContent>
//         </Card>
//       </div>
//     )
//   }

//   return (
//     <div className="min-h-screen bg-background">
//       {/* Header */}
//       <Header />

//       {/* Hero Image */}
//       <div className="w-full aspect-[21/9] relative overflow-hidden bg-muted">
//         <img src={property.image || "/placeholder.svg"} alt={property.title} className="object-cover w-full h-full" />
//         <Badge className="absolute top-6 right-6 text-base px-4 py-2">{property.type}</Badge>
//       </div>

//       {/* Content */}
//       <div className="container mx-auto px-4 py-8">
//         <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
//           {/* Main Content */}
//           <div className="lg:col-span-2 space-y-8">
//             {/* Title and Price */}
//             <div>
//               <h1 className="text-4xl font-bold mb-4 text-balance">{property.title}</h1>
//               <div className="flex items-center text-muted-foreground mb-4">
//                 <MapPin className="h-5 w-5 mr-2" />
//                 <span className="text-lg">{property.location}</span>
//               </div>
//               <p className="text-4xl font-bold text-primary">{property.price.toLocaleString()} LKR</p>
//             </div>

//             <Separator />

//             {/* Key Stats */}
//             <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
//               <div className="flex flex-col items-center p-4 bg-muted rounded-lg">
//                 <Bed className="h-8 w-8 mb-2 text-primary" />
//                 <span className="text-2xl font-bold">{property.bedrooms}</span>
//                 <span className="text-sm text-muted-foreground">Bedrooms</span>
//               </div>
//               <div className="flex flex-col items-center p-4 bg-muted rounded-lg">
//                 <Bath className="h-8 w-8 mb-2 text-primary" />
//                 <span className="text-2xl font-bold">{property.bathrooms}</span>
//                 <span className="text-sm text-muted-foreground">Bathrooms</span>
//               </div>
//               <div className="flex flex-col items-center p-4 bg-muted rounded-lg">
//                 <Square className="h-8 w-8 mb-2 text-primary" />
//                 <span className="text-2xl font-bold">{property.sqft}</span>
//                 <span className="text-sm text-muted-foreground">Sq Ft</span>
//               </div>
//               <div className="flex flex-col items-center p-4 bg-muted rounded-lg">
//                 <Calendar className="h-8 w-8 mb-2 text-primary" />
//                 <span className="text-2xl font-bold">{property.yearBuilt}</span>
//                 <span className="text-sm text-muted-foreground">Year Built</span>
//               </div>
//             </div>

//             <Separator />

//             {/* Location */}
//             <div>
//               <h2 className="text-2xl font-bold mb-4">Location</h2>
//               <div className="aspect-video rounded-lg overflow-hidden border">
//                 <iframe
//                   width="100%"
//                   height="100%"
//                   frameBorder="0"
//                   style={{ border: 0 }}
//                   src={`https://www.google.com/maps/embed/v1/place?key=AIzaSyBFw0Qbyq9zTFTd-tUY6dZWTgaQzuU17R8&q=${property.lat},${property.lng}&zoom=15`}
//                   allowFullScreen
//                 />
//               </div>
//             </div>

//             <Separator />

//             {/* Description */}
//             <div>
//               <h2 className="text-2xl font-bold mb-4">About This Property</h2>
//               <p className="text-muted-foreground leading-relaxed">{property.fullDescription}</p>
//             </div>

//             <Separator />

//             {/* Features */}
//             <div>
//               <h2 className="text-2xl font-bold mb-4">Features & Amenities</h2>
//               <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
//                 {property.features.map((feature, index) => (
//                   <div key={index} className="flex items-center gap-2">
//                     <div className="h-2 w-2 rounded-full bg-primary" />
//                     <span className="text-muted-foreground">{feature}</span>
//                   </div>
//                 ))}
//               </div>
//             </div>

//             <Separator />

//             {/* Additional Details */}
//             <div>
//               <h2 className="text-2xl font-bold mb-4">Property Details</h2>
//               <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
//                 <div className="flex justify-between p-3 bg-muted rounded-lg">
//                   <span className="text-muted-foreground">Parking</span>
//                   <span className="font-semibold">{property.parking}</span>
//                 </div>
//                 <div className="flex justify-between p-3 bg-muted rounded-lg">
//                   <span className="text-muted-foreground">Heating</span>
//                   <span className="font-semibold">{property.heating}</span>
//                 </div>
//                 <div className="flex justify-between p-3 bg-muted rounded-lg">
//                   <span className="text-muted-foreground">Cooling</span>
//                   <span className="font-semibold">{property.cooling}</span>
//                 </div>
//                 <div className="flex justify-between p-3 bg-muted rounded-lg">
//                   <span className="text-muted-foreground">Year Built</span>
//                   <span className="font-semibold">{property.yearBuilt}</span>
//                 </div>
//               </div>
//             </div>
//           </div>

//           {/* Sidebar */}
//           <div className="lg:col-span-1">
//             <Card className="sticky top-24">
//               <CardContent className="p-6 space-y-6">
//                 <div>
//                   <h3 className="text-xl font-bold mb-2">Interested in this property?</h3>
//                   <p className="text-sm text-muted-foreground">
//                     Contact us to schedule a viewing or get more information
//                   </p>
//                 </div>

//                 <Separator />

//                 <div className="space-y-3">
//                   <Button className="w-full" size="lg">
//                     <Phone className="h-5 w-5 mr-2" />
//                     Call Agent
//                   </Button>
//                   <Button variant="outline" className="w-full bg-transparent" size="lg">
//                     <Mail className="h-5 w-5 mr-2" />
//                     Send Message
//                   </Button>
//                 </div>

//                 <Separator />

//                 <div className="space-y-2 text-sm">
//                   <div className="flex justify-between">
//                     <span className="text-muted-foreground">Property ID</span>
//                     <span className="font-semibold">#{property.id.toString().padStart(6, "0")}</span>
//                   </div>
//                   <div className="flex justify-between">
//                     <span className="text-muted-foreground">Listed</span>
//                     <span className="font-semibold">2 weeks ago</span>
//                   </div>
//                   <div className="flex justify-between">
//                     <span className="text-muted-foreground">Views</span>
//                     <span className="font-semibold">1,234</span>
//                   </div>
//                 </div>
//               </CardContent>
//             </Card>
//           </div>
//         </div>
//       </div>
//     </div>
//   )
// }
// ____________________________________














"use client"

import { useEffect, useRef, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import {
  MapPin, Bed, Bath, Square, Calendar, Phone, Mail,
  ArrowLeft, ChevronLeft, ChevronRight, Sparkles,
} from "lucide-react"
import Link from "next/link"
import { Header } from "@/components/header"

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"
const MAPS_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_KEY ?? ""

import { MOCK_PROPERTY_DETAILS, MOCK_PROPERTIES, MOCK_EXPLANATIONS } from "../../mockData"

const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK_DATA === "true"

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

/**
 * Full property object returned by GET /api/v1/properties/:id
 *
 * REQUIRED:
 *   id            – matches the URL param
 *   title         – property heading
 *   location      – display address
 *   price         – numeric LKR
 *   bedrooms      – integer
 *   bathrooms     – integer
 *   sqft          – integer
 *   type          – "House" | "Apartment" | "Villa" | "Land" | "Commercial"
 *   image         – primary image URL  (shown first in the gallery)
 *   lat           – latitude for the map embed
 *   lng           – longitude for the map embed
 *
 * OPTIONAL (rendered only when present):
 *   images        – string[]  extra gallery images (image is always slide 0)
 *   fullDescription – long-form description paragraph
 *   features      – string[]  bullet-point amenities list
 *   yearBuilt     – number
 *   parking       – string   e.g. "2 spaces"
 *   heating       – string   e.g. "Central heating"
 *   cooling       – string   e.g. "Central A/C"
 *   insight       – short AI insight string (shown in the explainability panel
 *                   when the streaming endpoint is NOT configured)
 *
 * EXPLAINABILITY STREAMING  (GET /api/v1/properties/:id/explain)
 *   The endpoint should return text/event-stream with chunks of plain text.
 *   Each SSE event: `data: <chunk>\n\n`
 *   The panel renders tokens as they arrive without waiting for the stream to finish.
 *   If the endpoint is absent the panel falls back to the static `insight` field.
 */
interface PropertyDetail {
  id: string | number
  title: string
  location: string
  price: number
  bedrooms: number
  bathrooms: number
  sqft: number
  type: string
  image: string
  lat: number
  lng: number
  images?: string[]
  fullDescription?: string
  features?: string[]
  yearBuilt?: number
  parking?: string
  heating?: string
  cooling?: string
  insight?: string
}

// ---------------------------------------------------------------------------
// Image gallery
// ---------------------------------------------------------------------------

function Gallery({ images, title }: { images: string[]; title: string }) {
  const [current, setCurrent] = useState(0)

  const prev = () => setCurrent((c) => (c - 1 + images.length) % images.length)
  const next = () => setCurrent((c) => (c + 1) % images.length)

  return (
    <div className="w-full aspect-[21/9] relative overflow-hidden bg-muted group">
      {/* Main image */}
      <img
        key={current}
        src={images[current] || "/placeholder.svg"}
        alt={`${title} — photo ${current + 1}`}
        className="object-cover w-full h-full transition-opacity duration-300"
        onError={(e) => {
          ;(e.currentTarget as HTMLImageElement).src = "/placeholder.svg"
        }}
      />

      {/* Navigation arrows — only shown when there are multiple images */}
      {images.length > 1 && (
        <>
          <button
            onClick={prev}
            aria-label="Previous image"
            className="absolute left-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white rounded-full p-2 opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <ChevronLeft className="h-5 w-5" />
          </button>
          <button
            onClick={next}
            aria-label="Next image"
            className="absolute right-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white rounded-full p-2 opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <ChevronRight className="h-5 w-5" />
          </button>

          {/* Dot indicators */}
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-1.5">
            {images.map((_, i) => (
              <button
                key={i}
                aria-label={`Go to image ${i + 1}`}
                onClick={() => setCurrent(i)}
                className={`h-2 rounded-full transition-all ${
                  i === current
                    ? "w-6 bg-white"
                    : "w-2 bg-white/60 hover:bg-white/80"
                }`}
              />
            ))}
          </div>
        </>
      )}

      {/* Image counter */}
      {images.length > 1 && (
        <div className="absolute top-4 left-4 bg-black/50 text-white text-xs px-2 py-1 rounded-full">
          {current + 1} / {images.length}
        </div>
      )}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Explainability panel — streams text tokens as they arrive
// ---------------------------------------------------------------------------

/**
 * How it works:
 *  1. On mount it opens a fetch stream to /api/v1/properties/:id/explain
 *  2. Reads the response body as a ReadableStream, decoding each chunk.
 *  3. Appends each chunk to `streamedText` immediately — the UI re-renders
 *     with every new token so the user sees text appearing word-by-word.
 *  4. If the endpoint returns a non-2xx status or the fetch fails entirely,
 *     it falls back to the static `insight` prop.
 *
 * Backend requirement:
 *   GET /api/v1/properties/:id/explain
 *   Response: Content-Type: text/plain  OR  text/event-stream
 *   Body: plain text chunks streamed progressively.
 *   (SSE format also supported — the reader strips "data: " prefixes.)
 */
function ExplainabilityPanel({
  propertyId,
  fallbackInsight,
}: {
  propertyId: string | number
  fallbackInsight?: string
}) {
  const [streamedText, setStreamedText] = useState("")
  const [isStreaming, setIsStreaming] = useState(false)
  const [isDone, setIsDone] = useState(false)
  const [usedFallback, setUsedFallback] = useState(false)
  const abortRef = useRef<AbortController | null>(null)

  useEffect(() => {
    abortRef.current = new AbortController()

    const stream = async () => {
      setIsStreaming(true)
      setStreamedText("")
      setIsDone(false)
      setUsedFallback(false)

      // --- Mock streaming: type out the explanation word by word ---
      const mockText = MOCK_EXPLANATIONS[Number(propertyId)]
      if (USE_MOCK || mockText) {
        if (mockText) {
          const words = mockText.split(" ")
          for (let i = 0; i < words.length; i++) {
            if (abortRef.current?.signal.aborted) return
            // Vary delay slightly so it feels natural, not robotic
            await new Promise((r) => setTimeout(r, 28 + Math.random() * 22))
            setStreamedText((prev) => prev + (i === 0 ? "" : " ") + words[i])
          }
        } else if (fallbackInsight) {
          setStreamedText(fallbackInsight)
          setUsedFallback(true)
        }
        setIsDone(true)
        setIsStreaming(false)
        return
      }
      // --- End mock ---

      try {
        const res = await fetch(`${API_BASE}/api/v1/properties/${propertyId}/explain`, {
          signal: abortRef.current!.signal,
        })

        if (!res.ok || !res.body) {
          // Endpoint not available — show static insight instead
          if (fallbackInsight) {
            setStreamedText(fallbackInsight)
            setUsedFallback(true)
          }
          setIsDone(true)
          setIsStreaming(false)
          return
        }

        const reader = res.body.getReader()
        const decoder = new TextDecoder()

        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          let chunk = decoder.decode(value, { stream: true })

          // Strip SSE "data: " prefix if the backend sends event-stream format
          chunk = chunk
            .split("\n")
            .map((line) => (line.startsWith("data: ") ? line.slice(6) : line))
            .filter((line) => line !== "[DONE]")
            .join("\n")

          setStreamedText((prev) => prev + chunk)
        }
      } catch (err: any) {
        if (err.name === "AbortError") return
        // Network error — show fallback
        if (fallbackInsight) {
          setStreamedText(fallbackInsight)
          setUsedFallback(true)
        }
      } finally {
        setIsDone(true)
        setIsStreaming(false)
      }
    }

    stream()

    return () => {
      abortRef.current?.abort()
    }
  }, [propertyId]) // re-run if the property changes

  if (!streamedText && !isStreaming) return null

  return (
    <Card className="border-primary/20 bg-primary/5">
      <CardContent className="p-5">
        <div className="flex items-center gap-2 mb-3">
          <Sparkles className="h-4 w-4 text-primary" />
          <span className="text-sm font-semibold text-primary">
            {usedFallback ? "Property Insight" : "AI Analysis"}
          </span>
          {isStreaming && (
            <span className="ml-auto flex items-center gap-1 text-xs text-muted-foreground">
              <span className="inline-block h-1.5 w-1.5 rounded-full bg-primary animate-pulse" />
              Generating…
            </span>
          )}
        </div>
        <p className="text-sm leading-relaxed text-foreground whitespace-pre-wrap">
          {streamedText}
          {/* Blinking cursor while streaming */}
          {isStreaming && (
            <span className="inline-block w-0.5 h-4 bg-primary ml-0.5 align-middle animate-[blink_1s_step-end_infinite]" />
          )}
        </p>
      </CardContent>
    </Card>
  )
}

// ---------------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------------

export default function PropertyDetailPage() {
  const params = useParams()
  const router = useRouter()
  const propertyId = params.id as string

  const [property, setProperty] = useState<PropertyDetail | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<"not_found" | "fetch_error" | null>(null)

  useEffect(() => {
    if (!propertyId) return
    ;(async () => {
      try {
        setIsLoading(true)
        setError(null)

        if (USE_MOCK) {
          await new Promise((r) => setTimeout(r, 400))
          const id = parseInt(propertyId)
          const detail = MOCK_PROPERTY_DETAILS[id as keyof typeof MOCK_PROPERTY_DETAILS]
            ?? MOCK_PROPERTIES.find((p) => p.id === id)
          if (!detail) { setError("not_found"); return }
          setProperty(detail as PropertyDetail)
          return
        }

        const res = await fetch(`${API_BASE}/api/v1/properties/${propertyId}`)
        if (res.status === 404) { setError("not_found"); return }
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data: PropertyDetail = await res.json()
        setProperty(data)
      } catch {
        // API unreachable — try mock
        const id = parseInt(propertyId)
        const detail = MOCK_PROPERTY_DETAILS[id as keyof typeof MOCK_PROPERTY_DETAILS]
          ?? MOCK_PROPERTIES.find((p) => p.id === id)
        if (detail) {
          setProperty(detail as PropertyDetail)
        } else {
          setError("fetch_error")
        }
      } finally {
        setIsLoading(false)
      }
    })()
  }, [propertyId])

  // -- Loading skeleton ------------------------------------------------------
  if (isLoading) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="w-full aspect-[21/9] bg-muted animate-pulse" />
        <div className="container mx-auto px-4 py-8 space-y-6">
          {[...Array(5)].map((_, i) => (
            <div key={i} className={`h-${i === 0 ? 12 : 20} bg-muted animate-pulse rounded-lg`} />
          ))}
        </div>
      </div>
    )
  }

  // -- Error / not found -----------------------------------------------------
  if (error || !property) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="max-w-md w-full text-center">
          <CardContent className="pt-12 pb-12">
            <h2 className="text-2xl font-bold mb-4">
              {error === "not_found" ? "Property Not Found" : "Something went wrong"}
            </h2>
            <p className="text-muted-foreground mb-6">
              {error === "not_found"
                ? "This property doesn't exist or has been removed."
                : "We couldn't load this property. Please try again."}
            </p>
            <div className="flex gap-3 justify-center">
              <Button variant="outline" onClick={() => router.back()}>
                <ArrowLeft className="h-4 w-4 mr-2" /> Go Back
              </Button>
              <Link href="/"><Button>Back to Search</Button></Link>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  // Build gallery array: primary image first, then any extras from `images`
  const galleryImages = [
    property.image,
    ...(property.images ?? []).filter((u) => u && u !== property.image),
  ].filter(Boolean) as string[]

  // Google Maps embed URL — zooms to the exact coordinates
  const mapSrc = MAPS_KEY
    ? `https://www.google.com/maps/embed/v1/place?key=${MAPS_KEY}&q=${property.lat},${property.lng}&zoom=15`
    : `https://www.google.com/maps?q=${property.lat},${property.lng}&output=embed`

  return (
    <>
      {/* Blinking cursor keyframe for the streaming panel */}
      <style>{`
        @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
      `}</style>

      <div className="min-h-screen bg-background">
        <Header />

        {/* Hero image gallery */}
        <div className="relative">
          <Gallery images={galleryImages} title={property.title} />
          <Badge className="absolute top-6 right-6 text-base px-4 py-2 z-10">
            {property.type}
          </Badge>
        </div>

        {/* Main content */}
        <div className="container mx-auto px-4 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

            {/* Left column */}
            <div className="lg:col-span-2 space-y-8">

              {/* Title + price */}
              <div>
                <h1 className="text-4xl font-bold mb-4 text-balance">{property.title}</h1>
                <div className="flex items-center text-muted-foreground mb-4">
                  <MapPin className="h-5 w-5 mr-2 shrink-0" />
                  <span className="text-lg">{property.location}</span>
                </div>
                <p className="text-4xl font-bold text-primary">
                  {property.price.toLocaleString()} LKR
                </p>
              </div>

              <Separator />

              {/* Key stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                {[
                  { icon: Bed, value: property.bedrooms, label: "Bedrooms" },
                  { icon: Bath, value: property.bathrooms, label: "Bathrooms" },
                  { icon: Square, value: property.sqft, label: "Sq Ft" },
                  ...(property.yearBuilt
                    ? [{ icon: Calendar, value: property.yearBuilt, label: "Year Built" }]
                    : []),
                ].map(({ icon: Icon, value, label }) => (
                  <div key={label} className="flex flex-col items-center p-4 bg-muted rounded-lg">
                    <Icon className="h-8 w-8 mb-2 text-primary" />
                    <span className="text-2xl font-bold">{value}</span>
                    <span className="text-sm text-muted-foreground">{label}</span>
                  </div>
                ))}
              </div>

              <Separator />

              {/*
                Explainability panel.
                Mounts immediately after the property loads and starts streaming.
                Tokens are rendered as they arrive — no waiting for completion.
              */}
              <ExplainabilityPanel
                propertyId={property.id}
                fallbackInsight={property.insight}
              />

              <Separator />

              {/* Map — focused on property coordinates */}
              <div>
                <h2 className="text-2xl font-bold mb-4">Location</h2>
                <div className="aspect-video rounded-lg overflow-hidden border">
                  <iframe
                    width="100%"
                    height="100%"
                    frameBorder="0"
                    style={{ border: 0 }}
                    src={mapSrc}
                    allowFullScreen
                    loading="lazy"
                    referrerPolicy="no-referrer-when-downgrade"
                    title={`Map showing location of ${property.title}`}
                  />
                </div>
              </div>

              {/* Description */}
              {property.fullDescription && (
                <>
                  <Separator />
                  <div>
                    <h2 className="text-2xl font-bold mb-4">About This Property</h2>
                    <p className="text-muted-foreground leading-relaxed">{property.fullDescription}</p>
                  </div>
                </>
              )}

              {/* Features */}
              {(property.features?.length ?? 0) > 0 && (
                <>
                  <Separator />
                  <div>
                    <h2 className="text-2xl font-bold mb-4">Features &amp; Amenities</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {property.features!.map((feature, i) => (
                        <div key={i} className="flex items-center gap-2">
                          <div className="h-2 w-2 rounded-full bg-primary shrink-0" />
                          <span className="text-muted-foreground">{feature}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              )}

              {/* Extra property details */}
              {(property.parking || property.heating || property.cooling || property.yearBuilt) && (
                <>
                  <Separator />
                  <div>
                    <h2 className="text-2xl font-bold mb-4">Property Details</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {[
                        ["Parking", property.parking],
                        ["Heating", property.heating],
                        ["Cooling", property.cooling],
                        ["Year Built", property.yearBuilt],
                      ]
                        .filter(([, v]) => v)
                        .map(([label, value]) => (
                          <div key={label as string} className="flex justify-between p-3 bg-muted rounded-lg">
                            <span className="text-muted-foreground">{label}</span>
                            <span className="font-semibold">{value}</span>
                          </div>
                        ))}
                    </div>
                  </div>
                </>
              )}
            </div>

            {/* Sidebar */}
            <div className="lg:col-span-1">
              <Card className="sticky top-24">
                <CardContent className="p-6 space-y-6">
                  <div>
                    <h3 className="text-xl font-bold mb-2">Interested in this property?</h3>
                    <p className="text-sm text-muted-foreground">
                      Contact us to schedule a viewing or get more information.
                    </p>
                  </div>
                  <Separator />
                  <div className="space-y-3">
                    <Button className="w-full" size="lg">
                      <Phone className="h-5 w-5 mr-2" /> Call Agent
                    </Button>
                    <Button variant="outline" className="w-full bg-transparent" size="lg">
                      <Mail className="h-5 w-5 mr-2" /> Send Message
                    </Button>
                  </div>
                  <Separator />
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Property ID</span>
                      <span className="font-semibold">#{String(property.id).padStart(6, "0")}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Type</span>
                      <span className="font-semibold">{property.type}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
