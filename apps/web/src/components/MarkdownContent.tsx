"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type MarkdownContentProps = {
  content: string;
  className?: string;
};

/**
 * Renders markdown safely (NextChat-style: GFM, no raw HTML by default).
 * Used for assistant and optionally user message content.
 */
export default function MarkdownContent({
  content,
  className = "",
}: MarkdownContentProps) {
  return (
    <div className={`careloop-markdown ${className}`.trim()}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          p: ({ children }) => <p className="careloop-markdown__p">{children}</p>,
          ul: ({ children }) => <ul className="careloop-markdown__ul">{children}</ul>,
          ol: ({ children }) => <ol className="careloop-markdown__ol">{children}</ol>,
          li: ({ children }) => <li className="careloop-markdown__li">{children}</li>,
          strong: ({ children }) => <strong className="careloop-markdown__strong">{children}</strong>,
          a: ({ href, children }) => (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="careloop-markdown__a"
            >
              {children}
            </a>
          ),
          code: ({ className: codeClassName, children, ...props }) => {
            const isBlock = codeClassName?.includes("language-");
            if (isBlock) {
              return (
                <pre className="careloop-markdown__pre">
                  <code className={codeClassName ?? ""} {...props}>
                    {children}
                  </code>
                </pre>
              );
            }
            return (
              <code className="careloop-markdown__code" {...props}>
                {children}
              </code>
            );
          },
          blockquote: ({ children }) => (
            <blockquote className="careloop-markdown__blockquote">{children}</blockquote>
          ),
          h1: ({ children }) => <h1 className="careloop-markdown__h1">{children}</h1>,
          h2: ({ children }) => <h2 className="careloop-markdown__h2">{children}</h2>,
          h3: ({ children }) => <h3 className="careloop-markdown__h3">{children}</h3>,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
