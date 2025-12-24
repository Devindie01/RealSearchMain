"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { CheckCircle2, MapPin } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Header } from "@/components/header"

export default function SellPropertyPage() {
  const router = useRouter()
  const [submitted, setSubmitted] = useState(false)
  const [formData, setFormData] = useState({
    title: "",
    location: "",
    price: "",
    bedrooms: "",
    bathrooms: "",
    sqft: "",
    type: "",
    description: "",
    imageUrl: "",
    lat: "",
    lng: "",
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    console.log("[v0] Property submission:", formData)

    setSubmitted(true)

    setTimeout(() => {
      router.push("/")
    }, 2000)
  }

  const handleChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const handleGetCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setFormData((prev) => ({
            ...prev,
            lat: position.coords.latitude.toString(),
            lng: position.coords.longitude.toString(),
          }))
        },
        (error) => {
          console.error("[v0] Error getting location:", error)
          alert("Unable to get your location. Please enter coordinates manually.")
        },
      )
    } else {
      alert("Geolocation is not supported by your browser.")
    }
  }

  if (submitted) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="max-w-md w-full text-center">
          <CardContent className="pt-12 pb-12">
            <CheckCircle2 className="h-16 w-16 text-primary mx-auto mb-4" />
            <h2 className="text-2xl font-bold mb-2">Property Listed Successfully!</h2>
            <p className="text-muted-foreground mb-6">Your property has been submitted and will be reviewed shortly.</p>
            <p className="text-sm text-muted-foreground">Redirecting to home page...</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />

      {/* Form Section */}
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-3xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle>Property Details</CardTitle>
              <CardDescription>Fill in the information below to list your property on our platform</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Basic Information */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold">Basic Information</h3>

                  <div className="space-y-2">
                    <Label htmlFor="title">Property Title *</Label>
                    <Input
                      id="title"
                      placeholder="e.g., Modern Downtown Loft"
                      value={formData.title}
                      onChange={(e) => handleChange("title", e.target.value)}
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="type">Property Type *</Label>
                    <Select value={formData.type} onValueChange={(value) => handleChange("type", value)} required>
                      <SelectTrigger id="type">
                        <SelectValue placeholder="Select property type" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="House">House</SelectItem>
                        <SelectItem value="Apartment">Apartment</SelectItem>
                        <SelectItem value="Villa">Villa</SelectItem>
                        <SelectItem value="Land">Land</SelectItem>
                        <SelectItem value="Commercial">Commercial</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="location">Location *</Label>
                    <Input
                      id="location"
                      placeholder="e.g., Colombo 03, Sri Lanka"
                      value={formData.location}
                      onChange={(e) => handleChange("location", e.target.value)}
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="description">Description *</Label>
                    <Textarea
                      id="description"
                      placeholder="Describe your property, its features, and what makes it special..."
                      value={formData.description}
                      onChange={(e) => handleChange("description", e.target.value)}
                      rows={4}
                      required
                    />
                  </div>
                </div>

                {/* Property Specifications */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold">Property Specifications</h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="price">Price (LKR) *</Label>
                      <Input
                        id="price"
                        type="number"
                        placeholder="45000000"
                        value={formData.price}
                        onChange={(e) => handleChange("price", e.target.value)}
                        required
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="sqft">Square Feet *</Label>
                      <Input
                        id="sqft"
                        type="number"
                        placeholder="1200"
                        value={formData.sqft}
                        onChange={(e) => handleChange("sqft", e.target.value)}
                        required
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="bedrooms">Bedrooms *</Label>
                      <Input
                        id="bedrooms"
                        type="number"
                        placeholder="2"
                        value={formData.bedrooms}
                        onChange={(e) => handleChange("bedrooms", e.target.value)}
                        required
                        min="0"
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="bathrooms">Bathrooms *</Label>
                      <Input
                        id="bathrooms"
                        type="number"
                        step="0.5"
                        placeholder="2"
                        value={formData.bathrooms}
                        onChange={(e) => handleChange("bathrooms", e.target.value)}
                        required
                        min="0"
                      />
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <h3 className="text-lg font-semibold">Location Pin</h3>
                  <p className="text-sm text-muted-foreground">
                    Add your property location to help buyers find it on the map
                  </p>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="lat">Latitude *</Label>
                      <Input
                        id="lat"
                        type="number"
                        step="any"
                        placeholder="6.9271"
                        value={formData.lat}
                        onChange={(e) => handleChange("lat", e.target.value)}
                        required
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="lng">Longitude *</Label>
                      <Input
                        id="lng"
                        type="number"
                        step="any"
                        placeholder="79.8612"
                        value={formData.lng}
                        onChange={(e) => handleChange("lng", e.target.value)}
                        required
                      />
                    </div>
                  </div>

                  <Button
                    type="button"
                    variant="outline"
                    onClick={handleGetCurrentLocation}
                    className="w-full bg-transparent"
                  >
                    <MapPin className="h-4 w-4 mr-2" />
                    Use Current Location
                  </Button>

                  {formData.lat && formData.lng && (
                    <div className="aspect-video rounded-lg overflow-hidden border">
                      <iframe
                        width="100%"
                        height="100%"
                        frameBorder="0"
                        style={{ border: 0 }}
                        src={`https://www.google.com/maps/embed/v1/place?key=AIzaSyBFw0Qbyq9zTFTd-tUY6dZWTgaQzuU17R8&q=${formData.lat},${formData.lng}&zoom=15`}
                        allowFullScreen
                      />
                    </div>
                  )}
                </div>

                {/* Images */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold">Property Images</h3>

                  <div className="space-y-2">
                    <Label htmlFor="imageUrl">Image URL (Optional)</Label>
                    <Input
                      id="imageUrl"
                      type="url"
                      placeholder="https://example.com/image.jpg"
                      value={formData.imageUrl}
                      onChange={(e) => handleChange("imageUrl", e.target.value)}
                    />
                    <p className="text-sm text-muted-foreground">Provide a URL to your property image</p>
                  </div>
                </div>

                {/* Submit Button */}
                <div className="flex gap-4 pt-4">
                  <Button type="submit" size="lg" className="flex-1">
                    Submit Property Listing
                  </Button>
                  <Link href="/" className="flex-1">
                    <Button type="button" variant="outline" size="lg" className="w-full bg-transparent">
                      Cancel
                    </Button>
                  </Link>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
