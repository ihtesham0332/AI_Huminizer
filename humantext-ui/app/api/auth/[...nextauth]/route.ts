import NextAuth from "next-auth"
import GoogleProvider from "next-auth/providers/google"

// In a real application, these credentials would be loaded from .env.local
const handler = NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_ID || "mock-client-id",
      clientSecret: process.env.GOOGLE_SECRET || "mock-client-secret",
    }),
  ],
  session: {
    strategy: "jwt",
  },
  callbacks: {
    async session({ session, token }) {
      // In production, you would attach the user's stripe subscription status here
      // by querying your PostgreSQL database using the token.sub (user id)
      session.user.id = token.sub;
      session.user.isPro = false; // Mock default
      return session;
    }
  }
})

export { handler as GET, handler as POST }
