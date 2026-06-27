export default function FeatureSection(){
    return(
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
    )
}