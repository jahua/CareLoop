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
    <div className={`big5loop-markdown ${className}`.trim()}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          p: ({ children }) => <p className="big5loop-markdown__p">{children}</p>,
          ul: ({ children }) => <ul className="big5loop-markdown__ul">{children}</ul>,
          ol: ({ children }) => <ol className="big5loop-markdown__ol">{children}</ol>,
          li: ({ children }) => <li className="big5loop-markdown__li">{children}</li>,
          strong: ({ children }) => <strong className="big5loop-markdown__strong">{children}</strong>,
          a: ({ href, children }) => (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="big5loop-markdown__a"
            >
              {children}
            </a>
          ),
          code: ({ className: codeClassName, children, ...props }) => {
            const isBlock = codeClassName?.includes("language-");
            if (isBlock) {
              return (
                <pre className="big5loop-markdown__pre">
                  <code className={codeClassName ?? ""} {...props}>
                    {children}
                  </code>
                </pre>
              );
            }
            return (
              <code className="big5loop-markdown__code" {...props}>
                {children}
              </code>
            );
          },
          blockquote: ({ children }) => (
            <blockquote className="big5loop-markdown__blockquote">{children}</blockquote>
          ),
          h1: ({ children }) => <h1 className="big5loop-markdown__h1">{children}</h1>,
          h2: ({ children }) => <h2 className="big5loop-markdown__h2">{children}</h2>,
          h3: ({ children }) => <h3 className="big5loop-markdown__h3">{children}</h3>,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
