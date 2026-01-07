export function computeRisk({ profile, fast }) {
    const age = Number(profile?.age ?? 0)
    const sys = Number(profile?.bpSystolic ?? 120)
    const dia = Number(profile?.bpDiastolic ?? 80)
    const diabetes = Boolean(profile?.diabetes)
    const smoking = Boolean(profile?.smoking)

    const fastScore =
        (fast?.faceDroop ? 1 : 0) +
        (fast?.armWeakness ? 1 : 0) +
        (fast?.speechDifficulty ? 1 : 0)

    let score = 0

    // Age
    if (age >= 65) score += 25
    else if (age >= 55) score += 18
    else if (age >= 45) score += 10

    // Blood pressure
    if (sys >= 160 || dia >= 100) score += 22
    else if (sys >= 140 || dia >= 90) score += 14
    else if (sys >= 130 || dia >= 85) score += 8

    // Conditions
    if (diabetes) score += 10
    if (smoking) score += 10

    // FAST symptoms (dominant)
    score += fastScore * 18

    score = Math.max(0, Math.min(100, score))

    let level = 'low'
    if (score >= 70) level = 'high'
    else if (score >= 40) level = 'medium'

    // Conservative confidence
    const confidence = Math.max(
        0.55,
        Math.min(0.92, 0.6 + fastScore * 0.12 + (age >= 55 ? 0.06 : 0))
    )

    return { score, level, confidence }
}

export function levelLabel(level) {
    if (level === 'high') return 'High'
    if (level === 'medium') return 'Medium'
    return 'Low'
}

export function levelColor(level) {
    if (level === 'high') return 'var(--risk-high-text)'
    if (level === 'medium') return 'var(--risk-med-text)'
    return 'var(--risk-low-text)'
}

export function levelFill(level) {
    if (level === 'high') return '#dc2626'
    if (level === 'medium') return '#f59e0b'
    return '#16a34a'
}
