"use client"

import { useState } from "react"
import Link from "next/link"
import { ChevronDown } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

const buyerAssistanceContent = [
  {
    section: "Buyer Guides",
    icon: "📚",
    items: [
      { title: "Step-by-Step Home Buying Guide", description: "Learn the complete process from start to finish" },
      { title: "First-Time Home Buyer Guide", description: "Essential tips and resources for first-time buyers" },
      { title: "How to Get Pre-Approved", description: "Understand the pre-approval process and requirements" },
      {
        title: "Understanding Property Taxes & Legal Checks",
        description: "Important legal considerations when buying",
      },
    ],
  },
  {
    section: "Financial Assistance",
    icon: "💰",
    items: [
      { title: "Loan & Mortgage Options", description: "Explore various mortgage products available" },
      { title: "EMI Estimation Tools", description: "Calculate your monthly payments easily" },
      { title: "Down Payment Planner", description: "Plan and save for your down payment" },
      { title: "Connection to Loan Officers / Banks", description: "Get connected with financial institutions" },
    ],
  },
  {
    section: "Legal Assistance",
    icon: "⚖️",
    items: [
      { title: "Title Verification Help", description: "Verify property titles and ownership" },
      { title: "Agreement Review", description: "Get legal agreements reviewed by experts" },
    ],
  },
]

export default function BuyerAssistance() {
  const [expandedSections, setExpandedSections] = useState<string[]>(["Buyer Guides"])

  const toggleSection = (section: string) => {
    setExpandedSections((prev) => (prev.includes(section) ? prev.filter((s) => s !== section) : [...prev, section]))
  }

  return (
    <main className="min-h-screen bg-background">
      {/* Header */}
      <section className="bg-primary text-primary-foreground py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold mb-4">Buyer Assistance Center</h1>
          <p className="text-xl opacity-90">Your complete guide to buying property in Sri Lanka</p>
        </div>
      </section>

      {/* Content */}
      <section className="container mx-auto px-4 py-16">
        <div className="grid gap-6 max-w-4xl mx-auto">
          {buyerAssistanceContent.map((section, idx) => (
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
          <h2 className="text-2xl font-bold mb-4">Ready to Find Your Dream Home?</h2>
          <p className="mb-6 text-lg opacity-90">Browse our listings and connect with sellers today</p>
          <Link href="/">
            <Button variant="secondary" size="lg">
              Start Browsing Properties
            </Button>
          </Link>
        </div>
      </section>
    </main>
  )
}
