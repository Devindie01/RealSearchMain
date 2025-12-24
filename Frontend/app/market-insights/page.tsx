"use client"

import { TrendingUp, TrendingDown, Home, MapPin } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"

const priceData = [
  { month: "Jan", houses: 8500000, apartments: 5200000, villas: 15000000 },
  { month: "Feb", houses: 8600000, apartments: 5300000, villas: 15200000 },
  { month: "Mar", houses: 8400000, apartments: 5100000, villas: 14900000 },
  { month: "Apr", houses: 8800000, apartments: 5500000, villas: 15500000 },
  { month: "May", houses: 9200000, apartments: 5800000, villas: 16000000 },
  { month: "Jun", houses: 9500000, apartments: 6000000, villas: 16300000 },
]

const demandData = [
  { area: "Colombo", demand: 85, supply: 45 },
  { area: "Kandy", demand: 72, supply: 38 },
  { area: "Galle", demand: 68, supply: 52 },
  { area: "Jaffna", demand: 55, supply: 30 },
  { area: "Matara", demand: 62, supply: 41 },
]

const marketTrends = [
  {
    title: "Overall Market Growth",
    value: "+12.5%",
    change: "up",
    description: "Property prices up from last year",
    icon: TrendingUp,
  },
  {
    title: "Apartment Demand",
    value: "+18.3%",
    change: "up",
    description: "Strong demand for urban properties",
    icon: TrendingUp,
  },
  {
    title: "Villa Market",
    value: "-3.2%",
    change: "down",
    description: "Slight slowdown in luxury segment",
    icon: TrendingDown,
  },
  {
    title: "New Listings",
    value: "+25.0%",
    change: "up",
    description: "More properties entering the market",
    icon: TrendingUp,
  },
]

export default function MarketInsights() {
  return (
    <main className="min-h-screen bg-background">
      {/* Header */}
      <section className="bg-primary text-primary-foreground py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold mb-4">Market Insights & Trends</h1>
          <p className="text-xl opacity-90">Stay updated with the latest real estate market trends in Sri Lanka</p>
        </div>
      </section>

      {/* Market Overview Cards */}
      <section className="container mx-auto px-4 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {marketTrends.map((trend, idx) => {
            const Icon = trend.icon
            return (
              <Card key={idx}>
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-sm font-medium text-muted-foreground">{trend.title}</CardTitle>
                    <Icon className={`h-5 w-5 ${trend.change === "up" ? "text-green-600" : "text-red-600"}`} />
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-primary mb-2">{trend.value}</div>
                  <p className="text-sm text-muted-foreground">{trend.description}</p>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* Price Trends Chart */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Price Trends by Property Type</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={priceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip formatter={(value) => `LKR ${(value / 1000000).toFixed(1)}M`} />
                  <Legend />
                  <Line type="monotone" dataKey="houses" stroke="#1a5f3f" name="Houses" strokeWidth={2} />
                  <Line type="monotone" dataKey="apartments" stroke="#2d8659" name="Apartments" strokeWidth={2} />
                  <Line type="monotone" dataKey="villas" stroke="#8fbc8f" name="Villas" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Demand vs Supply Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Demand vs Supply by Region</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={demandData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="area" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="demand" fill="#1a5f3f" name="Buyer Demand" />
                  <Bar dataKey="supply" fill="#e8f5e9" name="Available Supply" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Key Insights */}
        <div className="mt-16">
          <h2 className="text-3xl font-bold text-primary mb-8">Key Market Insights</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MapPin className="h-5 w-5 text-primary" />
                  Hottest Markets
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  <li className="flex justify-between items-center pb-3 border-b">
                    <span className="text-muted-foreground">Colombo</span>
                    <span className="font-bold text-primary">+15.2%</span>
                  </li>
                  <li className="flex justify-between items-center pb-3 border-b">
                    <span className="text-muted-foreground">Kandy</span>
                    <span className="font-bold text-primary">+12.8%</span>
                  </li>
                  <li className="flex justify-between items-center">
                    <span className="text-muted-foreground">Galle</span>
                    <span className="font-bold text-primary">+8.5%</span>
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Home className="h-5 w-5 text-primary" />
                  Most Searched Properties
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  <li className="flex justify-between items-center pb-3 border-b">
                    <span className="text-muted-foreground">2-Bedroom Apartments</span>
                    <span className="font-bold">32%</span>
                  </li>
                  <li className="flex justify-between items-center pb-3 border-b">
                    <span className="text-muted-foreground">Houses (Mid-range)</span>
                    <span className="font-bold">28%</span>
                  </li>
                  <li className="flex justify-between items-center">
                    <span className="text-muted-foreground">Villas (Luxury)</span>
                    <span className="font-bold">18%</span>
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
    </main>
  )
}
