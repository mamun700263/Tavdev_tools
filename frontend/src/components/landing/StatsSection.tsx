export default function StateSection(){
    return(
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
    )
}