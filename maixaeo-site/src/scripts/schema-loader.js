// Schema Loader for maixAEO.com
// Loads JSON-LD schema markup from separate files

async function loadSchema(schemaId, schemaPath) {
    try {
        const response = await fetch(schemaPath);
        const schema = await response.json();
        
        // Add @id if not present
        if (!schema['@id']) {
            schema['@id'] = `https://maixaeo.com/#${schemaId}`;
        }
        
        const script = document.getElementById(schemaId + '-schema');
        if (script) {
            script.textContent = JSON.stringify(schema, null, 2);
        }
    } catch (error) {
        console.error(`Error loading schema ${schemaId}:`, error);
    }
}

// Load all schemas on page load
document.addEventListener('DOMContentLoaded', function() {
    // Organization schema
    loadSchema('organization', '/schema/organization.json');
    
    // Website schema
    const websiteSchema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": "https://maixaeo.com/#website",
        "url": "https://maixaeo.com",
        "name": "maixAEO",
        "description": "Answer Engine Optimization (AEO) service - No Magic AEO Hacks. Just Technical Excellence That Works.",
        "publisher": {
            "@id": "https://maixaeo.com/#organization"
        }
    };
    document.getElementById('website-schema').textContent = JSON.stringify(websiteSchema, null, 2);
    
    // Service schema
    loadSchema('service', '/schema/service.json');
    
    // FAQ schema (dynamically generated from FAQ section)
    generateFAQSchema();
});

function generateFAQSchema() {
    const faqItems = document.querySelectorAll('.faq-item');
    const faqSchema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    };
    
    faqItems.forEach(item => {
        const question = item.querySelector('h3')?.textContent;
        const answer = item.querySelector('p')?.textContent;
        
        if (question && answer) {
            faqSchema.mainEntity.push({
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": answer
                }
            });
        }
    });
    
    if (faqSchema.mainEntity.length > 0) {
        document.getElementById('faq-schema').textContent = JSON.stringify(faqSchema, null, 2);
    }
}
