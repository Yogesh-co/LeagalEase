type Props = { title: string; content: string };

function clean(line: string) {
  return line.trim().replace(/^#{1,6}\s+/, '').replace(/\*\*/g, '').replace(/__/g, '');
}

function isHeading(line: string) {
  return line.length < 100 && (
    /^\d+(?:\.\d+)*[.)]?\s+\S/.test(line) ||
    /^(?:section|article|clause)\s+[\w.-]+\b/i.test(line) ||
    /^[A-Z][A-Z\s&—–:,-]{5,}$/.test(line)
  );
}

export default function DocumentPreview({ title, content }: Props) {
  const lines = content.split(/\r?\n/).filter(line => !/^\s*```/.test(line));
  let firstVisible = true;

  return <article className="legal-page">
    <header className="legal-page-header"><span className="legal-page-mark">L</span><span>LEGALEASE <i>·</i> AI-ASSISTED DRAFT</span></header>
    <div className="legal-page-kicker">{title.toUpperCase()}</div>
    <h1>{title}</h1>
    <div className="legal-page-rule" />
    <div className="legal-document-content">
      {lines.map((source, index) => {
        const line = clean(source);
        if (!line) return <div className="legal-paragraph-space" key={index} />;
        if (firstVisible && (line.toLowerCase() === title.toLowerCase() || /^[A-Z][A-Z\s&—–:,-]{5,}$/.test(line))) {
          firstVisible = false;
          return null;
        }
        firstVisible = false;
        if (/^[-*•]\s+/.test(line)) return <div className="legal-list-item" key={index}><span>•</span><p>{line.replace(/^[-*•]\s+/, '')}</p></div>;
        if (isHeading(line)) return <h2 key={index}>{line}</h2>;
        if (/^(effective date|date|parties|between)\s*:/i.test(line)) return <p className="legal-meta-line" key={index}>{line}</p>;
        return <p key={index}>{line}</p>;
      })}
    </div>
    <footer className="legal-page-footer"><span>Prepared in LegalEase</span><span>Draft for review</span></footer>
  </article>;
}
