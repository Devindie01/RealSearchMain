"use client"

import { useState } from "react"
import Link from "next/link"
import { ChevronDown } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Header } from "@/components/header"

const sellerAssistanceContent = [
  {
    section: "Seller Guides",
    icon: "🏠",
    items: [
      { title: "How to Sell Your Home", description: "Step-by-step guide to selling your property successfully" },
      { title: "Documentation Checklist", description: "Complete list of documents needed for selling" },
      { title: "Staging Tips", description: "Make your property more attractive to buyers" },
      { title: "Photography Tips", description: "Capture professional photos of your property" },
    ],
  },
  {
    section: "Pricing Assistance",
    icon: "💵",
    items: [
      { title: "Property Valuation Tool", description: "Get an accurate valuation of your property" },
      { title: "Free Property Price Estimate", description: "Instant price estimates based on market data" },
      { title: "Comparative Market Analysis (CMA)", description: "Compare your property with similar listings" },
      { title: "Local Price Trends", description: "Understanding local market trends and prices" },
    ],
  },
]

export default function SellerAssistance() {
  const [expandedSections, setExpandedSections] = useState<string[]>(["Seller Guides"])

  const toggleSection = (section: string) => {
    setExpandedSections((prev) => (prev.includes(section) ? prev.filter((s) => s !== section) : [...prev, section]))
  }

  return (
    <div className="min-h-screen bg-background">
      {/* 2. ADD THE HEADER HERE */}
      <Header />

    <main className="min-h-screen bg-background">
      {/* Header */}
      <section className="bg-primary text-primary-foreground py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold mb-4">Seller Assistance Center</h1>
          <p className="text-xl opacity-90">Everything you need to know to sell your property</p>
        </div>
      </section>

      {/* Content */}
      <section className="container mx-auto px-4 py-16">
        <div className="grid gap-6 max-w-4xl mx-auto">
          {sellerAssistanceContent.map((section, idx) => (
            <Card key={idx} className="overflow-hidden">
              <div
                className="flex items-center justify-between p-6 bg-secondary cursor-pointer hover:bg-secondary/80 transition-colors"
                onClick={() => toggleSection(section.section)}
              >
                <div className="flex items-center gap-4">
                  <span className="text-3xl">{section.icon}</span>
                  <h2 className="text-2xl font-bold text-primary">{section.section}</h2>
                </div>
                <ChevronDown
                  className={`h-6 w-6 text-primary transition-transform ${
                    expandedSections.includes(section.section) ? "rotate-180" : ""
                  }`}
                />
              </div>

              {expandedSections.includes(section.section) && (
                <CardContent className="pt-6">
                  <div className="grid gap-4">
                    {section.items.map((item, itemIdx) => (
                      <div
                        key={itemIdx}
                        className="p-4 border border-border rounded-lg hover:bg-secondary/30 transition-colors"
                      >
                        <h3 className="font-semibold text-lg text-primary mb-2">{item.title}</h3>
                        <p className="text-muted-foreground mb-3">{item.description}</p>
                        <Button variant="outline" size="sm">
                          Learn More
                        </Button>
                      </div>
                    ))}
                  </div>
                </CardContent>
              )}
            </Card>
          ))}
        </div>

        {/* CTA Section */}
        <div className="mt-16 bg-primary text-primary-foreground rounded-lg p-8 text-center max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold mb-4">Ready to Sell Your Property?</h2>
          <p className="mb-6 text-lg opacity-90">List your property today and reach thousands of buyers</p>
          <Link href="/sell">
            <Button variant="secondary" size="lg">
              List Your Property
            </Button>
          </Link>
        </div>
      </section>
    </main>
    </div>
  )
}
