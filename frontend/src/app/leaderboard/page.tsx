export default function LeaderboardPage() {
  const data = [
    { url: "https://google.com", score: 120 },
    { url: "https://github.com", score: 180 },
    { url: "https://api.tavdev.com", score: 95 },
  ];

  return (
    <main className="max-w-4xl mx-auto px-8 py-16 text-white">
      <h1 className="text-3xl font-bold mb-6">Leaderboard</h1>

      <p className="text-zinc-400 mb-8">
        Fastest APIs ranked by response time (lower is better)
      </p>

      <div className="space-y-3">
        {data.map((item, idx) => (
          <div
            key={item.url}
            className="flex justify-between items-center p-4 bg-[#111] border border-zinc-800 rounded-md"
          >
            <span className="text-zinc-300">
              #{idx + 1} {item.url}
            </span>

            <span className="font-mono text-white">
              {item.score}ms
            </span>
          </div>
        ))}
      </div>
    </main>
  );
}