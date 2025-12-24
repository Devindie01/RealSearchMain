import { Header } from "@/components/header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Phone, Mail, MapPin, Clock } from "lucide-react"

export default function ContactPage() {
  return (
    <div className="min-h-screen bg-background">
      <Header />

      {/* Hero Section */}
      <div className="bg-gradient-to-b from-primary/10 to-background py-12">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl font-bold mb-4">Contact Us</h1>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            Have questions? We'd love to hear from you. Get in touch with our team.
          </p>
        </div>
      </div>

      {/* Contact Details */}
      <div className="container mx-auto px-4 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Phone */}
          <Card className="border-primary/20">
            <CardHeader>
              <div className="flex items-center gap-3 mb-2">
                <Phone className="h-6 w-6 text-primary" />
                <CardTitle>Phone</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-primary font-semibold text-lg">+94 11 234 5678</p>
              <p className="text-muted-foreground text-sm mt-1">Available Monday - Friday</p>
            </CardContent>
          </Card>

          {/* Email */}
          <Card className="border-primary/20">
            <CardHeader>
              <div className="flex items-center gap-3 mb-2">
                <Mail className="h-6 w-6 text-primary" />
                <CardTitle>Email</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-primary font-semibold text-lg">info@realsearch.lk</p>
              <p className="text-muted-foreground text-sm mt-1">We reply within 24 hours</p>
            </CardContent>
          </Card>

          {/* Address */}
          <Card className="border-primary/20">
            <CardHeader>
              <div className="flex items-center gap-3 mb-2">
                <MapPin className="h-6 w-6 text-primary" />
                <CardTitle>Address</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-primary font-semibold text-lg">123 Real Estate Ave</p>
              <p className="text-muted-foreground text-sm mt-1">Colombo 03, Sri Lanka</p>
            </CardContent>
          </Card>

          {/* Hours */}
          <Card className="border-primary/20">
            <CardHeader>
              <div className="flex items-center gap-3 mb-2">
                <Clock className="h-6 w-6 text-primary" />
                <CardTitle>Hours</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-primary font-semibold text-lg">9 AM - 6 PM</p>
              <p className="text-muted-foreground text-sm mt-1">Mon - Fri (Closed Weekends)</p>
            </CardContent>
          </Card>
        </div>

        {/* Additional Info */}
        <div className="mt-16 max-w-3xl mx-auto">
          <Card className="border-primary/20">
            <CardHeader>
              <CardTitle>Get in Touch</CardTitle>
              <CardDescription>
                Whether you're a buyer, seller, or just have questions about our platform, we're here to help.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h3 className="font-semibold text-primary mb-2">For Buyer Assistance:</h3>
                <p className="text-muted-foreground">
                  Our buyer specialists can help you find your perfect property and guide you through the entire
                  purchase process.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-primary mb-2">For Seller Assistance:</h3>
                <p className="text-muted-foreground">
                  List your property with ease. Our sellers specialists will help you maximize your property's
                  visibility and reach qualified buyers.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-primary mb-2">For General Inquiries:</h3>
                <p className="text-muted-foreground">
                  Have a question about our platform? Contact us directly and we'll get back to you as soon as possible.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
