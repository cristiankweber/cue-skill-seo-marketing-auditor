# Schema Markup Reference

## Essential Schema Types for Websites

### Physician / MedicalBusiness
```json
{
  "@context": "https://schema.org",
  "@type": "Physician",
  "name": "Dr. Nome Completo",
  "description": "Especialidade e breve descrição",
  "url": "https://www.site.com.br",
  "image": "https://www.site.com.br/foto.jpg",
  "telephone": "+55-XX-XXXXX-XXXX",
  "email": "contato@site.com.br",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Rua Exemplo, 123",
    "addressLocality": "Cidade",
    "addressRegion": "RS",
    "postalCode": "00000-000",
    "addressCountry": "BR"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": -00.0000,
    "longitude": -00.0000
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "08:00",
      "closes": "18:00"
    }
  ],
  "medicalSpecialty": "Hematology",
  "priceRange": "$$",
  "sameAs": [
    "https://www.instagram.com/perfil",
    "https://www.linkedin.com/in/perfil"
  ]
}
```

### FAQPage
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Pergunta frequente?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Resposta completa aqui."
      }
    }
  ]
}
```

### BreadcrumbList
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Início", "item": "https://site.com.br/"},
    {"@type": "ListItem", "position": 2, "name": "Sobre", "item": "https://site.com.br/sobre"}
  ]
}
```

### Article / BlogPosting
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Título do Artigo",
  "author": {"@type": "Person", "name": "Dr. Nome"},
  "datePublished": "2025-01-15",
  "dateModified": "2025-01-20",
  "image": "https://site.com.br/imagem.jpg",
  "description": "Resumo do artigo em até 160 caracteres."
}
```

### LocalBusiness (agregado com reviews)
```json
{
  "@context": "https://schema.org",
  "@type": "MedicalBusiness",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "47",
    "bestRating": "5"
  }
}
```

## Validation Tools
- Google Rich Results Test: https://search.google.com/test/rich-results
- Schema.org Validator: https://validator.schema.org/
- Google Search Console: Rich results report
