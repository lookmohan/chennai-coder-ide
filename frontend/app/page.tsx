import Link from "next/link";

import { Logo } from "@/components/layout/logo";
import { buttonClasses } from "@/components/ui/button";

export default function LandingPage() {
  return (
    <div className="flex min-h-dvh flex-col">
      <header className="mx-auto flex h-16 w-full max-w-5xl items-center justify-between px-4 md:px-8">
        <Logo />
        <nav aria-label="Account" className="flex items-center gap-2">
          <Link href="/login" className={buttonClasses({ variant: "ghost", size: "sm" })}>
            Log in
          </Link>
          <Link href="/register" className={buttonClasses({ size: "sm" })}>
            Sign up
          </Link>
        </nav>
      </header>

      <main id="main" className="mx-auto flex w-full max-w-5xl flex-1 flex-col justify-center px-4 py-16 md:px-8">
        <p className="text-sm font-medium text-primary">Learn. Code. Build.</p>
        <h1 className="mt-3 max-w-2xl text-4xl font-semibold tracking-tight md:text-5xl">
          A place to learn programming and practice until it clicks.
        </h1>
        <p className="mt-5 max-w-xl text-lg text-muted-foreground">
          Chennai Coder is a coding education platform: guided learning, hands-on practice problems, and a mentor that
          helps you think instead of handing you the answer.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link href="/register" className={buttonClasses({ size: "lg" })}>
            Create your account
          </Link>
          <Link href="/login" className={buttonClasses({ variant: "outline", size: "lg" })}>
            Log in
          </Link>
        </div>
        <p className="mt-6 text-sm text-muted-foreground">
          The platform is under active development. Accounts and profiles work today; practice problems and courses are
          coming next.
        </p>
      </main>

      <footer className="border-t border-border py-6 text-center text-sm text-muted-foreground">
        © {new Date().getFullYear()} Chennai Coder
      </footer>
    </div>
  );
}
