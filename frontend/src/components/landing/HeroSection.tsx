import Link from "next/link";
export default function HeroSection(){
    return (
      <section className="relative z-10 max-w-6xl mx-auto px-8 pt-24 pb-32">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 border border-zinc-800 rounded-full px-4 py-1.5 mb-8">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-xs text-zinc-400 font-mono">
            Real-time uptime monitoring
          </span>
        </div>

        <h1 className="text-6xl md:text-8xl font-black tracking-tighter leading-none mb-6">
          Know when
          <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">
            your site
          </span>
          <br />
          goes down.
        </h1>

        <p className="text-zinc-400 text-lg max-w-xl mb-10 leading-relaxed">
          TavDev monitors your websites and APIs every 30 seconds.
          Get instant alerts before your users notice anything is wrong.
        </p>

        <div className="flex items-center gap-4">
          <Link
            href="/register"
            className="bg-white text-black px-6 py-3 rounded-md font-semibold text-sm hover:bg-zinc-200 transition-colors"
          >
            Start monitoring free →
          </Link>
          <Link
            href="/login"
            className="text-zinc-400 text-sm hover:text-white transition-colors"
          >
            Already have an account?
          </Link>
        </div>
      </section>

    )
}