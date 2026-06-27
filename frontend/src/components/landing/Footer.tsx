import { Link } from "lucide-react"

export default function Footer(){
    return(
    <footer className="relative z-10 max-w-6xl mx-auto px-8 pb-8 flex justify-between items-center border-t border-zinc-800 pt-8">
        <span className="text-xs font-mono text-zinc-600 uppercase tracking-widest">
          TavDev Uptimer
        </span>
        <span className="text-xs text-zinc-600">
          Built for developers who care about reliability.
        </span>
      </footer>
    )
}