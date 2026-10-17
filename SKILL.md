---
name: seo-marketing-auditor
description: "Auditor completo de SEO e marketing digital para sites profissionais. Use para: auditar meta tags (título, descrição, OG, Twitter Card), validar Schema markup (JSON-LD), analisar keywords e densidade, executar checklist de otimização on-page, diagnosticar problemas de indexação, e gerar relatórios com score e recomendações priorizadas. Ideal para sites médicos, profissionais liberais e negócios locais."
---

# SEO & Marketing Digital Auditor

## Workflow

### 1. Meta Tags Audit (automated)

Run the audit script on any URL or local HTML file:

```bash
python3 scripts/audit_meta_tags.py <url_or_file>
```

Options: append `--json` for structured output. Script checks: title (length, presence), meta description, keywords, canonical, Open Graph (title, desc, image, type), Twitter Card, viewport, charset, robots, headings (H1 count, H2s), image alt text, structured data, and language declaration. Outputs score/grade and categorized issues.

### 2. Schema Markup Validation

Read `references/schema-markup.md` for templates of:
- Physician / MedicalBusiness (with geo, hours, specialties)
- FAQPage (for rich snippets)
- BreadcrumbList
- BlogPosting / Article
- AggregateRating

Validate existing schema by extracting `<script type="application/ld+json">` blocks and checking against Schema.org spec. Use Google Rich Results Test URL for live validation.

### 3. Keyword Analysis

Read `references/keyword-analysis.md` for the framework:
1. Extract seed keywords from page content
2. Categorize by intent (transactional > commercial > informational)
3. Map primary + secondary keywords to each page
4. Check density (1-2% primary, 0.5-1% secondary)
5. Identify content gaps vs. competitors

### 4. On-Page Checklist

Read `references/onpage-checklist.md` for the full checklist covering:
- Title, description, URL structure
- Headings hierarchy and keyword placement
- Content quality and internal linking
- Images (alt, compression, lazy loading)
- Technical (canonical, OG, schema, performance)
- Local SEO (NAP, maps, service area)

### 5. Generate Report

Compile findings into a prioritized report:

```markdown
# SEO Audit Report — [Site Name]
## Score: XX/100 (Grade: X)
## Critical Issues (fix immediately)
## Warnings (improve when possible)
## Passed Checks
## Recommendations (prioritized by impact)
```

## Decision Tree

| User Request | Action |
|---|---|
| "Auditar SEO" or "verificar meta tags" | Run audit script → report |
| "Adicionar Schema" or "structured data" | Read schema-markup.md → implement |
| "Analisar keywords" or "palavras-chave" | Read keyword-analysis.md → analyze |
| "Checklist SEO" or "otimização on-page" | Read onpage-checklist.md → audit |
| "Relatório completo" | All 4 steps → consolidated report |

## Key Rules

- Title: 30-60 chars, keyword near start, brand at end
- Description: 50-160 chars, includes CTA, unique per page
- Single H1 per page containing primary keyword
- All images must have descriptive alt text
- Structured data (JSON-LD) on every page type
- Canonical URL always set
- Mobile-first: viewport meta, 48px tap targets, responsive
- Local SEO: NAP consistent, city in title, Google Maps embedded
- Internal links: 3-5 per page with descriptive anchor text
- Page speed: LCP < 3s, no render-blocking scripts
