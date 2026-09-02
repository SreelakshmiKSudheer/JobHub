import type { ReactNode } from "react";

type TypographyVariant =
  | "display"
  | "heading"
  | "pageheading"
  | "subheading"
  | "body"
  | "caption"
  | "label";


interface TypographyProps {
  children: ReactNode;
  variant?: TypographyVariant;
  className?: string;
  type?: string;
  ashtml?: "h1" | "h2" | "h3" | "p" | "span";
}

const variantStyles: Record<TypographyVariant, string> = {
  display: "font-display text-4xl md:text-7xl font-extrabold uppercase tracking-[0.1rem]",

  heading: "font-display text-2xl md:text-4xl font-bold uppercase tracking-[0.2rem]",

  body: "font-body text-sm md:text-base ",

  caption: "font-body text-xs md:text-sm ",

  label: "font-body text-xs font-bold uppercase tracking-[0.15em]",

  pageheading: "font-body text-xl md:text-3xl font-bold ",
  subheading: "font-body text-lg md:text-2xl font-bold",
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