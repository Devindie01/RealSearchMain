"use client"
import Link from "next/link"
import { Home, User } from "lucide-react"
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
} from "@/components/ui/navigation-menu"
import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { useRouter } from "next/navigation"
import { useState, useEffect } from "react"

const propertyCategories = [
  {
    name: "Lands",
    subcategories: ["Bareland", "Tea Land", "Paddy Land", "Coconut Land"],
  },
  {
    name: "Houses",
    subcategories: ["Single Story", "Two Story", "Luxury Homes", "Budget Homes"],
  },
  {
    name: "Apartments",
    subcategories: ["Studio", "1 Bedroom", "2 Bedroom", "3+ Bedroom"],
  },
  {
    name: "Villas",
    subcategories: ["Beach Villas", "Hill Country", "City Villas", "Luxury Villas"],
  },
  {
    name: "Commercial",
    subcategories: ["Office Space", "Retail", "Warehouse", "Mixed Use"],
  },
]

export function Header() {
  const router = useRouter()
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [userName, setUserName] = useState("")

  // useEffect(() => {
  //   if (typeof window !== "undefined") {
  //     const userData = localStorage.getItem("realSearchUser")
  //     if (userData) {
  //       const user = JSON.parse(userData)
  //       setIsLoggedIn(true)
  //       setUserName(user.fullName)
  //     }
  //   }
  // }, [])

  useEffect(() => {
  const userData = localStorage.getItem("realSearchUser");
  if (userData) {
    try {
      const user = JSON.parse(userData);
      // Use optional chaining (?.) to prevent crashes
      if (user && (user.fullName || user.full_name)) {
        setIsLoggedIn(true);
        setUserName(user.fullName || user.full_name);
      }
    } catch (e) {
      console.error("Failed to parse user data", e);
      localStorage.removeItem("realSearchUser"); // Clear corrupt data
    }
  }
}, []);

  const handleLogout = () => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("realSearchUser");
      localStorage.removeItem("realSearchToken");
      // localStorage.clear();
      setIsLoggedIn(false)
      setUserName("")
      router.push("/")
    }
  }

  return (
    <header className="bg-primary text-primary-foreground border-b border-primary/20 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 hover:opacity-90 transition-opacity">
            <Home className="h-7 w-7" />
            <span className="text-2xl font-bold">realSearch</span>
          </Link>

          {/* Navigation */}
          <NavigationMenu className="hidden md:flex">
            <NavigationMenuList className="gap-1">
              {/* Property Types Dropdown */}
              <NavigationMenuItem>
                <NavigationMenuTrigger className="bg-transparent hover:bg-primary-foreground/10 text-primary-foreground">
                  Property Types
                </NavigationMenuTrigger>
                <NavigationMenuContent>
                  <div className="grid grid-cols-2 gap-3 p-6 w-[600px]">
                    {propertyCategories.map((category) => (
                      <div key={category.name} className="space-y-2">
                        <h4 className="font-semibold text-sm text-primary">{category.name}</h4>
                        <ul className="space-y-1">
                          {category.subcategories.map((sub) => (
                            <li key={sub}>
                              <Link
                                href={`/?type=${category.name.toLowerCase()}&subtype=${sub.toLowerCase()}`}
                                className="block text-sm text-muted-foreground hover:text-foreground hover:bg-muted px-2 py-1 rounded transition-colors"
                              >
                                {sub}
                              </Link>
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </NavigationMenuContent>
              </NavigationMenuItem>

              {/* Buyer Assistance */}
              <NavigationMenuItem>
                <Link href="/buyer-assistance" legacyBehavior passHref>
                  <NavigationMenuLink className="inline-flex h-10 w-max items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-primary-foreground/10 focus:bg-primary-foreground/10 focus:outline-none disabled:pointer-events-none disabled:opacity-50">
                    Buyer Assistance
                  </NavigationMenuLink>
                </Link>
              </NavigationMenuItem>

              {/* Seller Assistance */}
              <NavigationMenuItem>
                <Link href="/seller-assistance" legacyBehavior passHref>
                  <NavigationMenuLink className="inline-flex h-10 w-max items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-primary-foreground/10 focus:bg-primary-foreground/10 focus:outline-none disabled:pointer-events-none disabled:opacity-50">
                    Seller Assistance
                  </NavigationMenuLink>
                </Link>
              </NavigationMenuItem>

              {/* List Your Property */}
              <NavigationMenuItem>
                <Link href="/sell" legacyBehavior passHref>
                  <NavigationMenuLink className="inline-flex h-10 w-max items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-primary-foreground/10 focus:bg-primary-foreground/10 focus:outline-none disabled:pointer-events-none disabled:opacity-50">
                    List Your Property
                  </NavigationMenuLink>
                </Link>
              </NavigationMenuItem>

              {/* Market Insights */}
              <NavigationMenuItem>
                <Link href="/market-insights" legacyBehavior passHref>
                  <NavigationMenuLink className="inline-flex h-10 w-max items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-primary-foreground/10 focus:bg-primary-foreground/10 focus:outline-none disabled:pointer-events-none disabled:opacity-50">
                    Market Insights
                  </NavigationMenuLink>
                </Link>
              </NavigationMenuItem>

              {/* Contact Us */}
              <NavigationMenuItem>
                <Link href="/contact" legacyBehavior passHref>
                  <NavigationMenuLink className="inline-flex h-10 w-max items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-primary-foreground/10 focus:bg-primary-foreground/10 focus:outline-none disabled:pointer-events-none disabled:opacity-50">
                    Contact Us
                  </NavigationMenuLink>
                </Link>
              </NavigationMenuItem>
            </NavigationMenuList>
          </NavigationMenu>

          {/* Profile Icon */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                className="rounded-full hover:bg-primary-foreground/10 text-primary-foreground"
              >
                <User className="h-5 w-5" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              {isLoggedIn ? (
                <>
                  <div className="px-2 py-1.5 text-sm font-semibold text-foreground">{userName}</div>
                  <div className="my-1 border-t border-primary/10"></div>
                  <DropdownMenuItem onClick={() => router.push("/saved-properties")}>Saved Properties</DropdownMenuItem>
                  <DropdownMenuItem onClick={() => router.push("/recently-viewed")}>Recently Viewed</DropdownMenuItem>
                  <DropdownMenuItem onClick={() => router.push("/account-settings")}>Account Settings</DropdownMenuItem>
                  <DropdownMenuItem onClick={() => router.push("/inquiries")}>Inquiries</DropdownMenuItem>
                  <div className="my-1 border-t border-primary/10"></div>
                  <DropdownMenuItem onClick={handleLogout} className="text-red-600">
                    Sign Out
                  </DropdownMenuItem>
                </>
              ) : (
                <>
                  <DropdownMenuItem onClick={() => router.push("/login")}>Sign In</DropdownMenuItem>
                  <DropdownMenuItem onClick={() => router.push("/signup")}>Create Account</DropdownMenuItem>
                </>
              )}
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  )
}
