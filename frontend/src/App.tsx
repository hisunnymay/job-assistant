import { zhCN } from './content/zh-CN'
import './styles.css'

export function App() {
  return (
    <main className="app-shell">
      <section className="intro-card" aria-labelledby="app-title">
        <p className="eyebrow">{zhCN.eyebrow}</p>
        <h1 id="app-title">{zhCN.appName}</h1>
        <p className="introduction">{zhCN.introduction}</p>
        <p className="status" role="status">
          {zhCN.scaffoldStatus}
        </p>
      </section>
    </main>
  )
}
