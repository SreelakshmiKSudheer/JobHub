import type { ReactNode } from "react";

type TypographyVariant =
  | "display"
  | "heading"
  | "body"
  | "caption"
  | "label";

interface TypographyProps {
  children: ReactNode;
  variant?: TypographyVariant;
  className?: string;
  ashtml?: "h1" | "h2" | "h3" | "p" | "span";
}

const variantStyles: Record<TypographyVariant, string> = {
  display:
    "font-display text-4xl md:text-7xl font-extrabold uppercase tracking-[0.1rem]",

  heading:
    "font-display text-2xl md:text-4xl font-bold uppercase tracking-[0.2rem]",

  body:
    "font-body text-base leading-relaxed",

  caption:
    "font-body text-sm",

  label:
    "font-body text-xs font-bold uppercase tracking-[0.15em]",
};

export const Typography = ({
  children,
  variant = "body",
  className = "",
  ashtml: Component = "p",
}: TypographyProps) => {
  return (
    <Component className={`${variantStyles[variant]} ${className}`}>
      {children}
    </Component>
  );
}