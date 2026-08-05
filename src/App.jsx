import { useEffect, useState } from 'react'
import Papa from 'papaparse'

const PRIMARY_CSV_FILE = 'platonic_ideal.csv'
const SITE_NAME = 'Platonic Ideal'
const SITE_URL = 'https://laurent1056.github.io/my-platonic-app/'
const DEFAULT_DESCRIPTION =
  'One product per category, or empty. A catalog of durable, rebuildable product declarations.'
const IDENTITY_HEADERS = new Set([
  'Number',
  'Category',
  'Status',
  'Model',
  'Price',
  'Last Reviewed',
  'Image URL',
  'Slug',
])
const PRIMARY_REVIEW_HEADERS = [
  'Form Definition',
  'Form Statement',
  'Card Snippet (Why this ends the search)',
  'Core Reasoning',
  'Key Disqualifiers',
  'Maintenance / Replacement Cycle',
  'Permanence Mechanism',
  'Alternates (non-declared)',
  'Admission Test',
  'Failure Modes',
  'Notes',
]

function normalizeSpaces(text) {
  return String(text || '')
    .replace(/\s+/g, ' ')
    .trim()
}

function summarizeText(text, maxLength = 160) {
  const normalized = normalizeSpaces(text)
  if (!normalized) return ''
  if (normalized.length <= maxLength) return normalized
  const shortened = normalized.slice(0, maxLength - 1)
  const boundary = shortened.lastIndexOf(' ')
  return `${(boundary > 100 ? shortened.slice(0, boundary) : shortened).trim()}…`
}

function buildMetadata({ view, category, totalCategories }) {
  if (category) {
    return {
      title:
        category.status === 'EMPTY'
          ? `${category.category} (Empty) | ${SITE_NAME}`
          : `${category.model || category.category} | ${category.category} | ${SITE_NAME}`,
      description: summarizeText(
        category.oneLiner ||
          category.coreReasoning ||
          category.whyNotOthers ||
          `${category.category} is currently ${category.status.toLowerCase()}.`
      ),
      canonical: SITE_URL,
      url: SITE_URL,
    }
  }

  if (view === 'index') {
    return {
      title: `The Index | ${SITE_NAME}`,
      description: `Browse ${totalCategories} categories that resolve to one declaration or an empty verdict.`,
      canonical: SITE_URL,
      url: SITE_URL,
    }
  }

  if (view === 'methodology') {
    return {
      title: `Methodology | ${SITE_NAME}`,
      description:
        'The rules behind Platonic Ideal: one declaration per category, repairability bias, and honest empty verdicts.',
      canonical: SITE_URL,
      url: SITE_URL,
    }
  }

  if (view === 'oracle') {
    return {
      title: `Oracle | ${SITE_NAME}`,
      description:
        'Use the Oracle to draft category declarations while keeping the CSV as the final source of truth.',
      canonical: SITE_URL,
      url: SITE_URL,
    }
  }

  return {
    title: SITE_NAME,
    description: DEFAULT_DESCRIPTION,
    canonical: SITE_URL,
    url: SITE_URL,
  }
}

function upsertMeta(selector, attrName, attrValue, content) {
  let element = document.head.querySelector(selector)
  if (!element) {
    element = document.createElement('meta')
    element.setAttribute(attrName, attrValue)
    document.head.appendChild(element)
  }
  element.setAttribute('content', content)
}

function setDocumentMetadata(metadata) {
  if (typeof document === 'undefined') return

  document.title = metadata.title
  upsertMeta('meta[name="description"]', 'name', 'description', metadata.description)
  upsertMeta('meta[property="og:title"]', 'property', 'og:title', metadata.title)
  upsertMeta('meta[property="og:description"]', 'property', 'og:description', metadata.description)
  upsertMeta('meta[property="og:url"]', 'property', 'og:url', metadata.url)
  upsertMeta('meta[name="twitter:title"]', 'name', 'twitter:title', metadata.title)
  upsertMeta(
    'meta[name="twitter:description"]',
    'name',
    'twitter:description',
    metadata.description
  )

  let canonical = document.head.querySelector('link[rel="canonical"]')
  if (!canonical) {
    canonical = document.createElement('link')
    canonical.setAttribute('rel', 'canonical')
    document.head.appendChild(canonical)
  }
  canonical.setAttribute('href', metadata.canonical)
}

function getBaseUrl() {
  return import.meta.env.BASE_URL || './'
}

function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/--+/g, '-')
    .trim()
}

function formatPrice(price) {
  if (!price) return null
  return price.trim()
}

const FALLBACK_DATA = [
  {
    slug: 'frying-pan',
    category: 'Frying Pan',
    status: 'DECLARED',
    model: 'Lodge 12" Cast Iron Skillet (L10SK3)',
    price: '$30-40',
    oneLiner: 'Gets better with use, infinitely repairable, unchanged since 1896',
    coreReasoning:
      'Cast iron with proper thickness holds heat, resists temperature drops. No coatings to fail. Seasoning improves over time.',
    whyNotOthers:
      'Teflon dies in 3 years. Stainless never improves. Expensive cast iron is same iron at 5x price.',
    evidence:
      'Made since 1896 with same specs. Used globally in professional and home kitchens.',
    failureModes: 'Rust (repairable with re-seasoning). Cracks from thermal shock (rare, repairable).',
    caveats: 'Heavy. Requires seasoning maintenance. Not dishwasher safe.',
    whereToAcquire: 'https://www.lodgecastiron.com',
    lastReviewed: '2026-01-16',
    images: [],
  },
]

function StatusBadge({ status }) {
  const isDeclared = status === 'DECLARED'

  return (
    <span
      className={`inline-block px-3 py-1 text-xs uppercase tracking-wider font-medium border ${
        isDeclared
          ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
          : 'bg-amber-50 text-amber-700 border-amber-200'
      }`}
    >
      {status}
    </span>
  )
}

function CategoryCard({ category, onClick }) {
  return (
    <button
      onClick={onClick}
      className="w-full text-left p-6 border border-stone-200 bg-white hover:border-stone-300 hover:shadow-sm transition-all"
    >
      <div className="flex items-start justify-between gap-4 mb-2">
        <h3 className="text-lg font-serif text-stone-900">{category.category}</h3>
        <StatusBadge status={category.status} />
      </div>

      {category.status === 'DECLARED' && category.model && (
        <p className="text-sm text-stone-600 mb-1">{category.model}</p>
      )}

      {category.price && <p className="text-xs text-stone-500">{category.price}</p>}

      {category.oneLiner && (
        <p className="text-sm text-stone-700 mt-3 line-clamp-2">{category.oneLiner}</p>
      )}
    </button>
  )
}

function SectionCard({ title, children, className = '' }) {
  return (
    <div className={`border border-stone-200 bg-white p-5 ${className}`}>
      <h3 className="text-xs uppercase tracking-widest text-stone-500 mb-3 font-medium">
        {title}
      </h3>
      <div className="text-sm leading-6 text-stone-700 whitespace-pre-wrap">{children}</div>
    </div>
  )
}

function FieldList({ fields }) {
  if (!fields || fields.length === 0) {
    return null
  }

  return (
    <div className="space-y-4">
      {fields.map((field) => (
        <div key={field.label}>
          <h4 className="text-[11px] uppercase tracking-widest text-stone-500 mb-1">{field.label}</h4>
          <div className="text-sm leading-6 text-stone-700 whitespace-pre-wrap">{field.value}</div>
        </div>
      ))}
    </div>
  )
}

function HomeView({ onNavigate, categories }) {
  const [search, setSearch] = useState('')

  const declaredCount = categories.filter((category) => category.status === 'DECLARED').length
  const emptyCount = categories.filter((category) => category.status === 'EMPTY').length

  const filteredCategories = categories
    .filter(
      (category) =>
        category.category.toLowerCase().includes(search.toLowerCase()) ||
        (category.model && category.model.toLowerCase().includes(search.toLowerCase()))
    )
    .slice(0, 12)

  return (
    <div className="max-w-5xl mx-auto px-6 py-16">
      <div className="text-center mb-16">
        <h1 className="text-6xl md:text-7xl font-serif text-stone-900 mb-4">Platonic Ideal</h1>
        <p className="text-xl md:text-2xl text-stone-600 max-w-2xl mx-auto leading-relaxed">
          One product per category, or empty. <br />
          Ending searches, not facilitating them.
        </p>
      </div>

      <div className="flex justify-center gap-12 mb-12 text-center">
        <div>
          <div className="text-3xl font-serif text-stone-900">{declaredCount}</div>
          <div className="text-sm uppercase tracking-wider text-stone-500">Declared</div>
        </div>
        <div>
          <div className="text-3xl font-serif text-stone-900">{emptyCount}</div>
          <div className="text-sm uppercase tracking-wider text-stone-500">Empty</div>
        </div>
        <div>
          <div className="text-3xl font-serif text-stone-900">{categories.length}</div>
          <div className="text-sm uppercase tracking-wider text-stone-500">Total</div>
        </div>
      </div>

      <div className="mb-12">
        <input
          type="text"
          placeholder="Search categories or products..."
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          className="w-full px-6 py-4 border border-stone-300 bg-white text-lg focus:outline-none focus:border-stone-400"
        />
      </div>

      <div className="grid gap-4 md:grid-cols-2 mb-12">
        {filteredCategories.map((category) => (
          <CategoryCard
            key={category.slug}
            category={category}
            onClick={() => onNavigate('category', category.slug)}
          />
        ))}
      </div>

      <div className="text-center">
        <button
          onClick={() => onNavigate('index')}
          className="px-8 py-3 border-2 border-stone-900 bg-stone-900 text-white hover:bg-stone-800 transition-colors text-sm uppercase tracking-wider font-medium"
        >
          View Complete Index
        </button>
      </div>
    </div>
  )
}

function IndexView({ onNavigate, categories }) {
  const [search, setSearch] = useState('')
  const [filterStatus, setFilterStatus] = useState('ALL')
  const [sortBy, setSortBy] = useState('category')

  let filteredCategories = categories.filter((category) => {
    const matchesSearch =
      category.category.toLowerCase().includes(search.toLowerCase()) ||
      (category.model && category.model.toLowerCase().includes(search.toLowerCase()))

    const matchesFilter = filterStatus === 'ALL' || category.status === filterStatus

    return matchesSearch && matchesFilter
  })

  if (sortBy === 'category') {
    filteredCategories = [...filteredCategories].sort((a, b) => a.category.localeCompare(b.category))
  } else if (sortBy === 'status') {
    filteredCategories = [...filteredCategories].sort((a, b) => {
      if (a.status === 'DECLARED' && b.status === 'EMPTY') return -1
      if (a.status === 'EMPTY' && b.status === 'DECLARED') return 1
      return a.category.localeCompare(b.category)
    })
  }

  return (
    <div className="max-w-5xl mx-auto px-6 py-12">
      <h1 className="text-5xl md:text-6xl font-serif text-stone-900 mb-8">The Index</h1>

      <p className="text-lg text-stone-600 mb-12 max-w-3xl">
        Every category resolves to exactly one product declaration or an empty verdict. No
        shortlists. No hedging.
      </p>

      <div className="grid md:grid-cols-3 gap-4 mb-8">
        <input
          type="text"
          placeholder="Search..."
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          className="px-4 py-3 border border-stone-300 bg-white focus:outline-none focus:border-stone-400"
        />

        <select
          value={filterStatus}
          onChange={(event) => setFilterStatus(event.target.value)}
          className="px-4 py-3 border border-stone-300 bg-white focus:outline-none focus:border-stone-400"
        >
          <option value="ALL">All Categories</option>
          <option value="DECLARED">Declared Only</option>
          <option value="EMPTY">Empty Only</option>
        </select>

        <select
          value={sortBy}
          onChange={(event) => setSortBy(event.target.value)}
          className="px-4 py-3 border border-stone-300 bg-white focus:outline-none focus:border-stone-400"
        >
          <option value="category">Sort: Alphabetical</option>
          <option value="status">Sort: Declared First</option>
        </select>
      </div>

      <p className="text-sm text-stone-500 mb-4">
        Showing {filteredCategories.length} of {categories.length} categories
      </p>

      <div className="grid gap-3">
        {filteredCategories.map((category) => (
          <CategoryCard
            key={category.slug}
            category={category}
            onClick={() => onNavigate('category', category.slug)}
          />
        ))}
      </div>

      {filteredCategories.length === 0 && (
        <div className="text-center py-16">
          <p className="text-stone-500">No categories match your search.</p>
        </div>
      )}
    </div>
  )
}

function CategoryView({ onNavigate, category }) {
  if (!category) {
    return (
      <div className="max-w-5xl mx-auto px-6 py-12">
        <p className="text-stone-600">Category not found.</p>
        <button
          onClick={() => onNavigate('index')}
          className="mt-4 text-stone-600 hover:text-stone-900 underline"
        >
          ← Back to Index
        </button>
      </div>
    )
  }

  const isEmpty = category.status === 'EMPTY'

  return (
    <div className="max-w-7xl mx-auto px-6 py-12">
      <button
        onClick={() => onNavigate('index')}
        className="text-sm text-stone-600 hover:text-stone-900 mb-8 inline-flex items-center"
      >
        ← Back to Index
      </button>

      <div className="grid md:grid-cols-12 gap-8">
        <div className="md:col-span-8">
          <div className="mb-8">
            <p className="text-xs uppercase tracking-widest text-stone-500 mb-3">{category.category}</p>
            <StatusBadge status={category.status} />
          </div>

          {!isEmpty && category.model && (
            <>
              <h1 className="text-5xl md:text-6xl font-serif text-stone-900 mb-4">{category.model}</h1>
              {category.price && <p className="text-xl text-stone-600 mb-6">{category.price}</p>}
            </>
          )}

          {isEmpty && (
            <h1 className="text-5xl md:text-6xl font-serif text-stone-900 mb-6">{category.category}</h1>
          )}

          {category.oneLiner && (
            <p className="text-lg md:text-xl text-stone-700 leading-relaxed mb-12 border-l-4 border-stone-300 pl-6">
              {category.oneLiner}
            </p>
          )}

          {category.coreReasoning && (
            <section className="mb-12">
              <h2 className="text-xs uppercase tracking-widest text-stone-500 mb-4 font-medium">
                {isEmpty ? 'Why Empty' : 'Why This'}
              </h2>
              <div className="prose-custom text-base md:text-lg whitespace-pre-wrap">
                {category.coreReasoning}
              </div>
            </section>
          )}

          {!isEmpty && category.whyNotOthers && (
            <section className="mb-12">
              <h2 className="text-xs uppercase tracking-widest text-stone-500 mb-4 font-medium">
                Why Not Others
              </h2>
              <div className="prose-custom text-base whitespace-pre-wrap">{category.whyNotOthers}</div>
            </section>
          )}

          {category.evidence && (
            <section className="mb-12">
              <h2 className="text-xs uppercase tracking-widest text-stone-500 mb-4 font-medium">
                Evidence
              </h2>
              <div className="prose-custom text-base whitespace-pre-wrap">{category.evidence}</div>
            </section>
          )}
        </div>

        <div className="md:col-span-4 space-y-4">
          {category.failureModes && <SectionCard title="Failure Modes">{category.failureModes}</SectionCard>}
          {category.caveats && <SectionCard title="Caveats">{category.caveats}</SectionCard>}
          {category.whereToAcquire && (
            <SectionCard title="Where to Acquire">
              <a
                href={category.whereToAcquire}
                target="_blank"
                rel="noopener noreferrer"
                className="text-stone-700 hover:text-stone-900 underline break-words"
              >
                {category.whereToAcquire}
              </a>
            </SectionCard>
          )}
          {category.lastReviewed && <SectionCard title="Last Reviewed">{category.lastReviewed}</SectionCard>}
          {category.permanenceMechanism && (
            <SectionCard title="Permanence Mechanism">{category.permanenceMechanism}</SectionCard>
          )}
          {category.reviewFields && category.reviewFields.length > 0 && (
            <SectionCard title="Source Fields">
              <FieldList fields={category.reviewFields} />
            </SectionCard>
          )}
        </div>
      </div>

      {category.images && category.images.length > 0 && (
        <div className="mt-12 grid md:grid-cols-2 gap-4">
          {category.images.map((url, index) => (
            <div key={index} className="border border-stone-200 p-2 bg-white">
              <img src={url} alt={`${category.category} ${index + 1}`} className="w-full h-auto" />
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function MethodologyView() {
  return (
    <div className="max-w-3xl mx-auto px-6 py-12">
      <h1 className="text-5xl md:text-6xl font-serif text-stone-900 mb-8">Methodology</h1>

      <div className="prose-custom space-y-8">
        <section>
          <h2>The Core Rule</h2>
          <p>Every category resolves to exactly one of two outcomes:</p>
          <ul className="list-disc ml-6 space-y-2">
            <li>
              <strong>DECLARED:</strong> One specific product that best embodies the Form
            </li>
            <li>
              <strong>EMPTY:</strong> No product currently qualifies
            </li>
          </ul>
          <p>No shortlists. No "it depends." No hedging with subcategories to avoid hard choices.</p>
        </section>

        <section>
          <h2>What Is the Form?</h2>
          <p>
            The Form is the ideal expression of a product&apos;s function. It&apos;s what the product
            is trying to be when stripped of marketing, aesthetics, and brand positioning.
          </p>
          <p>
            A frying pan&apos;s Form: deliver even heat while allowing food to move freely. A
            hammer&apos;s Form: transfer kinetic energy to a fastener without breaking.
          </p>
          <p>If we can&apos;t state the Form in one sentence, the category isn&apos;t ready for declaration.</p>
        </section>

        <section>
          <h2>What Makes a Product Platonic?</h2>
          <p>A Platonic product:</p>
          <ul className="list-disc ml-6 space-y-2">
            <li>
              <strong>Ends the search</strong> - owning it makes further shopping unnecessary
            </li>
            <li>
              <strong>Improves or stays whole</strong> - performance doesn&apos;t degrade through ordinary use
            </li>
            <li>
              <strong>Is rebuildable</strong> - failure modes are reversible through repair
            </li>
            <li>
              <strong>Stays stable</strong> - the model doesn&apos;t drift year-to-year
            </li>
            <li>
              <strong>Is honest</strong> - no engineered obsolescence or fragile complexity
            </li>
            <li>
              <strong>Is supported</strong> - parts, service, and knowledge are accessible
            </li>
          </ul>
        </section>

        <section>
          <h2>Evidence Requirements</h2>
          <p>Declarations must be supported by verifiable evidence:</p>
          <ul className="list-disc ml-6 space-y-2">
            <li>Manufacturer warranty and support clarity</li>
            <li>Parts availability or documented service ecosystem</li>
            <li>Construction facts (materials, thickness, rebuildability)</li>
            <li>Known failure modes with documented fixes</li>
            <li>Production stability proof (same specs over years)</li>
          </ul>
          <p>We need at least three of these to declare with confidence.</p>
        </section>

        <section>
          <h2>Disqualifiers</h2>
          <p>Any one of these immediately disqualifies a product:</p>
          <ul className="list-disc ml-6 space-y-2">
            <li>Countdown timer surfaces (non-stick coatings, bonded finishes)</li>
            <li>Sealed-for-life design (no parts, no service, proprietary tools)</li>
            <li>Complexity without recoverability (electronics that brick the object)</li>
            <li>Silent model drift (same name, cheaper internals)</li>
            <li>Weak link dependency (one critical component fails and can&apos;t be replaced)</li>
          </ul>
        </section>

        <section>
          <h2>When Categories Are Empty</h2>
          <p>A category becomes EMPTY when:</p>
          <ul className="list-disc ml-6 space-y-2">
            <li>The market is fundamentally compromised (all products are disposable or sealed)</li>
            <li>No product meets our evidence standard</li>
            <li>The Form is still undefined (mixing incompatible sub-categories)</li>
            <li>The ideal exists but isn&apos;t currently available for purchase</li>
          </ul>
          <p>
            <strong>Empty is integrity, not failure.</strong> Declaring empty prevents readers from
            wasting money on products that don&apos;t meet the standard.
          </p>
        </section>

        <section>
          <h2>This Is Not Consumer Advice</h2>
          <p>
            These are declarations, not recommendations. We identify the product that most closely
            embodies the Form based on verifiable evidence. Whether it&apos;s right for your specific
            use case is a decision only you can make.
          </p>
        </section>
      </div>
    </div>
  )
}

function OracleView() {
  const [apiKey, setApiKey] = useState(() => localStorage.getItem('PI_ORACLE_KEY') || '')
  const [prompt, setPrompt] = useState('')
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSaveKey = () => {
    localStorage.setItem('PI_ORACLE_KEY', apiKey)
    setError('')
    alert('API key saved!')
  }

  const handleSubmit = async () => {
    if (!apiKey) {
      setError('Please enter an API key first')
      return
    }

    if (!prompt.trim()) {
      setError('Please enter a prompt')
      return
    }

    setLoading(true)
    setError('')
    setResponse('')

    try {
      const result = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01',
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-20250514',
          max_tokens: 4000,
          messages: [
            {
              role: 'user',
              content: `You are helping to draft content for the Platonic Ideal product catalog. Each category must declare ONE product or be marked EMPTY.

${prompt}

Please provide a draft response following the Platonic framework:
- If declaring a product: include Model, One-liner, Core Reasoning, Why Not Others, Evidence, Failure Modes, Caveats
- If declaring empty: explain specifically why no product qualifies
- Keep Core Reasoning under 600 words
- Be decisive, not diplomatic`,
            },
          ],
        }),
      })

      if (!result.ok) {
        throw new Error(`API request failed: ${result.status}`)
      }

      const data = await result.json()
      const text = data.content
        .filter((block) => block.type === 'text')
        .map((block) => block.text)
        .join('\n')

      setResponse(text)
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-6 py-12">
      <h1 className="text-5xl md:text-6xl font-serif text-stone-900 mb-8">Oracle</h1>

      <p className="text-lg text-stone-600 mb-8 max-w-3xl">
        AI-assisted drafting tool for category declarations. Use this to generate first drafts, not
        final verdicts.
      </p>

      <div className="mb-6 p-4 border border-amber-200 bg-amber-50">
        <p className="text-sm text-amber-800">
          API key is stored locally in your browser. Always verify Oracle output before publishing.
        </p>
      </div>

      <div className="mb-8">
        <label className="block text-sm uppercase tracking-wider text-stone-600 mb-2">Anthropic API Key</label>
        <div className="flex gap-3">
          <input
            type="password"
            value={apiKey}
            onChange={(event) => setApiKey(event.target.value)}
            placeholder="sk-ant-..."
            className="flex-1 px-4 py-3 border border-stone-300 bg-white focus:outline-none focus:border-stone-400"
          />
          <button
            onClick={handleSaveKey}
            className="px-6 py-3 border border-stone-900 bg-stone-900 text-white hover:bg-stone-800 transition-colors text-sm uppercase tracking-wider font-medium"
          >
            Save Key
          </button>
        </div>
      </div>

      <div className="mb-8">
        <label className="block text-sm uppercase tracking-wider text-stone-600 mb-2">Prompt</label>
        <textarea
          value={prompt}
          onChange={(event) => setPrompt(event.target.value)}
          placeholder="Example: Declare the platonic ideal for mechanical pencil..."
          rows={8}
          className="w-full px-4 py-3 border border-stone-300 bg-white focus:outline-none focus:border-stone-400 resize-vertical"
        />
      </div>

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="px-8 py-3 border-2 border-stone-900 bg-stone-900 text-white hover:bg-stone-800 disabled:bg-stone-400 disabled:border-stone-400 transition-colors text-sm uppercase tracking-wider font-medium"
      >
        {loading ? 'Generating...' : 'Generate Draft'}
      </button>

      {error && <div className="mt-8 p-4 border border-red-200 bg-red-50 text-red-800 text-sm">{error}</div>}

      {response && (
        <div className="mt-8 border border-stone-200 bg-white p-6">
          <h2 className="text-xs uppercase tracking-widest text-stone-500 mb-4 font-medium">Draft Output</h2>
          <div className="prose-custom whitespace-pre-wrap">{response}</div>
        </div>
      )}
    </div>
  )
}

function App() {
  const [view, setView] = useState('home')
  const [selectedSlug, setSelectedSlug] = useState(null)
  const [categories, setCategories] = useState(FALLBACK_DATA)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadCsv = async () => {
      try {
        const csvUrl = `${getBaseUrl()}${PRIMARY_CSV_FILE}`
        const response = await fetch(csvUrl, { cache: 'no-store' })

        if (!response.ok) {
          throw new Error(`Failed to load CSV: ${response.status}`)
        }

        const csvText = await response.text()

        Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
          complete: (results) => {
            const headers = results.meta.fields || []
            const parsed = results.data.map((row) => {
              const slug = row.Slug || slugify(row.Category || '')
              const coreReasoning =
                row.Core_Reasoning || row['Core Reasoning'] || row.core_reasoning || ''
              const keyDisqualifiers =
                row.Key_Disqualifiers || row['Key Disqualifiers'] || row.key_disqualifiers || ''
              const imageFields = [row['Image URL']]
              const reviewFields = headers
                .filter(
                  (header) =>
                    !IDENTITY_HEADERS.has(header) &&
                    row[header] &&
                    String(row[header]).trim()
                )
                .sort((left, right) => {
                  const leftIndex = PRIMARY_REVIEW_HEADERS.indexOf(left)
                  const rightIndex = PRIMARY_REVIEW_HEADERS.indexOf(right)
                  if (leftIndex === -1 && rightIndex === -1) return left.localeCompare(right)
                  if (leftIndex === -1) return 1
                  if (rightIndex === -1) return -1
                  return leftIndex - rightIndex
                })
                .map((header) => ({
                  label: header,
                  value: String(row[header]).trim(),
                }))

              return {
                slug,
                category: row.Category || '',
                status: (row.Status || '').toUpperCase(),
                model: row.Model || '',
                price: formatPrice(row.Price),
                oneLiner:
                  row.One_Liner ||
                  row['Card Snippet (Why this ends the search)'] ||
                  row['Form Statement'] ||
                  '',
                coreReasoning: coreReasoning.trim(),
                whyNotOthers: keyDisqualifiers.trim(),
                evidence: row.Evidence || row['Admission Test'] || '',
                failureModes: row.Failure_Modes || row['Failure Modes'] || '',
                caveats: row.Caveats || row.Notes || '',
                whereToAcquire: row.Where_to_acquire || row['Where to Acquire'] || '',
                lastReviewed: row.Last_Reviewed || row['Last Reviewed'] || '',
                permanenceMechanism:
                  row.Permanence_Mechanism || row['Permanence Mechanism'] || row['Maintenance / Replacement Cycle'] || '',
                images: imageFields.filter(Boolean),
                reviewFields,
              }
            })

            setCategories(parsed.length > 0 ? parsed : FALLBACK_DATA)
            setLoading(false)
          },
          error: () => {
            setCategories(FALLBACK_DATA)
            setLoading(false)
          },
        })
      } catch {
        setCategories(FALLBACK_DATA)
        setLoading(false)
      }
    }

    loadCsv()
  }, [])

  const handleNavigate = (newView, slug = null) => {
    setView(newView)
    setSelectedSlug(slug)
    window.scrollTo(0, 0)
  }

  const currentCategory = selectedSlug ? categories.find((category) => category.slug === selectedSlug) : null

  useEffect(() => {
    if (loading) return

    setDocumentMetadata(
      buildMetadata({
        view,
        category: view === 'category' ? currentCategory : null,
        totalCategories: categories.length,
      })
    )
  }, [categories.length, currentCategory, loading, view])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-stone-600">Loading...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      <header className="border-b border-stone-200 bg-white sticky top-0 z-50">
        <nav className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <button onClick={() => handleNavigate('home')} className="text-2xl font-serif text-stone-900 hover:text-stone-700">
            Platonic Ideal
          </button>

          <div className="flex gap-8 items-center">
            <button onClick={() => handleNavigate('index')} className="text-sm uppercase tracking-wider text-stone-600 hover:text-stone-900">
              Index
            </button>
            <button onClick={() => handleNavigate('methodology')} className="text-sm uppercase tracking-wider text-stone-600 hover:text-stone-900">
              Methodology
            </button>
            <button onClick={() => handleNavigate('oracle')} className="text-sm uppercase tracking-wider text-stone-600 hover:text-stone-900">
              Oracle
            </button>
          </div>
        </nav>
      </header>

      <main>
        {view === 'home' && <HomeView onNavigate={handleNavigate} categories={categories} />}
        {view === 'index' && <IndexView onNavigate={handleNavigate} categories={categories} />}
        {view === 'category' && <CategoryView onNavigate={handleNavigate} category={currentCategory} />}
        {view === 'methodology' && <MethodologyView />}
        {view === 'oracle' && <OracleView />}
      </main>

      <footer className="border-t border-stone-200 bg-white mt-16">
        <div className="max-w-7xl mx-auto px-6 py-8 text-center text-sm text-stone-500">
          <p>
            Platonic Ideal · One product per category, or empty · {categories.length} categories
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
