import express from 'express'
import cors from 'cors'
import { computeRisk } from '@stroke/model'

const app = express()

app.use(express.json({ limit: '256kb' }))
app.use(
    cors({
        origin: [/^http:\/\/localhost:\d+$/],
    })
)

app.get('/api/health', (_req, res) => {
    res.json({ ok: true })
})

app.post('/api/scan', (req, res) => {
    const { profile, fast } = req.body || {}
    const result = computeRisk({ profile, fast })

    res.json({
        ...result,
        ts: new Date().toISOString(),
    })
})

const port = Number(process.env.PORT || 8080)
app.listen(port, () => {
    // eslint-disable-next-line no-console
    console.log(`Stroke server listening on http://localhost:${port}`)
})
