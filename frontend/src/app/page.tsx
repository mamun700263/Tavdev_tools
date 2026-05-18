import Link from "next/link";

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-[#080808] text-white overflow-hidden">
      {/* Grid background */}
      <div
        className="fixed inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)`,
          backgroundSize: "64px 64px",
        }}
      />

      {/* Glow */}
      <div className="fixed top-[-20%] left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-emerald-500 opacity-[0.06] blur-[120px] pointer-events-none" />

      {/* Nav */}
      <nav className="relative z-10 flex justify-between items-center px-8 py-6 max-w-6xl mx-auto">
        <span className="text-sm font-mono font-bold tracking-widest text-white uppercase">
          TavDev
        </span>
        <div className="flex items-center gap-6">
          <Link
            href="/login"
            className="text-sm text-zinc-400 hover:text-white transition-colors"
          >
            Login
          </Link>
          <Link
            href="/register"
            className="text-sm bg-white text-black px-4 py-2 rounded-md font-medium hover:bg-zinc-200 transition-colors"
          >
            Get started
          </Link>
        </div>
      </nav>

      {/* Hero */}
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

      {/* Stats */}
      <section className="relative z-10 max-w-6xl mx-auto px-8 pb-32">
        <div className="grid grid-cols-3 gap-px bg-zinc-800 rounded-xl overflow-hidden border border-zinc-800">
          {[
            { value: "30s", label: "Fastest check interval" },
            { value: "99.9%", label: "Monitoring uptime" },
            { value: "< 1s", label: "Alert delivery time" },
          ].map((stat) => (
            <div key={stat.label} className="bg-[#0d0d0d] px-8 py-10">
              <p className="text-4xl font-black text-white mb-2 font-mono">
                {stat.value}
              </p>
              <p className="text-sm text-zinc-500">{stat.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="relative z-10 max-w-6xl mx-auto px-8 pb-32">
        <h2 className="text-3xl font-black tracking-tight mb-12 text-zinc-200">
          Everything you need to
          <br />
          stay ahead of downtime.
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            {
              icon: "⚡",
              title: "Instant monitoring",
              desc: "Check your sites every 30 seconds. Know about problems before your users do.",
            },
            {
              icon: "📊",
              title: "Response time tracking",
              desc: "Track latency trends over time. Spot performance degradation early.",
            },
            {
              icon: "🔒",
              title: "Secure accounts",
              desc: "Email verification, JWT auth, and rate limiting built in from day one.",
            },
          ].map((f) => (
            <div
              key={f.title}
              className="border border-zinc-800 rounded-xl p-6 bg-[#0d0d0d] hover:border-zinc-600 transition-colors"
            >
              <span className="text-2xl mb-4 block">{f.icon}</span>
              <h3 className="font-bold text-white mb-2">{f.title}</h3>
              <p className="text-sm text-zinc-500 leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="relative z-10 max-w-6xl mx-auto px-8 pb-32">
        <div className="border border-zinc-800 rounded-2xl p-12 text-center bg-[#0d0d0d] relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-emerald-500/5 to-transparent" />
          <h2 className="text-4xl font-black tracking-tight mb-4 relative z-10">
            Start monitoring in 60 seconds.
          </h2>
          <p className="text-zinc-400 mb-8 relative z-10">
            Free plan includes 10 monitors. No credit card required.
          </p>
          <Link
            href="/register"
            className="relative z-10 inline-block bg-white text-black px-8 py-3 rounded-md font-semibold text-sm hover:bg-zinc-200 transition-colors"
          >
            Create free account →
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 max-w-6xl mx-auto px-8 pb-8 flex justify-between items-center border-t border-zinc-800 pt-8">
        <span className="text-xs font-mono text-zinc-600 uppercase tracking-widest">
          TavDev Uptimer
        </span>
        <span className="text-xs text-zinc-600">
          Built for developers who care about reliability.
        </span>
      </footer>
    </main>
  );
}