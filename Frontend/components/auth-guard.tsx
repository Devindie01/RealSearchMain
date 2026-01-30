"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Loader2 } from "lucide-react"

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const [isAuthorized, setIsAuthorized] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem("realSearchToken")

    if (!token) {
      // 1. No token? Direct to login
      window.location.href = "/login"
      return
    }

    // 2. Check if token is expired
    try {
      const payload = JSON.parse(atob(token.split(".")[1])) // Decode JWT payload
      const isExpired = Date.now() >= payload.exp * 1000

      if (isExpired) {
        localStorage.removeItem("realSearchToken")
        window.location.href = "/login"
      } else {
        setIsAuthorized(true)
      }
    } catch (e) {
      // Invalid token format
      router.push("/login")
    }
  }, [router])

  if (!isAuthorized) {
    return (
      <div className="flex h-screen w-full items-center justify-center">
        <Loader2 className="h-10 w-10 animate-spin text-primary" />
      </div>
    )
  }

  return <>{children}</>
}